# False positive -- some firmware bits are mistaken for host binaries
%define _binaries_in_noarch_packages_terminate_build 0

%global _firmwaredir %{_prefix}/lib/firmware

# Needed if you want to be compatible with kernels < 5.15
# (support for compression was added then)
%bcond_without compress

Summary:	Linux kernel firmware files
Name:		kernel-firmware
Version:	20260910
Release:	2
License:	GPLv2
Group:		System/Kernel and hardware
URL:		https://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned
# above, by simply cloning it from
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# and doing:
# git archive -o linux-firmware-`date +%Y%m%d`.tar --prefix=linux-firmware-`date +%Y%m%d`/ origin/main ; zstd --ultra -22 --rm linux-firmware-`date +%Y%m%d`.tar
#
# We can also use upstream tarball generation with links like
# https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-main.tar.gz
# or
# https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/snapshot/linux-firmware-20231211.tar.gz
# but unfortunately those tarballs are huge (zlib is not exactly efficient).
Source0:	linux-firmware-%{version}.tar.zst
# Firmware for various components of PinePhone, PineBook and Orange Pi
# https://megous.com/git/linux-firmware
Source1:	linux-firmware-pine64-20240313.tar.zst
# Adreno firmware, from OQ820 BSP 3.2
Source2:	adreno-fw-820BSP3.2.tar.xz
# Firmware for Hauppauge HVR-1975
# see http://www.hauppauge.com/site/support/linux.html
Source3:	https://s3.amazonaws.com/hauppauge/linux/linux-ubuntu-14-04-2.tar.xz
# Firmware for various DVB receivers
Source4:	https://github.com/OpenELEC/dvb-firmware/archive/master/dvb-firmware-%{version}.tar.gz
# Additional Hauppauge TV receivers
Source13:	https://www.hauppauge.com/linux/firmware_1900.fw
# SI2157 tuner (TurboSight 6281/6285 on saa716x-budget, Hauppauge dualHD, …)
# Same blob as dvb_driver_si2157_rom50.fw; not in OpenELEC/linux-firmware.
# https://github.com/LibreELEC/dvb-firmware
Source14:	https://raw.githubusercontent.com/LibreELEC/dvb-firmware/master/firmware/dvb-tuner-si2157-a30-01.fw
Source100:	assign-firmware-lists.sh
Conflicts:	kernel-firmware-extra < %{version}-1
Obsoletes:	korg1212-firmware
Obsoletes:	maestro3-firmware
Obsoletes:	sb16-firmware
Obsoletes:	yamaha-firmware
Obsoletes:	alsa-firmware < 1.0.29-5
Provides:	alsa-firmware = 1.0.29-5
Suggests:	kernel-firmware-extra
BuildArch:	noarch
BuildRequires:	make
BuildRequires:	rdfind
BuildRequires:	parallel
BuildRequires:	python

%description
This package contains commonly needed firmware for in-kernel drivers
(Broadcom/Cypress Wi-Fi, Intel Xe GPU, and a few GPL-with-source
blobs). It is shared by all kernels >= 2.6.27-rc1.

Most other redistributable firmware is in kernel-firmware-extra.
Rare hardware (DVB, InfiniBand, PCMCIA, MOXA, ath10k, ath6k)
has its own kernel-firmware-* package, matching the
kernel-*-modules-* split.

%package extra
Summary:	Extra Linux kernel firmware files
Group:		System/Kernel and hardware
License:	Proprietary
URL:		https://www.kernel.org/
Conflicts:	kernel-firmware < 20120218
Obsoletes:	rt61-firmware
Obsoletes:	ueagle-firmware < 1.1-12
Provides:	ueagle-firmware = 1.1-12
Suggests:	kernel-firmware-dvb
Suggests:	kernel-firmware-infiniband
Suggests:	kernel-firmware-ath10k
Suggests:	kernel-firmware-ath6k
Suggests:	kernel-firmware-moxa
Suggests:	kernel-firmware-pcmcia

%description extra
This package contains extra redistributable firmware for in-kernel
drivers that is commonly needed on desktops and laptops (Wi-Fi,
Bluetooth, Ethernet, laptop audio, cameras, …).

Firmware that only exists for rarely used kernel modules lives in
matching kernel-firmware-* packages (DVB, InfiniBand, PCMCIA,
MOXA, ath10k, ath6k), the same split as kernel-*-modules-*.
If you do not know that you need those, you do not.

%package -n mali-g610-firmware
Summary:	Firmware files needed for Mali G610 graphics chips
Group:		System/Kernel and hardware
License:	Proprietary

%description -n mali-g610-firmware
Firmware files needed for Mali G610 graphics chips

%package -n firmware-powervr
Summary:	Firmware files needed for Imagination PowerVR graphics chips
Group:		System/Kernel and hardware
License:	Proprietary

%description -n firmware-powervr
Firmware files needed for Imagination PowerVR graphics chips

%package -n radeon-firmware
Summary:	ATI R600/R700/Evergreen/Fusion Firmware
Group:		System/Kernel and hardware
License:	Proprietary
Url:		https://ati.amd.com/
Obsoletes:	radeon-rlc-firmware
Obsoletes:	radeon-firmware <= 20110310-5
Conflicts:	radeon-firmware <= 20110310-5
Conflicts:	kernel-firmware-extra < 20110310-1

%description -n radeon-firmware
This is Ati Radeon R600/R700/Evergreen (HD5xxx)/Fusion firmware needed
for IRQ handling. It's needed for R600/R700/Evergreen/Fusion KMS support
beginning with 2.6.33 series kernels.

%package -n nvidia-firmware
Summary:	NVIDIA Firmware
Group:		System/Kernel and hardware
License:	Proprietary
Url:		https://nvidia.com/

%description -n nvidia-firmware
Firmware files needed to use NVIDIA GPUs, even when using the Open
Source Nouveau driver

# Directories replaced with symlinks
%pretrans -p <lua> -n nvidia-firmware
paths = {"%{_firmwaredir}/nvidia/ad103", "%{_firmwaredir}/nvidia/ad104", "%{_firmwaredir}/nvidia/ad106", "%{_firmwaredir}/nvidia/ad107"}
for i = 1, 4 do
	path = paths[i]
	st = posix.stat(path)
	if st and st.type == "directory" then
		status = os.rename(path, path .. ".rpmmoved")
		if not status then
			suffix = 0
			while not status do
				suffix = suffix + 1
				status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
			end
			os.rename(path, path .. ".rpmmoved")
		end
	end
end

%package -n adreno-firmware
Summary:	Adreno firmware
Group:		System/Kernel and hardware
License:	Proprietary
Url:		https://github.com/freedreno
Suggests:	kernel-firmware-ath10k

%description -n adreno-firmware
This is Adreno firmware needed for accelerated graphics on Adreno
graphics chipsets. Some Snapdragon boards also need
kernel-firmware-ath10k for the on-SoC Wi-Fi firmware.

%package -n iwlwifi-agn-ucode
Summary:	Nonfree iwlwifi firmware files for the Linux kernel
Obsoletes:	iwlwifi-100-ucode
Obsoletes:	iwlwifi-105-ucode
Obsoletes:	iwlwifi-135-ucode
Obsoletes:	iwlwifi-1000-ucode
Obsoletes:	iwlwifi-2000-ucode
Obsoletes:	iwlwifi-2030-ucode
Obsoletes:	iwlwifi-5000-ucode
Obsoletes:	iwlwifi-5150-ucode
Obsoletes:	iwlwifi-6000-ucode
Obsoletes:	iwlwifi-6005-ucode
Obsoletes:	iwlwifi-6030-ucode
Obsoletes:	iwlwifi-6050-ucode
Conflicts:	kernel-firmware-extra < 20130624-1
Conflicts:	kernel-firmware-nonfree < 20130624-1

%description -n iwlwifi-agn-ucode
Firmware for Intel wireless (iwlwifi) and the matching Intel
Bluetooth (ibt) blobs. Covers every generation shipped by
linux-firmware, from 100/1000 through current Wi-Fi 7 parts.

%package pinephone
Summary:	Firmware files needed to drive components of the PinePhone
Group:		System/Kernel and hardware

%description pinephone
Firmware files needed to drive components of the PinePhone.
Standalone — includes the Broadcom and Realtek blobs the phone
needs, so kernel-firmware / kernel-firmware-extra are not required
(the PinePhone is short on storage and will never need the rest).

%package mellanox
Summary:	Firmware files needed to drive Mellanox network cards
Group:		System/Kernel and hardware

%description mellanox
Firmware files needed to drive Mellanox / NVIDIA Networking cards
(Ethernet and InfiniBand). These are high-end server adapters.
If you do not know that you need this, you do not.

%package netronome
Summary:	Firmware files needed to drive Netronome network cards
Group:		System/Kernel and hardware

%description netronome
Firmware files needed to drive Netronome network cards.

Netronome cards are ultra high end server equipment unlikely
to show up in consumer grade hardware. If you don't know what
it is, you don't need to install this package.

# Firmware counterparts of kernel-*-modules-* splits. Files used to live
# in kernel-firmware / kernel-firmware-extra; Conflicts against the old
# unsplit packages so upgrades do not leave two owners of the same blob.

%package dvb
Summary:	Firmware for DVB, digital TV and analog TV tuner devices
Group:		System/Kernel and hardware
Conflicts:	kernel-firmware-extra < %{version}-1
Conflicts:	kernel-firmware < %{version}-1

%description dvb
Firmware for DVB frontends, DVB USB sticks, tuners and related TV
capture devices. Matches the kernel-*-modules-dvb-* / tuners / radio
split. Not needed unless you have a TV tuner.

%package infiniband
Summary:	Firmware for Intel Omni-Path (hfi1) InfiniBand adapters
Group:		System/Kernel and hardware
Conflicts:	kernel-firmware-extra < %{version}-1

%description infiniband
Firmware for Intel Omni-Path hfi1 InfiniBand adapters. Matches
kernel-*-modules-infiniband. Mellanox InfiniBand firmware is in
kernel-firmware-mellanox. If you do not know that you need this,
you do not.

%package moxa
Summary:	Firmware for MOXA Intellio serial cards
Group:		System/Kernel and hardware
Conflicts:	kernel-firmware-extra < %{version}-1

%description moxa
Firmware for MOXA Intellio (C218/C320) serial cards. Matches
kernel-*-modules-moxa.

%package pcmcia
Summary:	PCMCIA Card Information Structure firmware
Group:		System/Kernel and hardware
Conflicts:	kernel-firmware < %{version}-1

%description pcmcia
PCMCIA CIS (Card Information Structure) firmware. Matches
kernel-*-modules-pcmcia. Not needed on machines without a
PC Card slot.

%package ath10k
Summary:	Firmware for Qualcomm Atheros 802.11ac (ath10k) devices
Group:		System/Kernel and hardware
Conflicts:	kernel-firmware-extra < %{version}-1

%description ath10k
Firmware for Qualcomm Atheros 802.11ac devices driven by ath10k.
Matches kernel-*-modules-ath10k_pci.

%package ath6k
Summary:	Firmware for Qualcomm Atheros AR600x (ath6kl) devices
Group:		System/Kernel and hardware
Conflicts:	kernel-firmware-extra < %{version}-1

%description ath6k
Firmware for Qualcomm Atheros AR600x SDIO/USB devices driven by
ath6kl. Matches kernel-*-modules-ath6kl_sdio.

%prep
%autosetup -p1 -n linux-firmware-%{version}
# Let's compress a bit more...
sed -i -e 's,xz --compress,xz --compress -9,g' copy-firmware.sh
# And be a bit more verbose to give some progress indication
sed -i -e 's,--xz,-v --xz,g;s,--zstd,-v --zstd,g' Makefile

%install
%if %{with compress}
%make_build DESTDIR=%{buildroot}/ FIRMWAREDIR=%{_firmwaredir} install-xz
%else
%make_build DESTDIR=%{buildroot}/ FIRMWAREDIR=%{_firmwaredir} install
%endif

obsolete=0

# Pine64 devices
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{S:1}
cd linux-firmware-pine64
# Already in upstream firmware
rm -rf brcm/brcmfmac43362-sdio.bin \
	brcm/brcmfmac43455-sdio.bin \
	brcm/brcmfmac43455-sdio.clm_blob \
	brcm/brcmfmac43455-sdio.pine64,pinephone-pro.txt \
	brcm/brcmfmac43455-sdio.pine64,pinebook-pro.txt \
	rtlwifi \
	rtl_bt/rtl8821c_config.bin \
	rtl_bt/rtl8821c_fw.bin \
	rtl_bt/rtl8822b_config.bin \
	rtl_bt/rtl8822b_fw.bin \
	rtl_nic \
	rt2870.bin \
	rtw88 \
	rtw89 \
	rockchip
# Duplicate from wireless-regdb
rm regulatory.db regulatory.db.p7s
if [ -d %{buildroot}%{_firmwaredir}/ap6275p ]; then
	echo "===== ap6275p has been added upstream, remove from pine64 ====="
	obsolete=$((obsolete+1))
fi
mv ap6275p %{buildroot}%{_firmwaredir}/
mkdir -p %{buildroot}%{_firmwaredir}/brcm/2020-02-12
rm rtl_bt/rtl8723cs_xx_config.bin
rm rtl_bt/rtl8723cs_xx_fw.bin
for i in *.bin brcm/*.* brcm/2020-02-12/* rtl_bt/*.bin; do
	if [ -e %{buildroot}%{_firmwaredir}/$i -o -e %{buildroot}%{_firmwaredir}/$i.xz ]; then
		echo "===== $i from pine64 has been added upstream, please remove ====="
		obsolete=$((obsolete+1))
	fi
	mv $i %{buildroot}%{_firmwaredir}/$i
%if %{with compress}
	if [ -d "%{buildroot}%{_firmwaredir}/$i" ]; then
		xz -9 -C crc32 %{buildroot}%{_firmwaredir}/"$i"/*
		echo "%{_firmwaredir}/$i" >>../../nonfree.list
	else
		xz -9 -C crc32 "%{buildroot}%{_firmwaredir}/$i"
		echo "%{_firmwaredir}/$i.xz" >>../../nonfree.list
	fi
%else
	echo "%{_firmwaredir}/$i" >>../../nonfree.list
%endif
done
cd ../..

# Adreno
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{SOURCE2}
# Already upstream
rm a225_pfp.fw \
	a225_pm4.fw \
	a300_pfp.fw \
	a300_pm4.fw \
	a330_pfp.fw \
	a330_pm4.fw \
	a420_pfp.fw \
	a420_pm4.fw \
	a530_pfp.fw \
	a530_pm4.fw \
	a530v3_gpmu.fw2 \
	a530_zap.b00 \
	a530_zap.b01 \
	a530_zap.b02 \
	a530_zap.mdt
FW="$(ls)"
if [ -z "$FW" ]; then
	echo "Nothing left of adreno FW -- remove tarball"
	exit 1
fi
for i in $FW; do
	if ! [ -e %{buildroot}%{_firmwaredir}/$i -o -e %{buildroot}%{_firmwaredir}/$i.xz ] && ! [ -e %{buildroot}%{_firmwaredir}/qcom/$i -o -e %{buildroot}%{_firmwaredir}/qcom/$i.xz ]; then
		mv $i %{buildroot}%{_firmwaredir}/qcom/
%if %{with compress}
		xz -9 -C crc32 "%{buildroot}%{_firmwaredir}/qcom/$i"
		echo "%{_firmwaredir}/qcom/$i.xz" >>../adreno.list
%else
		echo "%{_firmwaredir}/qcom/$i" >>../adreno.list
%endif
	else
		echo "===== $i from adreno has been added upstream, please remove ====="
		obsolete=$((obsolete+1))
	fi
done
cd ..

# Assorted DVB
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{SOURCE4}
cd dvb-firmware-master/firmware
# Not yet there
if [ -e firmware_1900.fw ]; then
	echo "===== firmware_1900 has been added to OpenELEC - remove from spec ====="
	obsolete=$((obsolete+1))
fi
cp %{S:13} .
# Already added upstream
rm -rf	dvb-fe-xc4000-1.4.1.fw \
	dvb-fe-xc5000-1.6.114.fw \
	dvb-fe-xc5000c-4.1.30.7.fw \
	dvb-usb-dib0700-1.20.fw \
	dvb-usb-it9135-01.fw \
	dvb-usb-it9135-02.fw \
	dvb-usb-terratec-h5-drxk.fw \
	lgs8g75.fw \
	sms1xxx-hcw-55xxx-dvbt-02.fw \
	sms1xxx-hcw-55xxx-isdbt-02.fw \
	sms1xxx-nova-a-dvbt-01.fw \
	sms1xxx-nova-b-dvbt-01.fw \
	sms1xxx-stellar-dvbt-01.fw \
	v4l-cx231xx-avcore-01.fw \
	v4l-cx23418-apu.fw \
	v4l-cx23418-cpu.fw \
	v4l-cx23418-dig.fw \
	v4l-cx23885-avcore-01.fw \
	v4l-cx25840.fw \
	tlg2300_firmware.bin \
	cmmb_vega_12mhz.inp \
	cmmb_venice_12mhz.inp \
	dvb_nova_12mhz.inp \
	dvb_nova_12mhz_b0.inp \
	isdbt_nova_12mhz_b0.inp \
	isdbt_nova_12mhz.inp \
	isdbt_rio.inp \
	tdmb_nova_12mhz.inp \
	go7007/go7007fw.bin \
	go7007/go7007tv.bin \
	go7007/lr192.fw \
	go7007/px-m402u.fw \
	go7007/px-tv402u.fw \
	go7007/s2250-1.fw \
	go7007/s2250-2.fw \
	go7007/wis-startrek.fw \
	s2250_loader.fw \
	s2250.fw \
	ttusb-budget/dspbootcode.bin

for i in *.fw* *.bin *.inp *.mc *.mpg; do
	if [ -e %{buildroot}%{_firmwaredir}/$i -o -e %{buildroot}%{_firmwaredir}/$i.xz ]; then
		echo "===== Please remove $i from DVB firmware, it's upstream ====="
		obsolete=$((obsolete+1))
	fi
	mv $i %{buildroot}%{_firmwaredir}/
%if %{with compress}
	if [ -h "%{buildroot}%{_firmwaredir}/$i" ]; then
		cd %{buildroot}%{_firmwaredir}
		TGT=$(readlink "$i")
		ln -s $TGT.xz "$i".xz
		rm "$i"
		cd -
	else
		xz -9 -C crc32 "%{buildroot}%{_firmwaredir}/$i"
	fi
	echo "%{_firmwaredir}/$i.xz" >>../../../nonfree.list
%else
	echo "%{_firmwaredir}/$i" >>../../../nonfree.list
%endif
done
cd ../../..

# SI2157 tuner firmware (saa716x TurboSight 6281/6285 and other Si2157 cards).
# Optional for ROM 0x50 A30 parts, but the driver requests both names.
if [ -e %{buildroot}%{_firmwaredir}/dvb-tuner-si2157-a30-01.fw -o \
     -e %{buildroot}%{_firmwaredir}/dvb-tuner-si2157-a30-01.fw.xz ]; then
	echo "===== si2157-a30 firmware has been added upstream, please remove Source14 ====="
	obsolete=$((obsolete+1))
else
	cp %{S:14} %{buildroot}%{_firmwaredir}/dvb-tuner-si2157-a30-01.fw
%if %{with compress}
	xz -9 -C crc32 %{buildroot}%{_firmwaredir}/dvb-tuner-si2157-a30-01.fw
	ln -s dvb-tuner-si2157-a30-01.fw.xz \
		%{buildroot}%{_firmwaredir}/dvb_driver_si2157_rom50.fw.xz
%else
	ln -s dvb-tuner-si2157-a30-01.fw \
		%{buildroot}%{_firmwaredir}/dvb_driver_si2157_rom50.fw
%endif
fi

# Hauppauge
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{SOURCE3}
if [ -e %{buildroot}%{_firmwaredir}/v4l-pvrusb2-160xxx-01.fw -o -e %{buildroot}%{_firmwaredir}/v4l-pvrusb2-160xxx-01.fw.xz ]; then
	echo "===== pvrusb2-160xxx firmware has been merged upstream, please remove it here ====="
	obsolete=$((obsolete+1))
fi
cp "Linux-Ubuntu-14-04-2/firmware/HVR 19x5/v4l-pvrusb2-160xxx-01.fw" %{buildroot}%{_firmwaredir}/
cd ..
%if %{with compress}
xz -9 -C crc32 "%{buildroot}%{_firmwaredir}/v4l-pvrusb2-160xxx-01.fw"
echo '%{_firmwaredir}/v4l-pvrusb2-160xxx-01.fw.xz' >>nonfree.list
%else
echo '%{_firmwaredir}/v4l-pvrusb2-160xxx-01.fw' >>nonfree.list
%endif

if [ "$obsolete" -gt 0 ]; then
	echo "Some files being added manually have gone upstream"
	echo "and need to be removed."
	echo "Search the log for '====='"
	exit 1
fi

# Build file lists from what was actually installed so an upstream
# firmware drop cannot leave us with stale or missing %files entries.
# Assignment follows the kernel modules_subpackages split.
python %{S:100} %{buildroot}%{_firmwaredir} .
for pkg in main extra radeon nvidia adreno iwlwifi mali powervr \
	mellanox netronome pinephone dvb infiniband moxa pcmcia \
	ath10k ath6k; do
	if [ ! -s files-$pkg.list ]; then
		echo "assign-firmware-lists.sh produced no files-$pkg.list"
		exit 1
	fi
done

%files -f files-main.list
%defattr(0644,root,root,0755)
%doc LICENSE LICENSE-CRITERIA.md WHENCE README.md LICENSES

%files extra -f files-extra.list
%defattr(0644,root,root,0755)

%files -n mali-g610-firmware -f files-mali.list

%files -n firmware-powervr -f files-powervr.list

%files -n radeon-firmware -f files-radeon.list
%defattr(0644,root,root,0755)

%files -n nvidia-firmware -f files-nvidia.list

%files -n adreno-firmware -f files-adreno.list
%defattr(0644,root,root,0755)

%files -n iwlwifi-agn-ucode -f files-iwlwifi.list

%files mellanox -f files-mellanox.list

%files netronome -f files-netronome.list

%files pinephone -f files-pinephone.list

%files dvb -f files-dvb.list

%files infiniband -f files-infiniband.list

%files moxa -f files-moxa.list

%files pcmcia -f files-pcmcia.list

%files ath10k -f files-ath10k.list

%files ath6k -f files-ath6k.list
