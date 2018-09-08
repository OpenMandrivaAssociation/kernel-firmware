#
# This rpm is based on the git tree from:
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# version is date of the younger commit

# False positive -- some firmware bits are mistaken for host binaries
%define _binaries_in_noarch_packages_terminate_build 0

Summary:	Linux kernel firmware files
Name:   	kernel-firmware
Version:	20180903
Release:	2
License:	GPLv2
Group:  	System/Kernel and hardware
URL:    	http://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned
# above, by simply cloning it from
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# and  doing:
# git archive -o kernel-firmware-`date +%Y%m%d`.tar --prefix=kernel-firmware-`date +%Y%m%d`/ master ; xz -9e kernel-firmware-`date +%Y%m%d`.tar
Source0: 	kernel-firmware-%{version}.tar.xz
# http://ivtvdriver.org/index.php/Firmware
# Checked out Sat Nov 2 2013
Source1:	http://dl.ivtvdriver.org/ivtv/firmware/ivtv-firmware.tar.gz
# Adreno firmware, from OQ820 BSP 3.2
Source4:	adreno-fw-820BSP3.2.tar.xz
# Firmware for Hauppauge HVR-1975
# see http://www.hauppauge.com/site/support/linux.html
Source5:	https://s3.amazonaws.com/hauppauge/linux/linux-ubuntu-14-04-2.tar.xz
# Firmware for various DVB receivers
Source6:	https://github.com/OpenELEC/dvb-firmware/archive/master.tar.gz
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
URL:    	http://www.kernel.org/
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
Conflicts:      kernel-firmware-extra < 20130624-1
Conflicts:      kernel-firmware-nonfree < 20130624-1

%description -n iwlwifi-agn-ucode
This package contains all the iwlwifi wireless firmware files
supported by the iwlwifi kernel driver. That means all of:
iwlwifi-1xx/1000/2xxx/5xxx/6xxx*.ucode firmwares.

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

# Symlinks (not mentioned in WHENCE file)
echo '/lib/firmware/cxgb4/t4fw.bin' >>nonfree.list
echo '/lib/firmware/cxgb4/t5fw.bin' >>nonfree.list
echo '/lib/firmware/cxgb4/t6fw.bin' >>nonfree.list
echo '/lib/firmware/libertas/sd8688.bin' >>nonfree.list
echo '/lib/firmware/libertas/sd8688_helper.bin' >>nonfree.list
echo '/lib/firmware/rt3070.bin' >>nonfree.list
echo '/lib/firmware/rt3090.bin' >>nonfree.list

# Files not directly mentioned in WHENCE file (signatures, etc.)
echo '/lib/firmware/amd-ucode/microcode_amd.bin.asc' >>nonfree.list
echo '/lib/firmware/amd-ucode/microcode_amd_fam15h.bin.asc' >>nonfree.list
echo '/lib/firmware/amd-ucode/microcode_amd_fam16h.bin.asc' >>nonfree.list
echo '/lib/firmware/amd-ucode/microcode_amd_fam17h.bin.asc' >>nonfree.list
echo '/lib/firmware/s2250.fw' >>nonfree.list
echo '/lib/firmware/s2250_loader.fw' >>nonfree.list
echo '/lib/firmware/ti-connectivity/wl1271-nvs.bin' >>nonfree.list
echo '/lib/firmware/ti-connectivity/wl12xx-nvs.bin' >>nonfree.list
echo '/lib/firmware/ath10k/QCA988X/hw2.0/notice_ath10k_firmware-4.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw2.1/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw3.0/board-2.bin' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw3.0/notice_ath10k_firmware-4.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA988X/hw2.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA99X0/hw2.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9377/hw1.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA4019/hw1.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9887/hw1.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9888/hw2.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA9984/hw1.0/notice_ath10k_firmware-5.txt' >> nonfree.list
echo '/lib/firmware/ath10k/QCA6174/hw3.0/notice_ath10k_firmware-6.txt' >> nonfree.list
echo '/lib/firmware/qca/NOTICE.txt' >> nonfree.list

%install
mkdir -p %{buildroot}/lib/firmware
cp -avf * %{buildroot}/lib/firmware
rm -f %{buildroot}/lib/firmware/WHENCE %{buildroot}/lib/firmware/LICEN?E.*
rm -f %{buildroot}/lib/firmware/GPL-3
rm -f %{buildroot}/lib/firmware/GPL-2
rm -f %{buildroot}/lib/firmware/*.list
rm -f %{buildroot}/lib/firmware/check_whence.py

# Additional firmware
mkdir tmp
cd tmp
# ivtv
tar xf %{SOURCE1}
# This one is in linux-firmware git already
rm v4l-cx25840.fw
FW="`ls *.fw *.mpg`"
for i in $FW; do
    mv $i %{buildroot}/lib/firmware/
    echo "/lib/firmware/$i" >>../nonfree.list
done
cd ..

# Adreno
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{SOURCE4}
FW="`ls`"
for i in $FW; do
    mv $i %{buildroot}/lib/firmware/
    echo "/lib/firmware/$i" >>../adreno.list
done
cd ..

# Hauppauge
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{SOURCE5}
if [ -e %{buildroot}/lib/firmware/v4l-pvrusb2-160xxx-01.fw ]; then
	echo "pvrusb2-160xxx firmware has been merged upstream, please remove it here"
	exit 1
fi
if [ -e %{buildroot}/lib/firmware/NXP7164-2010-04-01.1.fw ]; then
	echo "NXP7164 firmware has been merged upstream, please remove it here"
	exit 1
fi
cp "Linux-Ubuntu-14-04-2/firmware/HVR 19x5/v4l-pvrusb2-160xxx-01.fw" %{buildroot}/lib/firmware/
cp "Linux-Ubuntu-14-04-2/firmware/HVR 22x5/NXP7164-2010-04-01.1.fw" %{buildroot}/lib/firmware/
cd ..
echo '/lib/firmware/v4l-pvrusb2-160xxx-01.fw' >>nonfree.list
echo '/lib/firmware/NXP7164-2010-04-01.1.fw' >>nonfree.list

# Assorted DVB
rm -rf tmp
mkdir tmp
cd tmp
tar xf %{SOURCE6}
cd dvb-firmware-master/firmware
# Already added upstream
rm -rf	go7007 \
	ttusb-budget \
	s2250.fw \
	NXP7164-2010-04-01.1.fw \
	dvb-fe-xc4000-1.4.1.fw \
	dvb-fe-xc5000-1.6.114.fw \
	dvb-fe-xc5000c-4.1.30.7.fw \
	dvb-usb-dib0700-1.20.fw \
	dvb-usb-it9135-01.fw \
	dvb-usb-it9135-02.fw \
	dvb-usb-terratec-h5-drxk.fw \
	lgs8g75.fw \
	s2250_loader.fw \
	sms1xxx-hcw-55xxx-dvbt-02.fw \
	sms1xxx-hcw-55xxx-isdbt-02.fw \
	sms1xxx-nova-a-dvbt-01.fw \
	sms1xxx-nova-b-dvbt-01.fw \
	sms1xxx-stellar-dvbt-01.fw \
	v4l-cx231xx-avcore-01.fw \
	v4l-cx23418-apu.fw \
	v4l-cx23418-cpu.fw \
	v4l-cx23418-dig.fw \
	v4l-cx2341x-dec.fw \
	v4l-cx2341x-enc.fw \
	v4l-cx23885-avcore-01.fw \
	v4l-cx25840.fw \
	v4l-pvrusb2-24xxx-01.fw \
	v4l-pvrusb2-29xxx-01.fw \
	as102_data1_st.hex \
	as102_data2_st.hex \
	tlg2300_firmware.bin \
	cmmb_vega_12mhz.inp \
	cmmb_venice_12mhz.inp \
	dvb_nova_12mhz.inp \
	dvb_nova_12mhz_b0.inp \
	isdbt_nova_12mhz.inp \
	isdbt_nova_12mhz_b0.inp \
	isdbt_rio.inp \
	tdmb_nova_12mhz.inp
for i in *.fw* *.bin *.inp *.mc; do
	if [ -e %{buildroot}/lib/firmware/$i ]; then
		echo "******* Please remove $i from DVB firmware, it's upstream *******"
		exit 1
	fi
	cp $i %{buildroot}/lib/firmware/
	echo "/lib/firmware/$i" >>../../../nonfree.list
done
cd ../../..

# Intel versioned files have the same license as their unlicensed counterparts
echo '/lib/firmware/intel/dsp_fw_kbl.bin' >>nonfree.list
echo '/lib/firmware/intel/dsp_fw_release.bin' >>nonfree.list
echo '/lib/firmware/intel/dsp_fw_bxtn.bin' >>nonfree.list
echo '/lib/firmware/intel/dsp_fw_glk.bin' >>nonfree.list
echo '/lib/firmware/qat_mmp.bin' >>nonfree.list
echo '/lib/firmware/intel/ipu3-fw.bin' >>nonfree.list

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

%files extra -f nonfree.list
%defattr(0644,root,root,0755)
%doc LICENCE.Marvell LICENCE.agere LICENCE.atheros_firmware
%doc LICENCE.broadcom_bcm43xx LICENCE.chelsio_firmware LICENCE.i2400m
%doc LICENCE.OLPC LICENCE.phanfw
%doc LICENCE.ralink-firmware.txt LICENCE.rtlwifi_firmware.txt
%doc LICENCE.tda7706-firmware.txt LICENCE.ti-connectivity LICENCE.xc5000
%doc LICENCE.siano LICENSE.amd-ucode
/lib/firmware/qcom/NOTICE.txt
/lib/firmware/netronome

%files -n radeon-firmware -f radeon.list
%defattr(0644,root,root,0755)
%doc LICENSE.radeon

%files -n adreno-firmware -f adreno.list
%defattr(0644,root,root,0755)

%files -n iwlwifi-agn-ucode -f iwlwifi.list
%doc LICENCE.iwlwifi_firmware LICENCE.ibt_firmware
