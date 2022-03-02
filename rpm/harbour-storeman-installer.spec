Summary:        Storeman Installer for Sailfish OS
License:        MIT
Name:           harbour-storeman-installer
Version:        1.1.0
Release:        1
Group:          System
Source0:        %{name}-%{version}.tar.bz2
Requires:       ssu
BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  sailfish-svg2png

%define localauthority_dir polkit-1/localauthority/50-local.d
%define ssu_features_dir   ssu/features.d
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

install -d %{buildroot}%{_datadir}/%{ssu_features_dir}
install mentaljam-obs/%{ssu_features_dir}/* %{buildroot}%{_datadir}/%{ssu_features_dir}

for s in 86 108 128 172
do
  prof=${s}x${s}
  install -d %{buildroot}%{hicolor_icons_dir}/$prof/apps
  sailfish_svg2png -s 1 1 1 1 1 1 $s . %{buildroot}%{hicolor_icons_dir}/$prof/apps
done

# a. `desktop-file-install --help-install` states that the syntax is `-dir=`: To check.
# b. Just an idea to try: -m 755 | --mode=755 may be helpful for resolving issue #1
desktop-file-install --delete-original --dir %{buildroot}%{_datadir}/applications %{name}.desktop

%post
rm -f /var/cache/ssu/features.ini && ssu ur && ssu er mentaljam-obs || true

%postun
rm -f /var/cache/ssu/features.ini && ssu ur || true

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{ssu_features_dir}/mentaljam-obs.ini
%{_datadir}/applications/%{name}.desktop
%{_sharedstatedir}/%{localauthority_dir}/50-%{name}-packagekit.pkla
%{hicolor_icons_dir}/*/apps/%{name}.png

%changelog
* Mon Sep  6 2021 Petr Tsymbarovich <petr@tsymbarovich.ru> - 1.1.0-1
- Update translations
* Sun Aug 22 2021 Petr Tsymbarovich <petr@tsymbarovich.ru> - 1.0.1-1
- Update translations
