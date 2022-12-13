Summary:        Installs Storeman for SailfishOS
License:        MIT
Name:           harbour-storeman-installer
# The Git release tag format must adhere to just <version> since version 1.2.6.
# The <version> field adheres to semantic versioning and the <release> field 
# comprises one of {alpha,beta,rc,release} postfixed with a natural number
# greater or equal to 1 (e.g., "beta3").  For details and reasons, see
# https://github.com/storeman-developers/harbour-storeman-installer/wiki/Git-tag-format
Version:        2.0.23
Release:        release1.rpm.only
Group:          Applications/System
URL:            https://github.com/storeman-developers/%{name}
# These "Source:" lines below require that the value of ${name} is also the
# project name at GitHub and the value of ${version} is also the name of a
# correspondingly set git-tag.
# Alternative links, which also download ${projectname}-${tagname}.tar.gz:
# Source:       https://github.com/storeman-developers/%%{name}/archive/%%{version}.tar.gz
# Source:       https://github.com/storeman-developers/%%{name}/archive/refs/tags/%%{version}.tar.gz
Source:         https://github.com/storeman-developers/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
# For details on "Requires:" statements, especially "Requires(a,b,c):", see:
# https://rpm-software-management.github.io/rpm/manual/spec.html#requires
# Most of the following dependencies are required for both, specifically for
# the `%post` section and additionally as a general requirement after the RPM
# transaction has finished, but shall be already installed on SailfishOS:
Requires:       ssu
Requires(pretrans): ssu
Requires(posttrans): harbour-storeman >= 0.3.0
# The oldest SailfishOS release Storeman ≥ 0.2.9 compiles for, plus the oldest
# useable DoD-repo at https://build.merproject.org/project/subprojects/sailfishos
Requires:       sailfish-version >= 3.1.0
# Provide an automatically presented update candidate for an installed Storeman < 0.2.99:
Conflicts:      harbour-storeman < 0.2.99
Obsoletes:      harbour-storeman < 0.2.99
Provides:       harbour-storeman = 0.3.0~1

%global screenshots_url https://github.com/storeman-developers/harbour-storeman/raw/master/.xdata/screenshots/

# This description section includes metadata for SailfishOS:Chum, see
# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%description
Storeman Installer selects, downloads and installs the right variant of
the Storeman OpenRepos client application built for the CPU-architecture
of the device and its installed SailfishOS release.

%if "%{?vendor}" == "chum"
PackageName: Storeman Installer for SailfishOS
Type: desktop-application
Categories:
 - Utilities
 - System
 - Network
 - PackageManager
DeveloperName: Storeman developers (mentaljam)
Custom:
  Repo: %{url}
Icon: %{url}/raw/master/icons/%{name}.svg
Screenshots:
 - %{screenshots_url}screenshot-screenshot-storeman-01.png
 - %{screenshots_url}screenshot-screenshot-storeman-02.png
 - %{screenshots_url}screenshot-screenshot-storeman-03.png
 - %{screenshots_url}screenshot-screenshot-storeman-04.png
 - %{screenshots_url}screenshot-screenshot-storeman-06.png
 - %{screenshots_url}screenshot-screenshot-storeman-07.png
 - %{screenshots_url}screenshot-screenshot-storeman-08.png
 - %{screenshots_url}screenshot-screenshot-storeman-09.png
Url:
  Homepage: %{url}
  Help: %{url}/issues
  Bugtracker: %{url}/issues
%endif

%prep
%setup -q

%build

%install

%pretrans
# The %%pretrans scriptlet is deliberately run when installing and updating.
# The added harbour-storeman-obs repository is not removed when Storeman Installer
# is removed, but when Storeman is removed (before it was added, removed, then
# added again when installing Storeman via Storeman Installer), which is far more
# fail-safe: If something goes wrong, this SSUs repo entry is now ensured to exist.
ssu_ur=no
ssu_lr="$(ssu lr | grep '^ - ' | cut -f 3 -d ' ')"
if echo "$ssu_lr" | grep -Fq mentaljam-obs
then
  ssu rr mentaljam-obs
  rm -f /var/cache/ssu/features.ini
  ssu_ur=yes
fi
if ! echo "$ssu_lr" | grep -Fq harbour-storeman-obs
then
  ssu ar harbour-storeman-obs 'https://repo.sailfishos.org/obs/home:/olf:/harbour-storeman/%%(release)_%%(arch)/'
  ssu_ur=yes
fi
if [ $ssu_ur = yes ]
then ssu ur
fi
# BTW, `ssu`, `rm -f`, `mkdir -p` etc. *always* return with "0" ("success"), hence
# no appended `|| true` needed to satisfy `set -e` for failing commands outside of
# flow control directives (if, while, until etc.).  Furthermore on Fedora Docs it
# is indicated that solely the final exit status of a whole scriptlet is crucial: 
# See https://docs.pagure.org/packaging-guidelines/Packaging%3AScriptlets.html
# or https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
# committed on 18 February 2019 by tibbs ( https://pagure.io/user/tibbs ) as
# "8d0cec9 Partially convert to semantic line breaks." in
# https://pagure.io/packaging-committee/c/8d0cec97aedc9b34658d004e3a28123f36404324
exit 0

%posttrans
# At the very end of every install or upgrade
# Try to fake it:
echo -n

%files

%changelog
* Mon Dec 12 2022 olf <Olf0@users.noreply.github.com> - 2.0.23-release1.rpm.only
- Try starting Storeman installation via RPM measures only
* Sun Dec 11 2022 olf <Olf0@users.noreply.github.com> - 2.0.22-release1.detached.script
- Start harbour-storeman-installer script fully detached ("double fork" / daemonize) in %%posttrans
- Update defer-inst-via-detached-script branch with changes for v1.3.6:
  - Set umask and PWD in harbour-storeman-installer script
  - Start installation of harbour-storeman fully detached ("double fork" / daemonize)
  - Print version of harbour-storeman-installer package in the log file entry of each run
  - Refactor and enhance failure of: pkcon repo-set-data harbour-storeman-obs refresh-now true  
* Fri Dec 09 2022 olf <Olf0@users.noreply.github.com> - 1.3.5-release1
- Update `harbor-storeman-installer` script to version in defer-inst-via-detached-script branch (#144)
- Re-adapt `harbor-storeman-installer` script for interactive use (#144)
- Log file needs to be writable (#146)
* Wed Dec 07 2022 olf <Olf0@users.noreply.github.com> - 2.0.12-release1.detached.script
- Start the `harbor-storeman-installer` script as detached ("&") in the `%posttrans` scriptlet
- Thus eliminating the necessity for user interaction(s), besides triggering the installation of Storeman Installer
* Sun Dec 04 2022 olf <Olf0@users.noreply.github.com> - 1.3.4-release1
- Radically rewrite `harbor-storeman-installer` script in `/usr/bin` (#136)
- The `harbor-storeman-installer` script ultimately issues `pkcon install harbour-storeman … &` (i.e., also detached), allowing this script to be removed in the process of the Storeman installation
- Do not use pkcon's option -n; it is slow enough (#134)
* Sat Dec 03 2022 olf <Olf0@users.noreply.github.com> - 1.3.3-release1
- Start pkcon commands with the options -pn (#130)
- Tidy spec file as implemented in v2.0 (#130)
- Clarify comment (#128)
* Thu Dec 01 2022 olf <Olf0@users.noreply.github.com> - 1.3.2-release1
- Refine %%post section of the spec file (#96)
* Wed Nov 30 2022 olf <Olf0@users.noreply.github.com> - 1.3.1-release1
- Fix auto-removing Storeman < 0.3.0 on SailfishOS ≥ 3.1.0 (#109)
* Tue Nov 29 2022 olf <Olf0@users.noreply.github.com> - 1.3.0-release1
- Now should automatically remove an installed Storeman < 0.3.0 when being installed (#95)
- Enhance multiple aspects of the spec file (#89, #91, #93)
- Many small enhancements of comments, strings and other non-code assets
- Storeman Installer ≥ 1.3.0 is a prerequisite for Storeman ≥ 0.3.2
* Sat Jun 04 2022 olf <Olf0@users.noreply.github.com> - 1.2.9-release1
- pkcon expects options before the command (#74)
* Sun May 15 2022 olf <Olf0@users.noreply.github.com> - 1.2.8-release1
- Requires: sailfish-version >= 3.1.0 (#61), because this is the oldest SailfishOS release any Storeman version installed by Storeman Installer will work on.
* Sun Apr 10 2022 olf <Olf0@users.noreply.github.com> - 1.2.7-release1
- Fix icon deployment
* Thu Apr 07 2022 olf <Olf0@users.noreply.github.com> - 1.2.6-release1
- Release tags must not carry a prepended "v" any longer and solely consist of a simple semantic version number a.b.c, because … (see next point)
- Specify a correct source link at GitHub (#42)
- Address a couple of rpmlint complaints
Versions 1.2.3, 1.2.4 and 1.2.5 are unreleased test versions.
* Sun Mar 20 2022 olf <Olf0@users.noreply.github.com> - 1.2.2-1
- .desktop file: Trivially bail out of SailJail #38
* Thu Mar 17 2022 olf <Olf0@users.noreply.github.com> - 1.2.1-1
- spec file: Add SailfishOS:Chum metadata (#23) plus spec file: Add categories (#31) and #30
- Create help-template.md (#24)
- Create and enhance README (#25, #29, #30, #32, #33, #34, #35)
* Sun Mar 13 2022 olf <Olf0@users.noreply.github.com> - 1.2.0-1
- Change group from users to ssu
- polkit: Limit allowed actions to the necessary ones
- Do not to call Bash
- desktop file: Only label languages by country code 
- Create bug-template.md / Create suggestion-template.md
- Create build.yml
- Update repository configuration
- Add URL: to spec file
- Update spec file
* Mon Sep  6 2021 Petr Tsymbarovich <petr@tsymbarovich.ru> - 1.1.0-1
- Update translations
* Sun Aug 22 2021 Petr Tsymbarovich <petr@tsymbarovich.ru> - 1.0.1-1
- Update translations
* Thu Aug 19 2021 Petr Tsymbarovich <petr@tsymbarovich.ru> - 1.0.0-1
- Initial release

