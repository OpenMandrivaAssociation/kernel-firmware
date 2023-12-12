# False positive -- some firmware bits are mistaken for host binaries
%define _binaries_in_noarch_packages_terminate_build 0

%global _firmwaredir %{_prefix}/lib/firmware

# Needed if you want to be compatible with kernels < 5.15
# (support for compression was added then)
%bcond_without compress

Summary:	Linux kernel firmware files
Name:		kernel-firmware
Version:	20231212
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
Source1:	linux-firmware-pine64-20230817.tar.zst
# Adreno firmware, from OQ820 BSP 3.2
Source2:	adreno-fw-820BSP3.2.tar.xz
# Firmware for Hauppauge HVR-1975
# see http://www.hauppauge.com/site/support/linux.html
Source3:	https://s3.amazonaws.com/hauppauge/linux/linux-ubuntu-14-04-2.tar.xz
# Firmware for various DVB receivers
Source4:	https://github.com/OpenELEC/dvb-firmware/archive/master/dvb-firmware-%{version}.tar.gz
# ARM Mali G610 GPU, e.g. Rock 5B board
# Available in a slew of versions...
# https://gitlab.com/rk3588_linux/linux/libmali/-/raw/master/firmware/g610/mali_csffw.bin
# https://launchpad.net/~liujianfeng1994/+archive/ubuntu/panfork-mesa/+sourcefiles/mali-g610-firmware/1.0.2/mali-g610-firmware_1.0.2.tar.gz
# https://gitlab.com/firefly-linux/external/libmali/-/raw/firefly/firmware/g610/mali_csffw.bin
# https://github.com/JeffyCN/mirrors/raw/libmali/firmware/g610/mali_csffw.bin
# The JeffyCN version seems to be the latest (g21); the kernel driver announcement
# https://lwn.net/Articles/953784/ mentiones the firefly version.
Source5:	https://github.com/JeffyCN/mirrors/raw/libmali/firmware/g610/mali_csffw.bin
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
BuildRequires:	rdfind

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
Url:		http://ati.amd.com/
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
Url:		http://nvidia.com/

%description -n nvidia-firmware
Firmware files needed to use NVIDIA GPUs, even when using the Open
Source Nouveau driver

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

%package mellanox
Summary:	Firmware files needed to drive Mellanox network cards
Group:		System/Kernel and hardware

%description mellanox
Firmware files needed to drive Mellanox network cards

Netronome cards are ultra high end server equipment unlikely
to show up in consumer grade hardware. If you don't know what
it is, you don't need to install this package.

%package netronome
Summary:	Firmware files needed to drive Netronome network cards
Group:		System/Kernel and hardware

%description netronome
Firmware files needed to drive Netronome network cards

Netronome cards are ultra high end server equipment unlikely
to show up in consumer grade hardware. If you don't know what
it is, you don't need to install this package.

%prep
%autosetup -p1
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
rm brcm/brcmfmac43362-sdio.bin \
	brcm/brcmfmac43455-sdio.bin \
	brcm/brcmfmac43455-sdio.clm_blob \
	brcm/brcmfmac43455-sdio.pine64,pinephone-pro.txt \
	rtlwifi/rtl8188eufw.bin \
	rt2870.bin
# Duplicate from wireless-regdb
rm regulatory.db regulatory.db.p7s
rmdir rtlwifi
for i in *.bin brcm/* rtl_bt/*; do
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
rm a300_pfp.fw \
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

# Mali
if [ -e %{buildroot}%{_firmwaredir}/arm/mali/arch10.8/mali_csffw.bin ]; then
	echo "Mali G610 firmware has been added upstream, drop it"
	obsolete=$((obsolete+1))
else
	mkdir -p %{buildroot}%{_firmwaredir}/arm/mali/arch10.8
	cp -f %{S:5} %{buildroot}%{_firmwaredir}/arm/mali/arch10.8/
fi

if [ "$obsolete" -gt 0 ]; then
	echo "Some files being added manually have gone upstream"
	echo "and need to be removed."
	echo "Search the log for '====='"
	exit 1
fi

%files
%defattr(0644,root,root,0755)
%doc GPL-3 LICENCE.ene_firmware LICENCE.myri10ge_firmware
%doc LICENCE.qla2xxx LICENCE.ueagle-atm4-firmware LICENCE.via_vt6656
%doc LICENSE.dib0700
%{_firmwaredir}/atusb
%{_firmwaredir}/av7110
%{_firmwaredir}/brcm
%{_firmwaredir}/cis
%{_firmwaredir}/cypress
%{_firmwaredir}/dsp56k
%{_firmwaredir}/isci
%{_firmwaredir}/keyspan_pda
%{_firmwaredir}/r128
%{_firmwaredir}/usbdux_firmware.bin*
%{_firmwaredir}/usbduxfast_firmware.bin*
%{_firmwaredir}/usbduxsigma_firmware.bin*

%files extra
%defattr(0644,root,root,0755)
%doc LICENCE.Marvell LICENCE.agere LICENCE.atheros_firmware
%doc LICENCE.broadcom_bcm43xx LICENCE.chelsio_firmware
%doc LICENCE.OLPC LICENCE.phanfw
%doc LICENCE.ralink-firmware.txt LICENCE.rtlwifi_firmware.txt
%doc LICENCE.ti-connectivity LICENCE.xc5000
%doc LICENCE.siano LICENSE.amd-ucode
%{_firmwaredir}/3com
%{_firmwaredir}/NXP7164*
%{_firmwaredir}/RTL8192E
%{_firmwaredir}/acenic
%{_firmwaredir}/adaptec
%{_firmwaredir}/advansys
%{_firmwaredir}/af9005.fw*
%{_firmwaredir}/agere*
%{_firmwaredir}/airoha
%{_firmwaredir}/amd-ucode
%{_firmwaredir}/amd
%{_firmwaredir}/amdtee
%{_firmwaredir}/amlogic
%{_firmwaredir}/amphion
%{_firmwaredir}/ar3k
%{_firmwaredir}/ar5523.bin*
%{_firmwaredir}/ar7010*.fw*
%{_firmwaredir}/ar9170*.fw*
%{_firmwaredir}/ar9271.fw*
%{_firmwaredir}/as102_data*_st.hex*
%{_firmwaredir}/ath10k
%{_firmwaredir}/ath11k
%{_firmwaredir}/ath3k-1.fw*
%{_firmwaredir}/ath6k
%{_firmwaredir}/ath9k_htc
%{_firmwaredir}/atmel
%{_firmwaredir}/bnx2
%{_firmwaredir}/bnx2x
%{_firmwaredir}/bootcode.bin*
%{_firmwaredir}/brcm
%{_firmwaredir}/cadence
%{_firmwaredir}/carl9170-1.fw*
%{_firmwaredir}/cavium
%{_firmwaredir}/cbfw*.bin*
%{_firmwaredir}/cirrus
%{_firmwaredir}/cmmb*.inp*
%{_firmwaredir}/cnm
%{_firmwaredir}/cpia2
%{_firmwaredir}/ct2fw*.bin*
%{_firmwaredir}/ctefx.bin*
%{_firmwaredir}/ctfw-*.bin*
%{_firmwaredir}/ctspeq.bin*
%{_firmwaredir}/cxgb3
%{_firmwaredir}/cxgb4
%{_firmwaredir}/dabusb
%{_firmwaredir}/dpaa2
%{_firmwaredir}/drxd-*.fw*
%{_firmwaredir}/drxk_a3.mc*
%{_firmwaredir}/dspbootcode.bin*
%{_firmwaredir}/dvb*.fw*
%{_firmwaredir}/dvb_nova_12mhz*.inp*
%{_firmwaredir}/dvb_rio.inp*
%{_firmwaredir}/e100
%{_firmwaredir}/edgeport
%{_firmwaredir}/emi26
%{_firmwaredir}/emi62
%{_firmwaredir}/ene-ub6250
%{_firmwaredir}/ess
%{_firmwaredir}/f2255usb.bin*
%{_firmwaredir}/firmware_1900.fw*
%{_firmwaredir}/go7007
%{_firmwaredir}/hfi1_*.fw*
%{_firmwaredir}/hm5065*.bin*
%{_firmwaredir}/htc_7010.fw*
%{_firmwaredir}/htc_9271.fw*
%{_firmwaredir}/i915
%{_firmwaredir}/imx
%{_firmwaredir}/inside-secure
%dir %{_firmwaredir}/intel
%{_firmwaredir}/intel/IntcSST2.bin*
%{_firmwaredir}/intel/dsp_*.bin*
%{_firmwaredir}/intel/fw_*.bin*
%{_firmwaredir}/intel/ice
%{_firmwaredir}/intel/irci*
%{_firmwaredir}/isdbt_*.inp*
%{_firmwaredir}/ixp4xx
%{_firmwaredir}/kaweth
%{_firmwaredir}/keyspan
%{_firmwaredir}/korg
%{_firmwaredir}/lbtf_usb.bin*
%{_firmwaredir}/lgs8g75.fw*
%{_firmwaredir}/libertas
%{_firmwaredir}/liquidio
%{_firmwaredir}/lt9611uxc_fw.bin*
%{_firmwaredir}/matrox
%{_firmwaredir}/mediatek
%{_firmwaredir}/meson
%{_firmwaredir}/microchip
%{_firmwaredir}/moxa
%{_firmwaredir}/mrvl
%{_firmwaredir}/mt7601u.bin*
%{_firmwaredir}/mt7650.bin*
%{_firmwaredir}/mt7662.bin*
%{_firmwaredir}/mt7662_rom_patch.bin*
%{_firmwaredir}/mts_cdma.fw*
%{_firmwaredir}/mts_edge.fw*
%{_firmwaredir}/mts_gsm.fw*
%{_firmwaredir}/mts_mt9234mu.fw*
%{_firmwaredir}/mts_mt9234zba.fw*
%{_firmwaredir}/mwl8k
%{_firmwaredir}/mwlwifi
%{_firmwaredir}/myri10ge*.dat*
%{_firmwaredir}/myricom
%{_firmwaredir}/ngene_15.fw*
%{_firmwaredir}/ngene_16.fw*
%{_firmwaredir}/ngene_17.fw*
%{_firmwaredir}/ngene_18.fw*
%{_firmwaredir}/nxp
%{_firmwaredir}/ositech
%{_firmwaredir}/ov5640_af.bin*
%{_firmwaredir}/phanfw.bin*
%{_firmwaredir}/qat_895xcc.bin*
%{_firmwaredir}/qat_895xcc_mmp.bin*
%{_firmwaredir}/qat_c3xxx.bin*
%{_firmwaredir}/qat_c3xxx_mmp.bin*
%{_firmwaredir}/qat_c62x.bin*
%{_firmwaredir}/qat_c62x_mmp.bin*
%{_firmwaredir}/qat_4xxx.bin.xz
%{_firmwaredir}/qat_4xxx_mmp.bin.xz
%{_firmwaredir}/qca
%{_firmwaredir}/qed
%{_firmwaredir}/ql2100_fw.bin*
%{_firmwaredir}/ql2200_fw.bin*
%{_firmwaredir}/ql2300_fw.bin*
%{_firmwaredir}/ql2322_fw.bin*
%{_firmwaredir}/ql2400_fw.bin*
%{_firmwaredir}/ql2500_fw.bin*
%{_firmwaredir}/qlogic
%{_firmwaredir}/r8a779x_usb3_v1.dlmem*
%{_firmwaredir}/r8a779x_usb3_v2.dlmem*
%{_firmwaredir}/r8a779x_usb3_v3.dlmem*
%{_firmwaredir}/rockchip
%{_firmwaredir}/rp2.fw*
%{_firmwaredir}/rsi
%{_firmwaredir}/rsi_91x.fw*
%{_firmwaredir}/rt2561.bin*
%{_firmwaredir}/rt2561s.bin*
%{_firmwaredir}/rt2661.bin*
%{_firmwaredir}/rt2860.bin*
%{_firmwaredir}/rt2870.bin*
%{_firmwaredir}/rt3070.bin*
%{_firmwaredir}/rt3071.bin*
%{_firmwaredir}/rt3090.bin*
%{_firmwaredir}/rt3290.bin*
%{_firmwaredir}/rt73.bin*
%{_firmwaredir}/rtl_bt
%{_firmwaredir}/rtl_nic
%{_firmwaredir}/rtlwifi
%{_firmwaredir}/rtw88
%{_firmwaredir}/rtw89
%{_firmwaredir}/qat_mmp.bin*
%{_firmwaredir}/s2250.fw*
%{_firmwaredir}/s2250_loader.fw*
%{_firmwaredir}/s5p-mfc-v6-v2.fw*
%{_firmwaredir}/s5p-mfc-v6.fw*
%{_firmwaredir}/s5p-mfc-v7.fw*
%{_firmwaredir}/s5p-mfc-v8.fw*
%{_firmwaredir}/s5p-mfc-v12.fw*
%{_firmwaredir}/s5p-mfc.fw*
%{_firmwaredir}/sb16
%{_firmwaredir}/sdd_sagrad_1091_1098.bin*
%{_firmwaredir}/slicoss
%{_firmwaredir}/sms1xxx-hcw-114xxx-cmmb-01.fw*
%{_firmwaredir}/sms1xxx-hcw-55xxx-dvbt-01.fw*
%{_firmwaredir}/sms1xxx-hcw-55xxx-dvbt-02.fw*
%{_firmwaredir}/sms1xxx-hcw-55xxx-dvbt-03.fw*
%{_firmwaredir}/sms1xxx-hcw-55xxx-isdbt-02.fw*
%{_firmwaredir}/sms1xxx-hcw-55xxx-isdbt-03.fw*
%{_firmwaredir}/sms1xxx-nova-a-dvbt-01.fw*
%{_firmwaredir}/sms1xxx-nova-b-dvbt-01.fw*
%{_firmwaredir}/sms1xxx-stellar-dvbt-01.fw*
%{_firmwaredir}/sun
%{_firmwaredir}/sxg
%{_firmwaredir}/tdmb_nova_12mhz.inp*
%{_firmwaredir}/tehuti
%{_firmwaredir}/ti-connectivity
%{_firmwaredir}/ti-keystone
%{_firmwaredir}/ti
%{_firmwaredir}/ti_3410.fw*
%{_firmwaredir}/ti_5052.fw*
%{_firmwaredir}/tigon
%{_firmwaredir}/tlg2300_firmware.bin*
%{_firmwaredir}/ttusb-budget
%{_firmwaredir}/ueagle-atm
%{_firmwaredir}/v4l-cx231xx-avcore-01.fw*
%{_firmwaredir}/v4l-cx23418-apu.fw*
%{_firmwaredir}/v4l-cx23418-cpu.fw*
%{_firmwaredir}/v4l-cx23418-dig.fw*
%{_firmwaredir}/v4l-cx2341x-dec.fw*
%{_firmwaredir}/v4l-cx2341x-enc.fw*
%{_firmwaredir}/v4l-cx2341x-init.mpg*
%{_firmwaredir}/v4l-cx23885-avcore-01.fw*
%{_firmwaredir}/v4l-cx23885-enc.fw*
%{_firmwaredir}/v4l-cx25840.fw*
%{_firmwaredir}/v4l-pvrusb2-160xxx-01.fw*
%{_firmwaredir}/v4l-pvrusb2-24xxx-01.fw*
%{_firmwaredir}/v4l-pvrusb2-29xxx-01.fw*
%{_firmwaredir}/v4l-pvrusb2-73xxx-01.fw*
%{_firmwaredir}/vicam
%{_firmwaredir}/vntwusb.fw*
%{_firmwaredir}/vpu_d.bin*
%{_firmwaredir}/vpu_p.bin*
%{_firmwaredir}/vxge
%{_firmwaredir}/wfx
%{_firmwaredir}/whiteheat.fw*
%{_firmwaredir}/whiteheat_loader.fw*
%{_firmwaredir}/wil6210.*
%{_firmwaredir}/wsm_22.bin*
%{_firmwaredir}/xc3028-v24.fw*
%{_firmwaredir}/xc3028-v27.fw*
%{_firmwaredir}/xc3028L-v36.fw*
%{_firmwaredir}/xc4000-1.4.fw*
%{_firmwaredir}/yam
%{_firmwaredir}/yamaha

%files -n mali-g610-firmware
%{_firmwaredir}/arm/mali/arch10.8/mali_csffw.bin

%files -n firmware-powervr
%{_firmwaredir}/powervr

%files -n radeon-firmware
%defattr(0644,root,root,0755)
%license LICENSE.radeon
%{_firmwaredir}/amdgpu
%{_firmwaredir}/radeon

%files -n nvidia-firmware
%{_firmwaredir}/nvidia

%files -n adreno-firmware
%defattr(0644,root,root,0755)
%{_firmwaredir}/a300_pfp.fw.xz
%{_firmwaredir}/a300_pm4.fw.xz
%{_firmwaredir}/qcom

%files -n iwlwifi-agn-ucode
%doc LICENCE.iwlwifi_firmware LICENCE.ibt_firmware
%{_firmwaredir}/iwlwifi-100-5.ucode.xz
%{_firmwaredir}/iwlwifi-1000-5.ucode.xz
%{_firmwaredir}/iwlwifi-105-6.ucode.xz
%{_firmwaredir}/iwlwifi-135-6.ucode.xz
%{_firmwaredir}/iwlwifi-2000-6.ucode.xz
%{_firmwaredir}/iwlwifi-2030-6.ucode.xz
%{_firmwaredir}/iwlwifi-3160-17.ucode.xz
%{_firmwaredir}/iwlwifi-3168-29.ucode.xz
%{_firmwaredir}/iwlwifi-3945-2.ucode.xz
%{_firmwaredir}/iwlwifi-4965-2.ucode.xz
%{_firmwaredir}/iwlwifi-5000-5.ucode.xz
%{_firmwaredir}/iwlwifi-5150-2.ucode.xz
%{_firmwaredir}/iwlwifi-6000-4.ucode.xz
%{_firmwaredir}/iwlwifi-6000g2a-6.ucode.xz
%{_firmwaredir}/iwlwifi-6000g2b-6.ucode.xz
%{_firmwaredir}/iwlwifi-6050-5.ucode.xz
%{_firmwaredir}/iwlwifi-7260-17.ucode.xz
%{_firmwaredir}/iwlwifi-7265-17.ucode.xz
%{_firmwaredir}/iwlwifi-7265D-29.ucode.xz
%{_firmwaredir}/iwlwifi-8000C-36.ucode.xz
%{_firmwaredir}/iwlwifi-8265-36.ucode.xz
%{_firmwaredir}/iwlwifi-9000-pu-b0-jf-b0-46.ucode.xz
%{_firmwaredir}/iwlwifi-9260-th-b0-jf-b0-46.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-hr-b0-74.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-jf-b0-74.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-hr-b0-74.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-jf-b0-74.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-hr-b0-74.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-jf-b0-74.ucode.xz
%{_firmwaredir}/iwlwifi-cc-a0-74.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-74.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0.pnvm.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-74.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0.pnvm.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-74.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-jf-b0-74.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-74.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0.pnvm.xz
%{_firmwaredir}/iwlwifi-Qu-b0-hr-b0-77.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-jf-b0-77.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-hr-b0-77.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-jf-b0-77.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-hr-b0-77.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-jf-b0-77.ucode.xz
%{_firmwaredir}/iwlwifi-cc-a0-77.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-77.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-77.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-77.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-jf-b0-77.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-77.ucode.xz
%{_firmwaredir}/iwlwifi-gl-c0-fm-c0-83.ucode.xz
%{_firmwaredir}/iwlwifi-gl-c0-fm-c0.pnvm.xz
%{_firmwaredir}/iwlwifi-ma-b0-gf-a0-83.ucode.xz
%{_firmwaredir}/iwlwifi-ma-b0-gf-a0.pnvm.xz
%{_firmwaredir}/iwlwifi-ma-b0-gf4-a0-83.ucode.xz
%{_firmwaredir}/iwlwifi-ma-b0-gf4-a0.pnvm.xz
%{_firmwaredir}/iwlwifi-ma-b0-hr-b0-83.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-84.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-84.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-84.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-84.ucode.xz
%{_firmwaredir}/intel/ibt-0040-0041.ddc.xz
%{_firmwaredir}/intel/ibt-0040-0041.sfi.xz
%{_firmwaredir}/intel/ibt-0040-1020.ddc.xz
%{_firmwaredir}/intel/ibt-0040-1020.sfi.xz
%{_firmwaredir}/intel/ibt-0040-1050.ddc.xz
%{_firmwaredir}/intel/ibt-0040-1050.sfi.xz
%{_firmwaredir}/intel/ibt-0040-2120.ddc.xz
%{_firmwaredir}/intel/ibt-0040-2120.sfi.xz
%{_firmwaredir}/intel/ibt-0040-4150.ddc.xz
%{_firmwaredir}/intel/ibt-0040-4150.sfi.xz
%{_firmwaredir}/intel/ibt-0041-0041.ddc.xz
%{_firmwaredir}/intel/ibt-0041-0041.sfi.xz
%{_firmwaredir}/intel/ibt-0180-0041.ddc.xz
%{_firmwaredir}/intel/ibt-0180-0041.sfi.xz
%{_firmwaredir}/intel/ibt-0180-1050.ddc.xz
%{_firmwaredir}/intel/ibt-0180-1050.sfi.xz
%{_firmwaredir}/intel/ibt-0180-4150.ddc.xz
%{_firmwaredir}/intel/ibt-0180-4150.sfi.xz
%{_firmwaredir}/intel/ibt-0291-0291.ddc.xz
%{_firmwaredir}/intel/ibt-0291-0291.sfi.xz
%{_firmwaredir}/intel/ibt-1040-1050.ddc.xz
%{_firmwaredir}/intel/ibt-1040-1050.sfi.xz
%{_firmwaredir}/intel/ibt-1040-0041.ddc.xz
%{_firmwaredir}/intel/ibt-1040-0041.sfi.xz
%{_firmwaredir}/intel/ibt-1040-1020.ddc.xz
%{_firmwaredir}/intel/ibt-1040-1020.sfi.xz
%{_firmwaredir}/intel/ibt-1040-2120.ddc.xz
%{_firmwaredir}/intel/ibt-1040-2120.sfi.xz
%{_firmwaredir}/intel/ibt-1040-4150.ddc.xz
%{_firmwaredir}/intel/ibt-1040-4150.sfi.xz
%{_firmwaredir}/intel/ibt-11-5.ddc.xz
%{_firmwaredir}/intel/ibt-11-5.sfi.xz
%{_firmwaredir}/intel/ibt-12-16.ddc.xz
%{_firmwaredir}/intel/ibt-12-16.sfi.xz
%{_firmwaredir}/intel/ibt-17-0-1.ddc.xz
%{_firmwaredir}/intel/ibt-17-0-1.sfi.xz
%{_firmwaredir}/intel/ibt-17-1.ddc.xz
%{_firmwaredir}/intel/ibt-17-1.sfi.xz
%{_firmwaredir}/intel/ibt-17-16-1.ddc.xz
%{_firmwaredir}/intel/ibt-17-16-1.sfi.xz
%{_firmwaredir}/intel/ibt-17-2.ddc.xz
%{_firmwaredir}/intel/ibt-17-2.sfi.xz
%{_firmwaredir}/intel/ibt-18-0-1.ddc.xz
%{_firmwaredir}/intel/ibt-18-0-1.sfi.xz
%{_firmwaredir}/intel/ibt-18-1.ddc.xz
%{_firmwaredir}/intel/ibt-18-1.sfi.xz
%{_firmwaredir}/intel/ibt-18-16-1.ddc.xz
%{_firmwaredir}/intel/ibt-18-16-1.sfi.xz
%{_firmwaredir}/intel/ibt-18-2.ddc.xz
%{_firmwaredir}/intel/ibt-18-2.sfi.xz
%{_firmwaredir}/intel/ibt-19-0-0.ddc.xz
%{_firmwaredir}/intel/ibt-19-0-0.sfi.xz
%{_firmwaredir}/intel/ibt-19-0-1.ddc.xz
%{_firmwaredir}/intel/ibt-19-0-1.sfi.xz
%{_firmwaredir}/intel/ibt-19-0-4.ddc.xz
%{_firmwaredir}/intel/ibt-19-0-4.sfi.xz
%{_firmwaredir}/intel/ibt-19-16-4.ddc.xz
%{_firmwaredir}/intel/ibt-19-16-4.sfi.xz
%{_firmwaredir}/intel/ibt-19-240-1.ddc.xz
%{_firmwaredir}/intel/ibt-19-240-1.sfi.xz
%{_firmwaredir}/intel/ibt-19-240-4.ddc.xz
%{_firmwaredir}/intel/ibt-19-240-4.sfi.xz
%{_firmwaredir}/intel/ibt-19-32-0.ddc.xz
%{_firmwaredir}/intel/ibt-19-32-0.sfi.xz
%{_firmwaredir}/intel/ibt-19-32-1.ddc.xz
%{_firmwaredir}/intel/ibt-19-32-1.sfi.xz
%{_firmwaredir}/intel/ibt-19-32-4.ddc.xz
%{_firmwaredir}/intel/ibt-19-32-4.sfi.xz
%{_firmwaredir}/intel/ibt-20-0-3.ddc.xz
%{_firmwaredir}/intel/ibt-20-0-3.sfi.xz
%{_firmwaredir}/intel/ibt-20-1-3.ddc.xz
%{_firmwaredir}/intel/ibt-20-1-3.sfi.xz
%{_firmwaredir}/intel/ibt-20-1-4.ddc.xz
%{_firmwaredir}/intel/ibt-20-1-4.sfi.xz
%{_firmwaredir}/intel/ibt-19-0-3.ddc.xz
%{_firmwaredir}/intel/ibt-19-0-3.sfi.xz
%{_firmwaredir}/intel/ibt-hw-37.7.10-fw-1.0.1.2d.d.bseq.xz
%{_firmwaredir}/intel/ibt-hw-37.7.10-fw-1.0.2.3.d.bseq.xz
%{_firmwaredir}/intel/ibt-hw-37.7.10-fw-1.80.1.2d.d.bseq.xz
%{_firmwaredir}/intel/ibt-hw-37.7.10-fw-1.80.2.3.d.bseq.xz
%{_firmwaredir}/intel/ibt-hw-37.7.bseq.xz
%{_firmwaredir}/intel/ibt-hw-37.8.10-fw-1.10.2.27.d.bseq.xz
%{_firmwaredir}/intel/ibt-hw-37.8.10-fw-1.10.3.11.e.bseq.xz
%{_firmwaredir}/intel/ibt-hw-37.8.10-fw-22.50.19.14.f.bseq.xz
%{_firmwaredir}/intel/ibt-hw-37.8.bseq.xz
%{_firmwaredir}/intel/ipu3-fw.bin.xz
%{_firmwaredir}/intel/avs/apl/dsp_basefw.bin.xz
%{_firmwaredir}/intel/avs/cnl/dsp_basefw.bin.xz
%{_firmwaredir}/intel/avs/skl/dsp_basefw.bin.xz
%{_firmwaredir}/intel/avs/skl/dsp_mod_7CAD0808-AB10-CD23-EF45-12AB34CD56EF.bin.xz
%{_firmwaredir}/intel/catpt/bdw/dsp_basefw.bin.xz
%{_firmwaredir}/iwlwifi-8000C-34.ucode.xz
%{_firmwaredir}/iwlwifi-8265-34.ucode.xz
%{_firmwaredir}/iwlwifi-9000-pu-b0-jf-b0-34.ucode.xz
%{_firmwaredir}/iwlwifi-9000-pu-b0-jf-b0-38.ucode.xz
%{_firmwaredir}/iwlwifi-9260-th-b0-jf-b0-34.ucode.xz
%{_firmwaredir}/iwlwifi-9260-th-b0-jf-b0-38.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-hr-b0-50.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-hr-b0-59.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-hr-b0-66.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-hr-b0-72.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-hr-b0-73.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-jf-b0-50.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-jf-b0-59.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-jf-b0-66.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-jf-b0-72.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-b0-jf-b0-73.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-hr-b0-50.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-hr-b0-59.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-hr-b0-66.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-hr-b0-72.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-hr-b0-73.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-jf-b0-50.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-jf-b0-59.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-jf-b0-66.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-jf-b0-72.ucode.xz
%{_firmwaredir}/iwlwifi-Qu-c0-jf-b0-73.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-hr-b0-50.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-hr-b0-59.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-hr-b0-66.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-hr-b0-72.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-hr-b0-73.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-jf-b0-50.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-jf-b0-59.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-jf-b0-66.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-jf-b0-72.ucode.xz
%{_firmwaredir}/iwlwifi-QuZ-a0-jf-b0-73.ucode.xz
%{_firmwaredir}/iwlwifi-cc-a0-50.ucode.xz
%{_firmwaredir}/iwlwifi-cc-a0-59.ucode.xz
%{_firmwaredir}/iwlwifi-cc-a0-66.ucode.xz
%{_firmwaredir}/iwlwifi-cc-a0-72.ucode.xz
%{_firmwaredir}/iwlwifi-cc-a0-73.ucode.xz
%{_firmwaredir}/iwlwifi-gl-c0-fm-c0-86.ucode.xz
%{_firmwaredir}/iwlwifi-ma-b0-gf-a0-86.ucode.xz
%{_firmwaredir}/iwlwifi-ma-b0-gf4-a0-86.ucode.xz
%{_firmwaredir}/iwlwifi-ma-b0-hr-b0-86.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-83.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-86.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-72.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-73.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-78.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-79.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-86.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-72.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-73.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-78.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-79.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-86.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-72.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-73.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-79.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-jf-b0-72.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-jf-b0-73.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-59.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-66.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-72.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-73.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-78.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-79.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-86.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-81.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf-a0-83.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-81.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-gf4-a0-83.ucode.xz
%{_firmwaredir}/iwlwifi-so-a0-hr-b0-81.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-81.ucode.xz
%{_firmwaredir}/iwlwifi-ty-a0-gf-a0-83.ucode.xz

%files mellanox
%{_firmwaredir}/mellanox

%files netronome
%license LICENCE.Netronome
%{_firmwaredir}/netronome

# This should be ifarch %{aarch64}, but since this is a noarch
# package, that can't be detected. So let's create a superfluous
# package on other arches rather than omitting an important
# package for aarch64
%files pinephone
%dir %{_firmwaredir}
%{_firmwaredir}/anx7688-fw.bin.xz
%{_firmwaredir}/hm5065-af.bin.xz
%{_firmwaredir}/hm5065-init.bin.xz
%{_firmwaredir}/ov5640_af.bin.xz
%dir %{_firmwaredir}/brcm
%{_firmwaredir}/brcm/BCM20702A1.hcd.xz
%{_firmwaredir}/brcm/BCM4345C5.hcd.xz
%{_firmwaredir}/brcm/brcmfmac43362-sdio.txt.xz
%{_firmwaredir}/brcm/brcmfmac43456-sdio.bin.xz
%{_firmwaredir}/brcm/brcmfmac43456-sdio.txt.xz
%dir %{_firmwaredir}/rtl_bt
%{_firmwaredir}/rtl_bt/rtl8723bs_config-pine64.bin.xz
%{_firmwaredir}/rtl_bt/rtl8723cs_xx_config.bin.xz
%{_firmwaredir}/rtl_bt/rtl8723cs_xx_fw.bin.xz
%dir %{_firmwaredir}/rtlwifi
%{_firmwaredir}/rtlwifi/rtl8188eufw.bin.xz
