# -*- Mode: rpm-spec -*-

%define kernelversion	2
%define patchlevel	6
%define sublevel	27

# Package version
%define mnbrel		1

# Kernel Makefile extraversion is substituted by kpatch/kgit/kstable which
# can be:
#
#	0   (empty)
#	rc  (kpatch)
#	git (kgit)
#	stable release (kstable)
#
%define kpatch		rc3
%define kgit		6
%define kstable		0

### Nothing below this need to be changed !!

# When we are using a pre/rc patch, the tarball is a sublevel -1
# NOTE! Switch to manbo_mkrel when it's moved to main!
%if %kpatch
%define kversion        %{kernelversion}.%{patchlevel}.%{sublevel}
%define tar_ver         %{kernelversion}.%{patchlevel}.%(expr %{sublevel} - 1)
%define rpmrel		%mkrel 0.%{kpatch}.%{mnbrel}
%else
%if %kstable
%define kversion        %{kernelversion}.%{patchlevel}.%{sublevel}.%{kstable}
%else
%define kversion        %{kernelversion}.%{patchlevel}.%{sublevel}
%define rpmrel		%mkrel %{mnbrel}
%endif
%define tar_ver         %{kernelversion}.%{patchlevel}.%{sublevel}
%endif

# Disable useless debug rpms...
%define _enable_debug_packages 	%{nil}
%define debug_package 		%{nil}

Summary: 	Linux kernel firmware built for Mandriva kernels
Name:		kernel-firmware
Version: 	%{kversion}
Release:	%{rpmrel}
License: 	GPLv2
Group: 	 	System/Kernel and hardware
ExclusiveArch:	%{ix86} x86_64 sparc64
ExclusiveOS: 	Linux
URL:            http://www.kernel.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{_arch}-buildroot
BuildRequires: 	gcc module-init-tools >= 0.9.15

####################################################################
#
# Sources
#
### This is for full SRC RPM
Source0: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2
Source1: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/linux-%{tar_ver}.tar.bz2.sign

### Needed defconfigs (from kernel-linus)
Source2: i386-smp.config
Source3: x86_64-smp.config
Source4: sparc64-smp.config
####################################################################
#
# Patches

%if %kpatch
Patch1:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/testing/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}.bz2.sign
%endif
%if %kgit
Patch2:		ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-%{kgit}.bz2
Source11: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/snapshots/patch-%{kernelversion}.%{patchlevel}.%{sublevel}-%{kpatch}-%{kgit}.bz2.sign
%endif
%if %kstable
Patch1:   	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2
Source10: 	ftp://ftp.kernel.org/pub/linux/kernel/v%{kernelversion}.%{patchlevel}/patch-%{kversion}.bz2.sign
%endif

%description
This package contains the GPL firmwares for in-kernel drivers.
It is shared by all kernels >= 2.6.27-rc2.

#
# Prep
#

%prep
%setup -q -n linux-%{tar_ver}

%if %kpatch
%patch1 -p1
%endif
%if %kgit
%patch2 -p1
%endif
%if %kstable
%patch1 -p1
%endif

#
# Build
#
%build
cp %{_sourcedir}/%{_arch}-smp.config .config
%make firmware/


%install
install -d %{buildroot}
make INSTALL_MOD_PATH=%{buildroot} firmware_install
rm -rf %{buildroot}/{firmware,include,scripts,usr,Makefile}

%clean

%files
/lib/firmware/*
