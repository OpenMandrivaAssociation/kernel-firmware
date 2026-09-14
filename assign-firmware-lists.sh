#!/usr/bin/python
# Assign installed firmware files to subpackages.
#
# Mirrors the kernel package's modules_subpackages split: everyday
# firmware stays in kernel-firmware / kernel-firmware-extra; firmware
# that only exists for a split-out kernel module class gets its own
# kernel-firmware-* package.
#
# Usage: assign-firmware-lists.sh FIRMWAREDIR OUTDIR
# Writes files-<pkg>.list in OUTDIR. Every regular file and symlink
# under FIRMWAREDIR is assigned to exactly one package.

import os
import sys
from collections import defaultdict
from fnmatch import fnmatch
from pathlib import Path

PREFIX = "/usr/lib/firmware"

# (glob, package) — first match wins. Globs are matched against the
# path relative to FIRMWAREDIR (no leading slash).
RULES = [
	# GPU / NPU / wifi packages that already existed
	("amdgpu/*", "radeon"),
	("amdnpu/*", "radeon"),
	("radeon/*", "radeon"),
	("nvidia/*", "nvidia"),
	("qcom/*", "adreno"),
	("a300_*", "adreno"),
	("iwlwifi-*", "iwlwifi"),
	("intel/iwlwifi/*", "iwlwifi"),
	("intel/ibt-*", "iwlwifi"),
	("arm/*", "mali"),
	("powervr/*", "powervr"),
	("mellanox/*", "mellanox"),
	("netronome/*", "netronome"),
	# PinePhone-only blobs (the rest of brcm/rtl lives in main/extra)
	("anx7688-*", "pinephone"),
	("hm5065-*", "pinephone"),
	("ov5640_af.bin*", "pinephone"),
	# Matches kernel-*-modules-dvb-* / tuners / radio
	("dvb-*", "dvb"),
	("dvb_driver_*", "dvb"),
	("v4l-*", "dvb"),
	("sms1xxx*", "dvb"),
	("xc3028*", "dvb"),
	("xc4000*", "dvb"),
	("go7007/*", "dvb"),
	("tlg2300*", "dvb"),
	("cmmb_*", "dvb"),
	("isdbt_*", "dvb"),
	("tdmb_*", "dvb"),
	("ngene_*", "dvb"),
	("as102_*", "dvb"),
	("firmware_1900*", "dvb"),
	("av7110/*", "dvb"),
	("dabusb/*", "dvb"),
	("af9005.fw*", "dvb"),
	("NXP7164*", "dvb"),
	("drxd-*", "dvb"),
	("drxk_*", "dvb"),
	("bootcode.bin*", "dvb"),
	("dspbootcode.bin*", "dvb"),
	("f2255usb.bin*", "dvb"),
	("s2250*", "dvb"),
	# Matches kernel-*-modules-infiniband (Intel Omni-Path; mlx is mellanox)
	("hfi1_*", "infiniband"),
	# Matches kernel-*-modules-moxa
	("moxa/*", "moxa"),
	# Matches kernel-*-modules-pcmcia
	("cis/*", "pcmcia"),
	# Matches kernel-*-modules-ath10k_pci / ath6kl_sdio
	("ath10k/*", "ath10k"),
	("ath6k/*", "ath6k"),
	# Everyday / historically free firmware kept in the main package
	# (kernel Recommends kernel-firmware). brcm/cypress/xe are the
	# useful default-install bits; the rest is GPL-with-source.
	("atusb/*", "main"),
	("brcm/*", "main"),
	("cypress/*", "main"),
	("dsp56k/*", "main"),
	("isci/*", "main"),
	("keyspan_pda/*", "main"),
	("r128/*", "main"),
	("usbdux*", "main"),
	("xe/*", "main"),
]

# Also ship these in kernel-firmware-pinephone (same path, same
# content) so the PinePhone image does not have to pull in
# kernel-firmware / kernel-firmware-extra. Primary ownership stays
# with main/extra via RULES above.
PINEPHONE_ALSO = [
	"brcm/BCM20702A1.hcd*",
	"brcm/BCM4345C5.hcd*",
	"brcm/brcmfmac43362-sdio.txt*",
	"brcm/brcmfmac43456-sdio.bin*",
	"brcm/brcmfmac43456-sdio.txt*",
	"rtl_bt/rtl8723bs_config-pine64.bin*",
	"rtl_bt/rtl8723cs_xx_config.bin*",
	"rtl_bt/rtl8723cs_xx_config-pinephone.bin*",
	"rtl_bt/rtl8723cs_xx_fw.bin*",
	"rtlwifi/rtl8188eufw.bin*",
]


def classify(rel: str) -> str:
	for pat, pkg in RULES:
		if fnmatch(rel, pat):
			return pkg
	return "extra"


def parents(rel: str):
	d = os.path.dirname(rel)
	while d and d != ".":
		yield d
		d = os.path.dirname(d)


def main() -> int:
	if len(sys.argv) != 3:
		print(f"usage: {sys.argv[0]} FIRMWAREDIR OUTDIR", file=sys.stderr)
		return 2
	fwdir = Path(sys.argv[1]).resolve()
	outdir = Path(sys.argv[2])
	outdir.mkdir(parents=True, exist_ok=True)

	pkg_of: dict[str, str] = {}
	for dirpath, _dirnames, filenames in os.walk(fwdir):
		for name in filenames:
			path = Path(dirpath) / name
			if not (path.is_file() or path.is_symlink()):
				continue
			rel = str(path.relative_to(fwdir))
			pkg_of[rel] = classify(rel)

	if not pkg_of:
		print(f"{sys.argv[0]}: no firmware files under {fwdir}", file=sys.stderr)
		return 1

	# A directory is exclusive to a package if every file under it
	# belongs to that package.
	dir_pkgs: dict[str, set[str]] = defaultdict(set)
	for rel, pkg in pkg_of.items():
		for d in parents(rel):
			dir_pkgs[d].add(pkg)

	exclusive = {d: next(iter(pkgs)) for d, pkgs in dir_pkgs.items() if len(pkgs) == 1}

	# Keep only maximal exclusive directories
	max_excl: dict[str, str] = {}
	for d, pkg in exclusive.items():
		parent = os.path.dirname(d)
		if parent and parent != "." and exclusive.get(parent) == pkg:
			continue
		max_excl[d] = pkg

	entries: dict[str, list[str]] = defaultdict(list)
	covered: set[str] = set()
	for d, pkg in max_excl.items():
		entries[pkg].append(f"{PREFIX}/{d}")
		prefix = d + "/"
		for rel in pkg_of:
			if rel == d or rel.startswith(prefix):
				covered.add(rel)

	for rel, pkg in pkg_of.items():
		if rel not in covered:
			entries[pkg].append(f"{PREFIX}/{rel}")

	# Duplicate the few blobs the PinePhone needs so that package
	# is installable on its own. Listed as individual files (plus
	# %dir parents below); main/extra keep the exclusive directory.
	for rel in pkg_of:
		if any(fnmatch(rel, pat) for pat in PINEPHONE_ALSO):
			entries["pinephone"].append(f"{PREFIX}/{rel}")

	# %dir for shared parents this package actually uses
	for pkg, files in entries.items():
		need_dir = {PREFIX}
		for item in files:
			d = os.path.dirname(item)
			while d.startswith(PREFIX):
				need_dir.add(d)
				if d == PREFIX:
					break
				d = os.path.dirname(d)
		# Don't %dir a path we already ship as a full directory
		owned = set(files)
		dir_lines = [f"%dir {d}" for d in sorted(need_dir) if d not in owned]
		body = sorted(set(files))
		path = outdir / f"files-{pkg}.list"
		path.write_text("\n".join(dir_lines + body) + "\n")

	map_path = outdir / "assign-firmware.map"
	with map_path.open("w") as fh:
		for rel in sorted(pkg_of):
			fh.write(f"{pkg_of[rel]}\t{rel}\n")

	print("Firmware file assignment:")
	for pkg in sorted(entries):
		n = len(set(entries[pkg]))
		print(f"  {pkg}: {n} entries")
	return 0


if __name__ == "__main__":
	sys.exit(main())
