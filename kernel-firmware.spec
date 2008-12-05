#
# This rpm is based on the git tree from:
# git.kernel.org/pub/scm/linux/kernel/git/dwmw2/linux-firmware-from-kernel.git
# version is date of the younger commit
#

Summary:	Linux kernel firmware files
Name:   	kernel-firmware
Version:	20080922
Release:	%manbo_mkrel 2
License:	GPLv2
Group:  	System/Kernel and hardware
URL:    	http://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned above, 
# by simply cloning it, doing a rm -rf linux-firmware-from-kernel/.git/ 
# and tar -cjvf kernel-firmware-version.tar.bz2 linux-firmware-from-kernel
Source0: 	kernel-firmware-%{version}.tar.bz2
Suggests:	kernel-firmware-extra
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:	noarch

%description
This package contains the GPL firmwares for in-kernel drivers.
It is shared by all kernels >= 2.6.27-rc1.

%prep
%setup -q -n linux-firmware-from-kernel

# don't include firmware without an acceptable open source license or
# without source available to be distributed on kernel-firmware-extra
rm -f korg/k1212.dsp # license unknown
rm -f ess/{maestro3_assp_kernel,maestro3_assp_minisrc}.fw # license unknown
rm -f yamaha/{ds1_ctrl,ds1_dsp,ds1e_ctrl}.fw # license unknown
rm -f tr_smctr.bin # specific license, see WHENCE
rm -f kaweth/new_code{,_fix}.bin kaweth/trigger_code{,_fix}.bin #license unknown
rm -f ttusb-budget/dspbootcode.bin # license unknown
rm -f keyspan/*.fw # specific license, see WHENCE
rm -f emi26/{bitstream,firmware,loader}.fw # specific license, see WHENCE
rm -f emi62/{bitstream,loader,midi,spdif}.fw # license unknown
rm -f ti_{3410,5052}.fw # GPLv2+, no source visible
rm -f whiteheat{,_loader{,_debug}}.fw # GPLv2, no source visible
rm -f intelliport2.bin # license unknown
rm -f cpia2/stv0672_vp4.bin # GPLv2+, no source visible
rm -f dabusb/firmware.fw dabusb/bitstream.bin # distributable license
rm -f vicam/firmware.fw # license unknown
rm -f edgeport/boot{,2}.fw edgeport/down{,2}.fw  GPLv2+, no source visible
rm -f edgeport/down3.bin # specific license, see WHENCE
rm -f sb16/*.csp # GPLv2+, no source visible
rm -f sun/cassini.bin # license unknown
rm -f atmsar11.fw # unknown

# remove empty directories
for dir in `find . -type d | sed -e 's|^\.||' -e 's|^/||'`; do
	rmdir -p --ignore-fail-on-non-empty $dir
done

# remove unwanted source files
rm -f dsp56k/bootstrap.asm keyspan_pda/*.S

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/lib/firmware
cp -avf * %{buildroot}/lib/firmware
rm -f %{buildroot}/lib/firmware/WHENCE

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc WHENCE
/lib/firmware/*
