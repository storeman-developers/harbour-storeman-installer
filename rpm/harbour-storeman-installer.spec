Summary:        Storeman Installer for Sailfish OS
License:        MIT
Name:           harbour-storeman-installer
Version:        1.2.0
Release:        1
Group:          System
URL:            https://github.com/storeman-developers/harbour-storeman-installer
Source0:        %{name}-%{version}.tar.bz2
Requires:       ssu
BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  sailfish-svg2png

%define localauthority_dir polkit-1/localauthority/50-local.d
%define hicolor_icons_dir  %{_datadir}/icons/hicolor

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}

install -d %{buildroot}%{_sharedstatedir}/%{localauthority_dir}
install %{localauthority_dir}/* %{buildroot}%{_sharedstatedir}/%{localauthority_dir}

for s in 86 108 128 172
do
  prof=${s}x${s}
  install -d %{buildroot}%{hicolor_icons_dir}/$prof/apps
  sailfish_svg2png -s 1 1 1 1 1 1 $s . %{buildroot}%{hicolor_icons_dir}/$prof/apps
done

# a. `desktop-file-install --help-install` states that the syntax is `-dir=`: To check.
# b. Just an idea to try: -m 755 | --mode=755 may be helpful for resolving issue #1
desktop-file-install --delete-original --dir %{buildroot}%{_datadir}/applications %{name}.desktop

%posttrans
ssu rr mentaljam-obs
rm -f /var/cache/ssu/features.ini
ssu ar storeman-obs 'https://repo.sailfishos.org/obs/home:/poetaster:/storeman/%%(release)_%%(arch)/'
ssu ur

%postun
ssu rr storeman-obs
rm -f /var/cache/ssu/features.ini
ssu ur

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_sharedstatedir}/%{localauthority_dir}/50-%{name}-packagekit.pkla
%{hicolor_icons_dir}/*/apps/%{name}.png

%changelog
* Thu Jan 27 2022 olf <https://github.com/Olf0> - 1.2.0-1
- Update repository configuration
- Add URL: to spec file
* Mon Sep  6 2021 Petr Tsymbarovich <petr@tsymbarovich.ru> - 1.1.0-1
- Update translations
* Sun Aug 22 2021 Petr Tsymbarovich <petr@tsymbarovich.ru> - 1.0.1-1
- Update translations
* Thu Aug 19 2021 Petr Tsymbarovich <petr@tsymbarovich.ru> - 1.0.0-1
- Initial release
