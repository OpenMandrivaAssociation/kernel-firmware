#
# This rpm is based on the git tree from:
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# version is date of the youngest commit

# False positive -- some firmware bits are mistaken for host binaries
%define _binaries_in_noarch_packages_terminate_build 0

Summary:	Linux kernel firmware files
Name:		kernel-firmware
Version:	20211223
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
URL:		http://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned
# above, by simply cloning it from
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# and doing:
# git archive -o kernel-firmware-`date +%Y%m%d`.tar --prefix=kernel-firmware-`date +%Y%m%d`/ origin/main ; zstd --ultra -22 --rm kernel-firmware-`date +%Y%m%d`.tar
Source0:	kernel-firmware-%{version}.tar.zst
# Firmware for various components of PinePhone, PineBook and Orange Pi
# https://megous.com/git/linux-firmware
Source1:	linux-firmware-pine64-20211223.tar.zst
# Adreno firmware, from OQ820 BSP 3.2
Source2:	adreno-fw-820BSP3.2.tar.xz
# Firmware for Hauppauge HVR-1975
# see http://www.hauppauge.com/site/support/linux.html
Source3:	https://s3.amazonaws.com/hauppauge/linux/linux-ubuntu-14-04-2.tar.xz
# Firmware for various DVB receivers
Source4:	https://github.com/OpenELEC/dvb-firmware/archive/master/dvb-firmware-%{version}.tar.gz
# Broadcom firmware for Raspberry Pi 400
Source5:	https://raw.githubusercontent.com/RPi-Distro/firmware-nonfree/master/brcm/brcmfmac43456-sdio.bin
Source6:	https://raw.githubusercontent.com/RPi-Distro/firmware-nonfree/master/brcm/brcmfmac43456-sdio.clm_blob
Source7:	https://raw.githubusercontent.com/RPi-Distro/firmware-nonfree/master/brcm/brcmfmac43456-sdio.txt
# Those exist in upstream kernel-firmware, but RPi has newer versions
Source8:	https://raw.githubusercontent.com/RPi-Distro/firmware-nonfree/master/brcm/brcmfmac43455-sdio.bin
Source9:	https://raw.githubusercontent.com/RPi-Distro/firmware-nonfree/master/brcm/brcmfmac43455-sdio.txt
# RPi bluetooth firmware
Source11:	https://github.com/RPi-Distro/bluez-firmware/raw/master/broadcom/BCM43430A1.hcd
Source12:	https://github.com/RPi-Distro/bluez-firmware/raw/master/broadcom/BCM4345C0.hcd
# Additional Hauppauge TV receivers
Source13:	https://www.hauppauge.com/linux/firmware_1900.fw
Source100:	gen-firmware-lists.sh
Conflicts:	kernel-firmware-extra < %{version}-1
Obsoletes:	korg1212-firmware
Obsoletes:	maestro3-firmware
Obsoletes:	sb16-firmware
Obsoletes:	yamaha-firmware
Obsoletes:	alsa-firmware < 1.0.29-5
Provides:	alsa-firmware = 1.0.29-5
Suggests:	kernel-firmware-extra
BuildArch:	noarch

%description
This package contains the firmware for in-kernel drivers that was previously
included in the kernel. It is shared by all kernels >= 2.6.27-rc1.

%package extra
Summary:	Extra linux kernel firmware files
Group:		System/Kernel and hardware
License:	Proprietary
URL:		http://www.kernel.org/
Conflicts:	kernel-firmware < 20120218
Obsoletes:	rt61-firmware
Obsoletes:	ueagle-firmware < 1.1-12
Provides:	ueagle-firmware = 1.1-12

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

%package -n adreno-firmware
Summary:	Adreno firmware
Group:		System/Kernel and hardware
License:	Proprietary
Url:		https://github.com/freedreno

%description -n adreno-firmware
This is Adreno firmware needed for accelerated graphics on Adreno
graphics chipsets.

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
This package contains all the iwlwifi wireless firmware files
supported by the iwlwifi kernel driver. That means all of:
iwlwifi-1xx/1000/2xxx/5xxx/6xxx*.ucode firmwares.

%package pinephone
Summary:	Firmware files needed to drive components of the PinePhone
Group:		System/Kernel and hardware

%description pinephone
Firmware files needed to drive components of the PinePhone

%prep
%setup -q

# remove source files we don't need to package
find . -name "*.asm" -o -name "*.S" -o -name "Makefile*" \
     -o -name "*.c" -o -name "*.h" -o -name "CMakeLists.txt" \
     -o -name "*.cmake" -o -name "*.diff" -o -name "*.sh" \
     -o -name "*.pl" -o -name "*.lds" -o -name "*.y" \
     -o -name "*.l" -o -name "*.gperf" -o -name "Kconfig" \
     -o -name "SHA*SUMS" -o -name "COPYRIGHT" -o -name "GPL" \
     -o -name "README*" -o -name configure -o -name ChangeLog \
     |xargs rm
# And directories that contained only source files
# (repeatedly to also cover directories that contained only
# directories containing source files)
for i in `seq 1 10`; do
    find . -type d |grep -v '^.$' |xargs -r rmdir --ignore-fail-on-non-empty
done

pwd
echo "--------------" >> WHENCE
sh %SOURCE100

# Files not directly mentioned in WHENCE file (signatures, etc.)
echo '/lib/firmware/amd-ucode/microcode_amd.bin.asc' >>nonfree.list
echo '/lib/firmware/amd-ucode/microcode_amd_fam15h.bin.asc' >>nonfree.list
echo '/lib/firmware/amd-ucode/microcode_amd_fam16h.bin.asc' >>nonfree.list
echo '/lib/firmware/amd-ucode/microcode_amd_fam17h.bin.asc' >>nonfree.list
echo '/lib/firmware/ath10k/QCA4019/hw1.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw2.1/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9377/hw1.0/notice_ath10k_firmware-sdio-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw3.0/notice_ath10k_firmware-sdio-6.txt' >> nonfree.list
echo '/lib/firmware/ath11k/IPQ6018/hw1.0/Notice.txt' >> nonfree.list
echo '/lib/firmware/ath11k/IPQ8074/hw2.0/Notice.txt' >> nonfree.list
echo '/lib/firmware/ath11k/QCA6390/hw2.0/Notice.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw3.0/board-2.bin' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw3.0/notice_ath10k_firmware-4.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw3.0/notice_ath10k_firmware-6.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9377/hw1.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9377/hw1.0/notice_ath10k_firmware-6.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9887/hw1.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9888/hw2.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA988X/hw2.0/notice_ath10k_firmware-4.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA988X/hw2.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9984/hw1.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA99X0/hw2.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/WCN3990/hw1.0/notice.txt_wlanmdsp' >>nonfree.list
echo '/lib/firmware/brcm/brcmfmac4330-sdio.Prowise-PT301.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43340-sdio.meegopad-t08.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43340-sdio.predia-basic.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43362-sdio.cubietech,cubietruck.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43430a0-sdio.jumper-ezpad-mini3.txt' >> nonfree.list
echo '"/lib/firmware/brcm/brcmfmac43430a0-sdio.ONDA-V80 PLUS.txt"' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43430a0-sdio.ilife-S806.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43430-sdio.AP6212.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43430-sdio.Hampoo-D2D3_Vi8A1.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43430-sdio.MUR1DX.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43430-sdio.raspberrypi,3-model-b.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43455-sdio.raspberrypi,3-model-b-plus.txt' >> nonfree.list
echo '/lib/firmware/brcm/brcmfmac43455-sdio.raspberrypi,4-model-b.txt' >>nonfree.list
echo '/lib/firmware/brcm/brcmfmac4356-pcie.gpd-win-pocket.txt' >> nonfree.list
echo '/lib/firmware/qca/NOTICE.txt' >> nonfree.list

%install
mkdir -p %{buildroot}/lib/firmware
cp -avf * %{buildroot}/lib/firmware
rm -f %{buildroot}/lib/firmware/WHENCE %{buildroot}/lib/firmware/LICEN?E.*
rm -f %{buildroot}/lib/firmware/GPL-3
rm -f %{buildroot}/lib/firmware/GPL-2
rm -f %{buildroot}/lib/firmware/*.list
rm -f %{buildroot}/lib/firmware/check_whence.py

# Pine64 devices
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{S:1}
cd linux-firmware-pine64
# Already in upstream firmware
rm brcm/brcmfmac43362-sdio.bin \
	rtlwifi/rtl8188eufw.bin
# Duplicate from wireless-regdb
rm regulatory.db regulatory.db.p7s
rmdir rtlwifi
for i in *.bin brcm/* rtl_bt/*; do
	if [ -e %{buildroot}/lib/firmware/$i ]; then
		echo "$i has been added upstream, please remove"
		exit 1
	fi
	mv $i %{buildroot}/lib/firmware/$i
	echo "/lib/firmware/$i" >>../../nonfree.list
done
cd ../..

# Adreno
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{SOURCE2}
FW="$(ls)"
for i in $FW; do
	if ! [ -e %{buildroot}/lib/firmware/$i ] && ! [ -e %{buildroot}/lib/firmware/qcom/$i ]; then
		mv $i %{buildroot}/lib/firmware/qcom/
		echo "/lib/firmware/qcom/$i" >>../adreno.list
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
	echo firmware_1900 has been added to OpenELEC - remove from spec
	exit 1
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
	if [ -e %{buildroot}/lib/firmware/$i ]; then
		echo "******* Please remove $i from DVB firmware, it's upstream *******"
		exit 1
	fi
	cp $i %{buildroot}/lib/firmware/
	echo "/lib/firmware/$i" >>../../../nonfree.list
done
cd ../../..

# Hauppauge
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{SOURCE3}
if [ -e %{buildroot}/lib/firmware/v4l-pvrusb2-160xxx-01.fw ]; then
	echo "pvrusb2-160xxx firmware has been merged upstream, please remove it here"
	exit 1
fi
cp "Linux-Ubuntu-14-04-2/firmware/HVR 19x5/v4l-pvrusb2-160xxx-01.fw" %{buildroot}/lib/firmware/
cd ..
echo '/lib/firmware/v4l-pvrusb2-160xxx-01.fw' >>nonfree.list

# Raspberry Pi (and potentially others)
if [ -e %{buildroot}/lib/firmware/brcm/brcmfmac43456-sdio.raspberrypi,400.txt ]; then
	echo "Looks like Raspberry Pi 400 firmware has been merged,"
	echo "please check if the updates (Sources 5 to 10) can be removed."
	exit 1
fi
cp -f %{S:5} %{S:6} %{S:7} %{S:8} %{S:9} %{buildroot}/lib/firmware/brcm/
if [ -n "$(find %{buildroot} -name BCM43430A1.hcd)" ]; then
	echo "Broadcom bluetooth firmware has been merged upstream, please remove"
	exit 1
fi
cp -f %{S:11} %{S:12} %{buildroot}/lib/firmware/
ln -sf brcmfmac43456-sdio.clm_blob %{buildroot}/lib/firmware/brcm/brcmfmac43455-sdio.clm_blob
ln -sf brcmfmac43456-sdio.txt %{buildroot}/lib/firmware/brcm/brcmfmac43456-sdio.raspberrypi,400.txt
ln -sf brcmfmac43456-sdio.txt %{buildroot}/lib/firmware/brcm/brcmfmac43456-sdio.raspberrypi,4-compute-module.txt
cat >>nonfree.list <<EOF
/lib/firmware/brcm/brcmfmac43456-sdio.bin
/lib/firmware/brcm/brcmfmac43456-sdio.clm_blob
/lib/firmware/brcm/brcmfmac43456-sdio*.txt
/lib/firmware/brcm/brcmfmac43455-sdio.bin
/lib/firmware/brcm/brcmfmac43455-sdio.clm_blob
/lib/firmware/brcm/brcmfmac43455-sdio.txt
/lib/firmware/brcm/brcmfmac43455-sdio.acepc-t8.txt
/lib/firmware/BCM43430A1.hcd
/lib/firmware/BCM4345C0.hcd
EOF

# (tpg) fix it
sed -i -e 's#^/lib/firmware/isci/$##' free.list
sed -i -e 's#^/lib/firmware/cis/$##' free.list
echo '/lib/firmware/cis/src/DP83903.cis' >>free.list
echo '/lib/firmware/cis/src/LA-PCM.cis' >>free.list
echo '/lib/firmware/cis/src/NE2K.cis' >>free.list
echo '/lib/firmware/cis/src/PCMLM28.cis' >>free.list
echo '/lib/firmware/cis/src/PE-200.cis' >>free.list
echo '/lib/firmware/cis/src/PE520.cis' >>free.list
echo '/lib/firmware/cis/src/tamarack.cis' >>free.list

echo '/lib/firmware/intel/ibt-20-0-3.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-20-0-3.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-20-1-3.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-20-1-3.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-0-0.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-0-0.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-0-1.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-0-1.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-0-4.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-0-4.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-16-4.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-16-4.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-32-0.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-32-0.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-32-1.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-32-1.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-240-1.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-240-1.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-240-4.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-19-240-4.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-20-1-4.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-20-1-4.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-0041-0041.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-0041-0041.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-0040-1020.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-0040-1020.sfi' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-1040-1020.ddc' >>iwlwifi.list
echo '/lib/firmware/intel/ibt-1040-1020.sfi' >>iwlwifi.list

echo '/lib/firmware/amd-ucode/microcode_amd_fam19h.bin.asc' >>nonfree.list

# rpm doesn't like dupes, but the WHENCE file contains some
cat free.list |sort |uniq >free.list.new
mv -f free.list.new free.list
cat nonfree.list |sort |uniq >nonfree.list.new
mv -f nonfree.list.new nonfree.list

%files -f free.list
%defattr(0644,root,root,0755)
%doc WHENCE GPL-3 LICENCE.ene_firmware LICENCE.myri10ge_firmware
%doc LICENCE.qla2xxx LICENCE.ueagle-atm4-firmware LICENCE.via_vt6656
%doc LICENSE.dib0700
/lib/firmware/brcm/brcmfmac43340-sdio.pov-tab-p1006w-data.txt
/lib/firmware/brcm/brcmfmac43455-sdio.MINIX-NEO*

%files extra -f nonfree.list
%defattr(0644,root,root,0755)
%doc LICENCE.Marvell LICENCE.agere LICENCE.atheros_firmware
%doc LICENCE.broadcom_bcm43xx LICENCE.chelsio_firmware LICENCE.i2400m
%doc LICENCE.OLPC LICENCE.phanfw
%doc LICENCE.ralink-firmware.txt LICENCE.rtlwifi_firmware.txt
%doc LICENCE.tda7706-firmware.txt LICENCE.ti-connectivity LICENCE.xc5000
%doc LICENCE.siano LICENSE.amd-ucode
/lib/firmware/silabs/LICENCE.wf200
/lib/firmware/qcom/NOTICE.txt
/lib/firmware/netronome/flower/*.nffw
/lib/firmware/nvidia
%dir /lib/firmware/qca
/lib/firmware/qca/crbtfw21.tlv
/lib/firmware/qca/crbtfw32.tlv
/lib/firmware/qca/crnv21.bin
/lib/firmware/qca/crnv32.bin
/lib/firmware/qca/crnv32u.bin

%files -n radeon-firmware -f radeon.list
%defattr(0644,root,root,0755)
%doc LICENSE.radeon

%files -n adreno-firmware -f adreno.list
%defattr(0644,root,root,0755)

%files -n iwlwifi-agn-ucode -f iwlwifi.list
%doc LICENCE.iwlwifi_firmware LICENCE.ibt_firmware
/lib/firmware/intel/ibt-19-32-4.ddc
/lib/firmware/intel/ibt-19-32-4.sfi
/lib/firmware/intel/ibt-0040-0041.ddc
/lib/firmware/intel/ibt-0040-0041.sfi
/lib/firmware/intel/ibt-0040-2120.ddc
/lib/firmware/intel/ibt-0040-2120.sfi
/lib/firmware/intel/ibt-0040-4150.ddc
/lib/firmware/intel/ibt-0040-4150.sfi
/lib/firmware/intel/ibt-1040-0041.ddc
/lib/firmware/intel/ibt-1040-0041.sfi
/lib/firmware/intel/ibt-1040-2120.ddc
/lib/firmware/intel/ibt-1040-2120.sfi
/lib/firmware/intel/ibt-1040-4150.ddc
/lib/firmware/intel/ibt-1040-4150.sfi

# This should be ifarch %{aarch64}, but since this is a noarch
# package, that can't be detected. So let's create a superfluous
# package on other arches rather than omitting an important
# package for aarch64
%files pinephone
%dir /lib/firmware
/lib/firmware/anx7688-fw.bin
/lib/firmware/hm5065-af.bin
/lib/firmware/hm5065-init.bin
/lib/firmware/ov5640_af.bin
%dir /lib/firmware/brcm
/lib/firmware/brcm/BCM20702A1.hcd
/lib/firmware/brcm/BCM4345C5.hcd
/lib/firmware/brcm/brcmfmac43362-sdio.txt
/lib/firmware/brcm/brcmfmac43456-sdio.bin
/lib/firmware/brcm/brcmfmac43456-sdio.txt
%dir /lib/firmware/rtl_bt
/lib/firmware/rtl_bt/rtl8723bs_config-pine64.bin
/lib/firmware/rtl_bt/rtl8723cs_xx_config.bin
/lib/firmware/rtl_bt/rtl8723cs_xx_fw.bin
%dir /lib/firmware/rtlwifi
/lib/firmware/rtlwifi/rtl8188eufw.bin
