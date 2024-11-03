Summary:        Installs Storeman for SailfishOS
License:        LGPL-2.1-only
Name:           harbour-storeman-installer
# The Git tag format must adhere to <release>/<version> since 2023-05-18.
# The <version> tag must adhere to semantic versioning, for details see
# https://semver.org/
Version:        2.2.7
# The <release> tag comprises one of {alpha,beta,rc,release} postfixed with a
# natural number greater or equal to 1 (e.g. "beta3") and may additionally be
# postfixed with a plus character ("+"), the name of the packager and a release
# number chosen by her (e.g. "rc2+jane4").  `{alpha|beta|rc|release}`
# indicates the expected status of the software.  No other identifiers shall be
# used for any published version, but for the purpose of testing infrastructure
# other nonsensual identifiers as `adud` may be used, which do *not* trigger a
# build at GitHub and OBS, when configured accordingly; mind the sorting
# (`adud` < `alpha`).  For details and reasons, see
# https://github.com/Olf0/sfos-upgrade/wiki/Git-tag-format
Release:        release8
# The Group tag should comprise one of the groups listed here:
# https://github.com/mer-tools/spectacle/blob/master/data/GROUPS
Group:          Software Management/Package Manager
URL:            https://github.com/storeman-developers/%{name}
# The "Source0:" line below requires that the value of %%{name} is also the
# project name at GitHub and the value of %%{release}/%%{version} is also the
# name of a correspondingly set Git tag.
Source0:        %{url}/archive/%{release}/%{version}/%{name}-%{version}.tar.gz
# Note that the rpmlintrc file must be named so according to
# https://en.opensuse.org/openSUSE:Packaging_checks#Building_Packages_in_spite_of_errors
Source99:       %{name}.rpmlintrc
BuildArch:      noarch
# For details on "Requires:" statements, especially "Requires(a,b,c):", see:
# https://rpm-software-management.github.io/rpm/manual/spec.html#requires
# Most of the following dependencies are required for both, specifically for
# the %%post scriptlet and additionally as a general requirement after the RPM
# transaction has finished, but shall be already installed on SailfishOS:
Requires:       ssu
Requires(post): ssu
Requires:       PackageKit
Requires(posttrans): PackageKit
# `or` was introduced with RPM 4.13, SailfishOS v2.2.1 started deploying v4.14:
# https://together.jolla.com/question/187243/changelog-221-nurmonjoki/#187243-rpm
# But the SailfishOS-OBS' does not support `or`, either due to the antique OBS
# release or `tar_git`: https://github.com/MeeGoIntegration/obs-service-tar-git
# ToDo: Check if the GNU-versions of these packages (named as alternatives below)
# also provide the aliases ("virtual packages") denoted here, then these can be
# used; ultimately most of these packages shall be already installed, anyway.
# 1. `coreutils` (for e.g. `touch` and many other very basic UNIX tools):
# Requires:       (busybox-symlinks-coreutils or gnu-coreutils)
Requires:       coreutils
# Requires(post,posttrans): (busybox-symlinks-coreutils or gnu-coreutils)
Requires(post): coreutils
Requires(posttrans): coreutils
# 2. `util-linux` for `setsid`:
Requires:       util-linux
Requires(posttrans): util-linux
# 3. `psmisc` for `killall`:
# Requires:       (busybox-symlinks-psmisc or psmisc-tools)
Requires:       psmisc
# Requires(posttrans): (busybox-symlinks-psmisc or psmisc-tools)
Requires(posttrans): psmisc
# 4. `procps` for `pkill` / `pgrep`: Used `killall` instead, which suits better here.
# Requires:       (busybox-symlinks-procps or procps-ng)
#Requires:       procps
# Requires(posttrans): (busybox-symlinks-procps or procps-ng)
#Requires(posttrans): procps
# The oldest SailfishOS release Storeman ≥ 0.2.9 compiles for, plus the oldest
# useable DoD-repo at https://build.merproject.org/project/subprojects/sailfishos
Requires:       sailfish-version >= 3.1.0
# Provide an automatically presented update candidate for an installed Storeman < 0.2.99:
Conflicts:      harbour-storeman < 0.2.99
Obsoletes:      harbour-storeman < 0.2.99
Provides:       harbour-storeman = 0.3.0~3

%global screenshots_url    https://github.com/storeman-developers/harbour-storeman/raw/master/.xdata/screenshots/
%global logdir             %{_localstatedir}/log
%global logfile            %{logdir}/%{name}.log.txt

# This %%description section includes metadata for SailfishOS:Chum, see
# https://github.com/sailfishos-chum/main/blob/main/Metadata.md
%description
Storeman Installer selects, downloads and installs the right variant of
the Storeman OpenRepos client application built for the CPU-architecture
of the device and its installed SailfishOS release.

%if 0%{?_chum}
Title: Storeman Installer for SailfishOS
Type: desktop-application
Categories:
 - System
 - Utility
 - Network
 - Settings
 - PackageManager
DeveloperName: olf (Olf0)
Custom:
  Repo: %{url}
PackageIcon: %{url}/raw/master/.icon/%{name}.svg
Screenshots:
 - %{screenshots_url}screenshot-screenshot-storeman-01.png
 - %{screenshots_url}screenshot-screenshot-storeman-02.png
 - %{screenshots_url}screenshot-screenshot-storeman-03.png
 - %{screenshots_url}screenshot-screenshot-storeman-04.png
 - %{screenshots_url}screenshot-screenshot-storeman-06.png
 - %{screenshots_url}screenshot-screenshot-storeman-07.png
 - %{screenshots_url}screenshot-screenshot-storeman-08.png
 - %{screenshots_url}screenshot-screenshot-storeman-09.png
Links:
  Homepage: https://openrepos.net/content/olf/storeman-installer
  Help: %{url}/issues
  Bugtracker: %{url}/issues
  Donation: https://openrepos.net/donate
%endif

%define _binary_payload w6.gzdio
%define _source_payload w6.gzdio

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_bindir}
cp bin/%{name} %{buildroot}%{_bindir}/

%post
# The %%post scriptlet is deliberately run when installing and updating.
# Create a persistent log-file, i.e. which is not managed by RPM and hence
# is unaffected by removing the %%{name} RPM package:
if [ ! -e %{logfile} ]
then
  curmask="$(umask)"
  umask 022
  [ ! -e %{logdir} ] && mkdir -p %{logdir}
  umask 113
  touch %{logfile}
  # Not necessary, because umask is set:
  # chmod 0664 %%{logfile}
  chgrp ssu %{logfile}
  umask "$curmask"
fi
# The added harbour-storeman-obs repository is not removed when Storeman Installer
# is removed, but when Storeman is removed (before it was added, removed, then
# added again when installing Storeman via Storeman Installer), which is far more
# fail-safe: If something goes wrong, this SSUs repo entry is now ensured to exist.
ssu_ur=no
ssu_lr="$(ssu lr | grep '^ - ' | cut -f 3 -d ' ')"
if echo "$ssu_lr" | grep -Fq mentaljam-obs
then
  ssu rr mentaljam-obs
  ssu_ur=yes
fi
# Add harbour-storeman-obs repository configuration, depending on the installed
# SailfishOS release (3.1.0 is the lowest supported, see line 68):
source %{_sysconfdir}/os-release
# Three equivalent variants, but the sed-based ones have additional, ugly
# backslashed quoting of all backslashes, curly braces and brackets (likely
# also quotation marks), and a double percent for a single percent character,
# because they were developed as shell-scripts for `%%define <name> %%(<script>)`
# (the same applies to scriplets with "queryformat-expansion" option -q, see 
# https://rpm-software-management.github.io/rpm/manual/scriptlet_expansion.html#queryformat-expansion ):
# %%define _sailfish_version %%(source %%{_sysconfdir}/os-release; echo "$VERSION_ID" | %%{__sed} 's/^\\(\[0-9\]\[0-9\]*\\)\\.\\(\[0-9\]\[0-9\]*\\)\\.\\(\[0-9\]\[0-9\]*\\).*/\\1\\2\\3/')
# ~: sailfish_version="$(source %%{_sysconfdir}/os-release; echo "$VERSION_ID" | sed 's/^\([0-9][0-9]*\)\.\([0-9][0-9]*\)\.\([0-9][0-9]*\).*/\1\2\3/')"
# Using an extended ("modern") RegEx shortens the sed script, but busybox's sed
# does not support the POSIX option -E for that!  Hence one must resort to the
# non-POSIX option -r for that, without a real gain compared to the basic RegEx:
# %%define _sailfish_version %%(source %%{_sysconfdir}/os-release; echo "$VERSION_ID" | %%{__sed} -r 's/^(\[0-9\]+)\\.(\[0-9\]+)\\.(\[0-9\]+).*/\\1\\2\\3/')
# ~: sailfish_version="$(source %%{_sysconfdir}/os-release; echo "$VERSION_ID" | sed -r 's/^([0-9]+)\.([0-9]+)\.([0-9]+).*/\1\2\3/')"
# Note: Debug output of RPM macros assigned by a %%define statement is best
# done by `echo`s / `printf`s at the start of the %%build section.
# The variant using `cut` and `tr` instead of `sed` does not require extra quoting,
# regardless where it is used (though escaping each quotation mark by a backslash
# might be advisable, when using it inside a %%define statement's `%%()` ).
sailfish_version="$(echo "$VERSION_ID" | cut -s -f 1-3 -d '.' | tr -d '.')"
# Must be an all numerical string of at least three digits:
if echo "$sailfish_version" | grep -q '^[0-9][0-9][0-9][0-9]*$'
then
  if [ "$sailfish_version" -lt 460 ]
  then ssu ar harbour-storeman-obs 'https://repo.sailfishos.org/obs/home:/olf:/harbour-storeman/%%(release)_%%(arch)/'
  else ssu ar harbour-storeman-obs 'https://repo.sailfishos.org/obs/home:/olf:/harbour-storeman/%%(releaseMajorMinor)_%%(arch)/'
  fi
  ssu_ur=yes
# Should be enhanced to proper debug output, also writing to log-file and systemd-journal:
else echo "Error: VERSION_ID=$VERSION_ID => sailfish_version=$sailfish_version" >&2
fi
if [ $ssu_ur = yes ]
then ssu ur
fi
# BTW, `ssu`, `rm -f`, `mkdir -p` etc. *always* return with "0" ("success"), hence
# no appended `|| true` needed to satisfy `set -e` for failing commands outside of
# flow control directives (if, while, until etc.).  Furthermore Fedora Docs etc.
# state that solely the final exit status of a whole scriptlet is crucial: 
# See https://docs.pagure.org/packaging-guidelines/Packaging%3AScriptlets.html
# or https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_syntax
# committed on 18 February 2019 by tibbs ( https://pagure.io/user/tibbs ) in
# https://pagure.io/packaging-committee/c/8d0cec97aedc9b34658d004e3a28123f36404324
# Hence only the main section of a spec file and likely also `%%(<shell-script>)`
# statements are executed in a shell called with the option `-e', but not the
# scriptlets: `%%pre*`, `%%post*`, `%%trigger*` and `%%file*`
exit 0

%posttrans
# At the very end of every install or upgrade
# The harbour-storeman-installer script must be started fully detached
# (by a double-fork / "daemonize") to allow for this RPM transaction
# to finalise (what waiting for it to finish would prevent).
# (Ab)using the %%posttrans' interpreter instance for the preamble:
umask 113
# [ "$PWD" = / ] || cd /  # Set PWD to /, if not already; omitted,
# because the scriptlets are executed with PWD safely set to /.
setsid --fork sh -c '(%{_bindir}/%{name} "$1" "$2")' sh_call_inst-storeman "$$" "%{logfile}" >> "%{logfile}" 2>&1 <&-
# The first 15 characters of the spawned process' name
# (to be used for, e.g. `ps` and `pgrep` / `pkill`) are:
# sh_call_inst-st
exit 0

%files
%attr(0754,root,ssu) %{_bindir}/%{name}

# Changelog format: https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/SF4VVE4NBEDQJDJZ4DJ6YW2DTGMWP23E/#6O6DFC6GDOLCU7QC3QJKJ3VCUGAOTD24
%changelog
* Thu Sep  9 1999 olf <Olf0@users.noreply.github.com> - 99.99.99
- See %{url}/releases

