Summary:        Storeman Installer for Sailfish OS
License:        MIT
Name:           harbour-storeman-installer
Version:        1.0.0
Release:        1
Group:          System
Source0:        %{name}-%{version}.tar.bz2
Requires:       ssu
BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  sailfish-svg2png

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}

install -d %{buildroot}%{_datadir}/mapplauncherd/privileges.d
install mapplauncherd/privileges.d/%{name} %{buildroot}%{_datadir}/mapplauncherd/privileges.d/%{name}

install -d %{buildroot}%{_datadir}/ssu/features.d
install mentaljam-obs/ssu/features.d/mentaljam-obs.ini %{buildroot}%{_datadir}/ssu/features.d/mentaljam-obs.ini

for s in 86 108 128 172
do
  prof=${s}x${s}
  install -d %{buildroot}%{_datadir}/icons/hicolor/$prof/apps
  sailfish_svg2png -s 1 1 1 1 1 1 $s . %{buildroot}%{_datadir}/icons/hicolor/$prof/apps
done

desktop-file-install \
  --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{name}.desktop

%post
rm -f /var/cache/ssu/features.ini && ssu ur && ssu er mentaljam-obs || true

%postun
rm -f /var/cache/ssu/features.ini && ssu ur || true

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/mapplauncherd/privileges.d/%{name}
%{_datadir}/ssu/features.d/mentaljam-obs.ini
