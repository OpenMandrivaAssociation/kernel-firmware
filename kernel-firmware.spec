#
# This rpm is based on the git tree from:
# git.kernel.org/pub/scm/linux/kernel/git/dwmw2/linux-firmware-from-kernel.git
# version is date of the younger commit
#

Summary:	Linux kernel firmware files
Name:   	kernel-firmware
Version:	20090111
Release:	%manbo_mkrel 2
License:	GPLv2
Group:  	System/Kernel and hardware
URL:    	http://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned above, 
# by simply cloning it, doing a rm -rf linux-firmware-from-kernel/.git/ 
# and tar -cjvf kernel-firmware-version.tar.bz2 linux-firmware-from-kernel
Source0: 	kernel-firmware-%{version}.tar.bz2
Conflicts:	kernel-firmware-extra <= 20090212-1mnb2
Suggests:	kernel-firmware-extra
BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildArch:	noarch

%description
This package contains the firmware for in-kernel drivers that was previously
included in the kernel. It is shared by all kernels >= 2.6.27-rc1.

%prep
%setup -q -n linux-firmware-from-kernel

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
