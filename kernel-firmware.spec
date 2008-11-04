#
# This rpm is based on the git tree from:
# git.kernel.org/pub/scm/linux/kernel/git/dwmw2/linux-firmware-from-kernel.git
# version is date of the younger commit
#

Summary:	Linux kernel firmware files
Name:   	kernel-firmware
Version:	20080922
Release:	%manbo_mkrel 1
License:	GPLv2
Group:  	System/Kernel and hardware
URL:    	http://www.kernel.org/
Obsoletes:	korg1212-firmware maestro3-firmware sb16-firmware yamaha-firmware
# kernel-firmware tarball is generated from the git tree mentioned above, 
# by simply cloning it, doing a rm -rf linux-firmware-from-kernel/.git/ 
# and tar -cjvf kernel-firmware-version.tar.bz2 linux-firmware-from-kernel
Source0: 	kernel-firmware-%version.tar.bz2
BuildRoot:      %_tmppath/%name-buildroot
Buildarch:	noarch

%description
This package contains the GPL firmwares for in-kernel drivers.
It is shared by all kernels >= 2.6.27-rc1.

%prep
%setup -q -n linux-firmware-from-kernel

%install
rm -rf %buildroot
mkdir -p %buildroot/lib/firmware
cp -avf * %buildroot/lib/firmware

%clean
rm -rf %buildroot

%files
%defattr(0644,root,root,0755)
/lib/firmware/*
