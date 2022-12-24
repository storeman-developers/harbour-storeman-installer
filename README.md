# Storeman Installer

**The Storeman Installer for SailfishOS performs the initial installation of the [Storeman OpenRepos client application](https://github.com/storeman-developers/harbour-storeman). Storeman Installer selects, downloads and installs the correct variant of the Storeman application built for the CPU-architecture of the device and the installed SailfishOS release from the SailfishOS-OBS.**

### Background

Starting with version 0.2.9, Storeman is built by the help of the SailfishOS-OBS and initially installed by the Storeman Installer (or manually).  To update from Storeman <&nbsp;0.2.9 (requires SailfishOS ≥&nbsp;3.1.0), one should reinstall Storeman via the Storeman Installer.  After an initial installation of Storeman ≥&nbsp;0.3.0, further updates of Storeman will be performed within Storeman, as usual.

The Storeman Installer works on any SailfishOS release ≥&nbsp;3.1.0 and all supported CPU-architectures (armv7hl, i486 and aarch64).  The current Storeman Installer RPM can be obtained from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest), [OpenRepos.net](https://openrepos.net/content/olf/storeman-installer) and [the SailfishOS-OBS](https://build.merproject.org/package/show/home:olf:harbour-storeman/harbour-storeman-installer).

The current RPMs of Storeman proper can be obtained for manual installation from [Storeman's releases section at GitHub](https://github.com/storeman-developers/harbour-storeman/releases); the RPMs of older Storeman releases are also available there, e.g., v0.1.8 which works on SailfishOS 2.2.1.<br />
Alternatively, the current RPMs of Storeman proper can be obtained from [the SailfishOS-OBS](https://build.merproject.org/project/show/home:olf:harbour-storeman).

### Important notes

* If you experience issues with Storeman Installer, please take a look at its log file `/var/log/harbour-storeman-installer.log.txt`.  If that does not reveal to you what is going wrong, please check first if an issue report describing this issue [is already filed at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/issues), then you might file a new issue report there and attach the log file to it, or enhance an extant bug report; alternatively (but this is really a much worse choice) and usually with much longer response times from me and no real issue tracking due to the lack of any integration, you can describe your issue in [a comment at OpenRepos](https://openrepos.net/content/olf/storeman-installer#comments) with a link to your log file copied to a data-sharing service like Pastebin etc.
* If you experience issues when installing, removing or updating packages after a SailfishOS upgrade, try running `devel-su pkcon refresh` in a terminal app.
* Before software can be build for a SailfishOS release at the SailfishOS-OBS, Jolla must create a corresponding "download on demand (DoD)" OBS-repository.  It might take some time after a new "general availability (GA)" SailfishOS release is published before the corresponding "DoD" repository is being made available, during which installing or updating Storeman by the Storeman Installer or Storeman's self-updating on a device with the new SailfishOS release already installed will not succeed, because Storeman cannot be compiled for this new SailfishOS release by the Sailfish-OBS, yet; consequently this is always the case during the "closed beta (cBeta)" and "early access (EA)" phases of a new SailfishOS release.  Hence one has to manually download and install, or update Storeman built for the last prior SailfishOS GA release, then (and hope that there is no change in the new SailfishOS release, which breaks Storeman; if there is please report that soon at [Storeman's issue tracker](https://github.com/storeman-developers/harbour-storeman/issues)).
* Disclaimer: Storeman and Storeman Installer may still have flaws, kill your kittens or break your SailfishOS installation!  Although this is very unlikely after years of testing by many users, new flaws may be introduced in any release (as for any software).  Be aware, that the license you implicitly accept by using Storeman excludes any liability.

### Installation instructions

* Initial installation without having Storeman or SailfishOS:Chum already installed
  1. Enable "System → Security → Untrusted software → Allow untrusted software" in the SailfishOS Settings app.
  2. Download the current Storeman Installer RPM from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest), [OpenRepos.net](https://openrepos.net/content/olf/storeman-installer) or [the SailfishOS-OBS](https://build.merproject.org/package/show/home:olf:harbour-storeman/harbour-storeman-installer).
