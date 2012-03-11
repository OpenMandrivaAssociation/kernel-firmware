#
# This rpm is based on the git tree from:
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# version is date of the younger commit
#

Summary:	Linux kernel firmware files
Name:   	kernel-firmware
Version:	20120218
Release:	%mkrel 1
License:	GPLv2
Group:  	System/Kernel and hardware
URL:    	http://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned
# above, by simply cloning it, and  doing:
# git archive --prefix=linux-firmware-from-kernel/ origin/master | xz > linux-firmware-version.tar.xz
Source0: 	kernel-firmware-%{version}.tar.xz
Conflicts:	kernel-firmware-extra < 20110310-1
Obsoletes:	korg1212-firmware
Obsoletes:	maestro3-firmware
Obsoletes:	sb16-firmware
Obsoletes:	yamaha-firmware
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
