#
# This rpm is based on the git tree from:
# git://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git
# version is date of the younger commit
#

Summary:	Linux kernel firmware files
Name:   	kernel-firmware
Version:	20130307
Release:	1
License:	GPLv2
Group:  	System/Kernel and hardware
URL:    	http://www.kernel.org/
# kernel-firmware tarball is generated from the git tree mentioned
# above, by simply cloning it, and  doing:
# git archive -o kernel-firmware-20130307.tar --prefix=linux-firmware-from-kernel/ master
Source0: 	linux-firmware-free-%{version}.tar.xz
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

%prep
%setup -q -n linux-firmware-free-%{version}

# remove unwanted source files
rm -f dsp56k/bootstrap.asm keyspan_pda/*.S

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/lib/firmware
cp -avf * %{buildroot}/lib/firmware
rm -f %{buildroot}/lib/firmware/WHENCE

%files
%defattr(0644,root,root,0755)
%doc WHENCE
/lib/firmware/*

%changelog
* Sun Oct 28 2912 akdengi <akdengi> 20120909-1
- update to 2012-09-09

* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 20110314-2mnb2
+ Revision: 666022
- mass rebuild

* Tue Mar 22 2011 Thomas Backlund <tmb@mandriva.org> 20110314-1
+ Revision: 647606
- update to 2011-03-14

* Fri Feb 04 2011 Thomas Backlund <tmb@mandriva.org> 20101231-1
+ Revision: 635980
- update to 2010-12-31 snapshot

* Thu Nov 04 2010 Thomas Backlund <tmb@mandriva.org> 20101024-1mnb2
+ Revision: 593285
- update to 2010-10-24

* Sun Aug 15 2010 Thomas Backlund <tmb@mandriva.org> 20100804-1mnb2
+ Revision: 570139
- update to 2010-08-04

* Mon May 03 2010 Thomas Backlund <tmb@mandriva.org> 20100217-1mnb2
+ Revision: 541831
- keep bnx2x fw for 2.6.33 series kernels
- update to 20100217 (updated bnx2 and bnx2x firmwares)

* Sun Feb 07 2010 Thomas Backlund <tmb@mandriva.org> 20100107-1mnb2
+ Revision: 501683
- drop firmware tarball from drm-next as its merged upstream
- update to 2010-01-07

* Sat Sep 19 2009 Thomas Backlund <tmb@mandriva.org> 20090604-4mnb2
+ Revision: 444767
- update drm-next firmware to 2009-09-18

* Thu Sep 17 2009 Thomas Backlund <tmb@mandriva.org> 20090604-3mnb2
+ Revision: 444038
- use correct radeon ihex-converted firmware tarball

* Thu Sep 17 2009 Thomas Backlund <tmb@mandriva.org> 20090604-2mnb2
+ Revision: 443983
- add radeon firmware from drm-next, needed by kernel-tmb
- update to 2009-06-04

* Thu May 28 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 20090418-1mnb2
+ Revision: 380647
- Updated to 20090418
- Use lzma for source tarball.

* Mon Mar 30 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 20090111-3mnb2
+ Revision: 362326
- Re-add obsoletes from kernel-firmware-extra to kernel-firmware for
  firmware files which moved to kernel-firmware after previous change.

* Mon Mar 30 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 20090111-2mnb2
+ Revision: 362309
- Include all firmware, not splitting firmwares into
  kernel-firmware-extra (#49195).

* Tue Feb 17 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 20090111-1mnb2
+ Revision: 341862
- Updated to 20090111

* Fri Dec 05 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 20080922-2mnb2
+ Revision: 310782
- Don't include firmware without source, they should be in non-free
  (distributed with kernel-firmware-extra package).
- Suggests kernel-firmware-extra.
- Cosmetics.

* Tue Nov 04 2008 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 20080922-1mnb2
+ Revision: 299838
- Updated to latest linux-firmware-from-kernel snapshot, and change
  versioning to use date of the younger commit, as firmwares aren't
  bound to specific kernel version.

* Sat Sep 06 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-2mnb2
+ Revision: 281995
- Obsolete korg1212-firmware, maestro3-firmware, sb16-firmware, yamaha-firmware.

* Thu Aug 28 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-1mnb2
+ Revision: 277014
- redo spec based on kernel-headers spec
- switch to using dwmw2's linux-firmware-from-kernel git tree
- no need to follow -rc/-git versioning as the firmwares does
  not change that often.
- package is now noarch as we dont build anything
- switch to Manbo Core tagging

* Thu Aug 21 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc4.1mdv2009.0
+ Revision: 274527
- update to 2.6.27-rc4

* Wed Aug 20 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc3.1mdv2009.0
+ Revision: 274212
- fix git typo
- update to 2.6.27-rc3-git6

* Thu Aug 07 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc2.2mdv2009.0
+ Revision: 265550
- bump release
- add buildrequires

* Thu Aug 07 2008 Thomas Backlund <tmb@mandriva.org> 2.6.27-0.rc2.1mdv2009.0
+ Revision: 265537
- add spec file
- use defconfigs from kernel-linus
- start with 2.6.27-rc2
- Created package structure for kernel-firmware.

