#
# This rpm is based on the git tree from:
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# version is date of the younger commit

Summary:	Linux kernel firmware files
Name:   	kernel-firmware
Version:	20141027
Release:	3
License:	GPLv2
Group:  	System/Kernel and hardware
URL:    	http://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned
# above, by simply cloning it from
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# and  doing:
# git archive -o linux-firmware-`date +%Y%m%d`.tar --prefix=linux-firmware/ master ; xz -9e linux-firmware-`date +%Y%m%d`.tar
Source0: 	linux-firmware-%{version}.tar.xz
# http://ivtvdriver.org/index.php/Firmware
# Checked out Sat Nov 2 2013
Source1:	http://dl.ivtvdriver.org/ivtv/firmware/ivtv-firmware.tar.gz
# (tpg) https://issues.openmandriva.org/show_bug.cgi?id=918
# looks like kernel-firmware git is not so up to date
Source2:	ath3k-1.fw
Source10:	gen-firmware-lists.sh
Conflicts:	kernel-firmware-extra < %{version}-1
Obsoletes:	korg1212-firmware
Obsoletes:	maestro3-firmware
Obsoletes:	sb16-firmware
Obsoletes:	yamaha-firmware
Suggests:	kernel-firmware-extra
BuildArch:	noarch

%description
This package contains the firmware for in-kernel drivers that was previously
included in the kernel. It is shared by all kernels >= 2.6.27-rc1.

%package extra
Summary:	Extra linux kernel firmware files
Group:		System/Kernel and hardware
License:	Proprietary
URL:    	http://www.kernel.org/
Conflicts:	kernel-firmware < 20120218
Obsoletes:	rt61-firmware

%description extra
This package contains extra redistributable etc. firmwares for in-kernel
drivers. It is shared for all kernels.

%package -n radeon-firmware
Summary:	ATI R600/R700/Evergreen/Fusion Firmware
Group:		System/Kernel and hardware
License:	Proprietary
Url:		http://ati.amd.com/
Obsoletes:	radeon-rlc-firmware
Obsoletes:	radeon-firmware <= 20110310-5
Conflicts:	radeon-firmware <= 20110310-5
Conflicts:	kernel-firmware-extra < 20110310-1

%description -n radeon-firmware
This is Ati Radeon R600/R700/Evergreen (HD5xxx)/Fusion firmware needed
for IRQ handling. It's needed for R600/R700/Evergreen/Fusion KMS support
beginning with 2.6.33 series kernels.

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
Conflicts:      kernel-firmware-extra < 20130624-1
Conflicts:      kernel-firmware-nonfree < 20130624-1

%description -n iwlwifi-agn-ucode
This package contains all the iwlwifi wireless firmware files
supported by the iwlwifi kernel driver. That means all of:
iwlwifi-1xx/1000/2xxx/5xxx/6xxx*.ucode firmwares.

%prep
%setup -q -n linux-firmware

# remove source files we don't need to package
find . -name "*.asm" -o -name "*.S" -o -name "Makefile*" \
     -o -name "*.c" -o -name "*.h" -o -name "CMakeLists.txt" \
     -o -name "*.cmake" -o -name "*.diff" -o -name "*.sh" \
     -o -name "*.pl" -o -name "*.lds" -o -name "*.y" \
     -o -name "*.l" -o -name "*.gperf" -o -name "Kconfig" \
     -o -name "SHA*SUMS" -o -name "COPYRIGHT" -o -name "GPL" \
     -o -name "README*" -o -name configure \
     |xargs rm
# And directories that contained only source files
# (repeatedly to also cover directories that contained only
# directories containing source files)
for i in `seq 1 10`; do
	find . -type d |grep -v '^.$' |xargs -r rmdir --ignore-fail-on-non-empty
done

pwd
sh %SOURCE10

# Symlinks (not mentioned in WHENCE file)
echo '/lib/firmware/cxgb4/t4fw.bin' >>nonfree.list
echo '/lib/firmware/cxgb4/t5fw.bin' >>nonfree.list
echo '/lib/firmware/libertas/sd8688.bin' >>nonfree.list
echo '/lib/firmware/libertas/sd8688_helper.bin' >>nonfree.list
echo '/lib/firmware/rt3070.bin' >>nonfree.list
echo '/lib/firmware/rt3090.bin' >>nonfree.list

# Files not directly mentioned in WHENCE file (signatures, etc.)
echo '/lib/firmware/amd-ucode/microcode_amd.bin.asc' >>nonfree.list
echo '/lib/firmware/amd-ucode/microcode_amd_fam15h.bin.asc' >>nonfree.list
echo '/lib/firmware/s2250.fw' >>nonfree.list
echo '/lib/firmware/s2250_loader.fw' >>nonfree.list
echo '/lib/firmware/ti-connectivity/wl1271-nvs.bin' >>nonfree.list
echo '/lib/firmware/ti-connectivity/wl12xx-nvs.bin' >>nonfree.list

%install
mkdir -p %{buildroot}/lib/firmware
cp -avf * %{buildroot}/lib/firmware
rm -f %{buildroot}/lib/firmware/WHENCE %buildroot/lib/firmware/LICEN?E.*
rm -f %buildroot/lib/firmware/GPL-3
rm -f %buildroot/lib/firmware/*.list

# (tpg) fix for https://issues.openmandriva.org/show_bug.cgi?id=918
cp -f %{SOURCE2} %{buildroot}/lib/firmware/ath3k-1.fw

# Additional firmware (ivtv driver)
mkdir tmp
cd tmp
tar xf %{SOURCE1}
# This one is in linux-firmware git already
rm v4l-cx25840.fw
FW="`ls *.fw *.mpg`"
for i in $FW; do
	mv $i %{buildroot}/lib/firmware/
	echo "/lib/firmware/$i" >>../nonfree.list
done

%files -f free.list
%defattr(0644,root,root,0755)
%doc WHENCE GPL-3 LICENCE.ene_firmware LICENCE.myri10ge_firmware
%doc LICENCE.qla2xxx LICENCE.ueagle-atm4-firmware LICENCE.via_vt6656
%doc LICENSE.dib0700

%files extra -f nonfree.list
%defattr(0644,root,root,0755)
%doc LICENCE.Marvell LICENCE.agere LICENCE.atheros_firmware
%doc LICENCE.broadcom_bcm43xx LICENCE.chelsio_firmware LICENCE.i2400m
%doc LICENCE.mwl8335 LICENCE.OLPC LICENCE.phanfw
%doc LICENCE.ralink-firmware.txt LICENCE.rtlwifi_firmware.txt
%doc LICENCE.tda7706-firmware.txt LICENCE.ti-connectivity LICENCE.xc5000

%files -n radeon-firmware -f radeon.list
%defattr(0644,root,root,0755)
%doc LICENSE.radeon

%files -n iwlwifi-agn-ucode -f iwlwifi.list
%doc LICENCE.iwlwifi_firmware LICENCE.ibt_firmware
