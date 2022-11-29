Summary:        Installs Storeman for SailfishOS
License:        MIT
Name:           harbour-storeman-installer
# The Git release tag format must adhere to just <version> since version 1.2.6.
# The <version> field adheres to semantic versioning and the <release> field 
# comprises one of {alpha,beta,rc,release} postfixed with a natural number
# greater or equal to 1 (e.g. "beta3").  For details and reasons, see
# https://github.com/storeman-developers/harbour-storeman-installer/wiki/Git-tag-format
Version:        2.0.0
Release:        alpha1
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
BuildRequires:  desktop-file-utils
Requires:       ssu
Requires:       systemd
# The oldest SailfishOS release Storeman ≥ 0.2.9 compiles for & the oldest available DoD repo at Sailfish-OBS:
Requires: sailfish-version >= 3.1.0

%define localauthority_dir polkit-1/localauthority/50-local.d
%define screenshots_url    https://github.com/storeman-developers/harbour-storeman/raw/master/.xdata/screenshots/

# This description section includes metadata for SailfishOS:Chum, see
# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%description
Storeman Installer selects the right variant of the Storeman OpenRepos client
application built for the CPU-architecture of the device and the installed
SailfishOS release.

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
mkdir -p %{buildroot}%{_unitdir}
cp /systemd/system/%{name}.* %{buildroot}%{_unitdir}/

mkdir -p %{buildroot}%{_sharedstatedir}/%{localauthority_dir}
cp %{localauthority_dir}/* %{buildroot}%{_sharedstatedir}/%{localauthority_dir}/
#mkdir -p %%{buildroot}%%{_sysconfdir}/%%{localauthority_dir}
#cp %%{localauthority_dir}/* %%{buildroot}%%{_sysconfdir}/%%{localauthority_dir}/

%post
ssu rr mentaljam-obs
rm -f /var/cache/ssu/features.ini
ssu ar harbour-storeman-obs 'https://repo.sailfishos.org/obs/home:/olf:/harbour-storeman/%%(release)_%%(arch)/'
ssu ur

%posttrans
%{_bindir}/systemctl start %{name}.timer

# This MUST be omitted for Storeman ≥ 0.3.2!
# Disabling this is fine, anyway, because Storeman will re-employ this repo.
# In any failure case, at most this repo stays enabled unnecessarily.
#%%postun
#if [ "$1" = "0" ] # Removal
#then
#  ssu rr harbour-storeman-obs
#  rm -f /var/cache/ssu/features.ini
#  ssu ur
#fi

%files
%defattr(-,root,root,-)
%{_unitdir}/%{name}.timer
%{_unitdir}/%{name}.service
%{_sharedstatedir}/%{localauthority_dir}/50-%{name}.pkla
#%%{_sysconfdir}/%%{localauthority_dir}/50-%%{name}.pkla

%changelog
* XXXX - 2.0.0-alpha1
- 
* Tue Nov 29 2022 olf <https://github.com/Olf0> - 1.3.0-release1
- Enhance spec file a bit
* Sat Jun 04 2022 olf <https://github.com/Olf0> - 1.2.9-release1
- pkcon expects options before the command (#74)
* Sun May 15 2022 olf <https://github.com/Olf0> - 1.2.8-release1
- Requires: sailfish-version >= 3.1.0 (#61), because this is the oldest SailfishOS release any Storeman version installed by Storeman Installer will work on.
* Sun Apr 10 2022 olf <https://github.com/Olf0> - 1.2.7-release1
- Fix icon deployment
* Thu Apr 07 2022 olf <https://github.com/Olf0> - 1.2.6-release1
- Release tags must not carry a prepended "v" any longer and solely consist of a simple semantic version number a.b.c, because … (see next point)
- Specify a correct source link at GitHub (#42)
- Address a couple of rpmlint complaints
Versions 1.2.3, 1.2.4 and 1.2.5 are unreleased test versions.
* Sun Mar 20 2022 olf <https://github.com/Olf0> - 1.2.2-1
- .desktop file: Trivially bail out of SailJail #38
* Thu Mar 17 2022 olf <https://github.com/Olf0> - 1.2.1-1
- spec file: Add SailfishOS:Chum metadata (#23) plus spec file: Add categories (#31) and #30
- Create help-template.md (#24)
- Create and enhance README (#25, #29, #30, #32, #33, #34, #35)
* Sun Mar 13 2022 olf <https://github.com/Olf0> - 1.2.0-1
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
