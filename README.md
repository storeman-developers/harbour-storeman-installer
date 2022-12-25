# Storeman Installer

**The Storeman Installer for SailfishOS performs the initial installation of the [Storeman OpenRepos client application](https://github.com/storeman-developers/harbour-storeman). Storeman Installer selects, downloads and installs the correct variant of the Storeman application built for the CPU-architecture of the device and the installed SailfishOS release from the SailfishOS-OBS.**

### Background

Starting with version 0.2.9, Storeman is built by the help of the SailfishOS-OBS and initially installed by the Storeman Installer (or manually).  To update from Storeman <&nbsp;0.2.9 (requires SailfishOS ≥&nbsp;3.1.0), one should reinstall Storeman via the Storeman Installer.  After an initial installation of Storeman ≥&nbsp;0.3.0, further updates of Storeman will be performed within Storeman, as usual.

The Storeman Installer works on any SailfishOS release ≥&nbsp;3.1.0 and all supported CPU-architectures (armv7hl, i486 and aarch64).  The current Storeman Installer RPM can be obtained from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest), [OpenRepos.net](https://openrepos.net/content/olf/storeman-installer) and [the SailfishOS-OBS](https://build.merproject.org/package/show/home:olf:harbour-storeman/harbour-storeman-installer).

The current RPMs of Storeman proper can be obtained for manual installation from [Storeman's releases section at GitHub](https://github.com/storeman-developers/harbour-storeman/releases); the RPMs of older Storeman releases are also available there and [at OpenRepos](https://openrepos.net/content/olf/storeman-legacy), e.g., v0.1.8 which works on SailfishOS 2.2.1.<br />
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
  3. Tap on the "File downloaded" notification on your SailfishOS device or select the downloaded RPM file in a file-manager app and choose "Install" in its pulley menu; then confirm the installation.
  4. Preferably disable "Allow untrusted software" again.

* Installation via Storeman (i.e., updating from Storeman <&nbsp; 0.2.9)
  1. Search for *Installer*
  2. Select the *Storeman Installer* by *olf*<br />
     <sup>Side note: If you select the outdated *Storeman Installer* by *osetr*, that will install an outdated *Storeman*, with which you can install the current *Storeman* release; save yourself this indirection and potential issues with software which was never tested on recent SailfishOS releases by installing the current *Storeman Installer* by *olf*.</sup>
  3. You need to enable *olf*'s repository in the top pulley menu, if you did not enable it before.
  4. Install *Storeman Installer*

* Installation via SailfishOS:Chum GUI application
  1. Search for *Installer* in "Applications"
  2. Select *Storeman Installer*
  3. Install *Storeman Installer*

### Features of Storeman Installer

* The Storeman Installer is automatically removed ("uninstalled") when Storeman is being installed.
* [Storeman Installer 1.3.1](https://github.com/storeman-developers/harbour-storeman-installer/releases/tag/1.3.1) and all later versions are offered as an update candidate for Storeman, if an RPM repository is enabled, which offers the *harbour-storeman-installer* package and Storeman (*harbour-storeman* package) <&nbsp;0.2.99 is already installed.
* Installing [Storeman Installer 1.3.1](https://github.com/storeman-developers/harbour-storeman-installer/releases/tag/1.3.1) and all later versions also automatically removes an installed Storeman (*harbour-storeman* package) <&nbsp;0.2.99, which eliminates the former necessity to manually remove ("uninstall") an old Storeman. 
* [Storeman Installer 1.3.8](https://github.com/storeman-developers/harbour-storeman-installer/releases/tag/1.3.8) and all later versions create a persistent log file `/var/log/harbour-storeman-installer.log.txt`.
* Storeman Installer 2 runs "unattended": I.e., without any manual steps, after its installation has been triggered, until Storeman is installed.
* Storeman Installer is slow, because it calls `pkcon` two (releases before v1.3.8) to three times (releases from v[1.3.8](https://github.com/storeman-developers/harbour-storeman-installer/releases/tag/1.3.8) on), which acts quite slowly.  The minimal run time for Storeman Installer 2 is about 7 seconds, the typical run time is rather 10 seconds (measured from the moment Storeman Installer's installation has been triggered, until ultimately Storeman is installed).  This is already a lot, but I rarely experienced a stalled Packagekit daemon (for which `pkcon` is just a command line frontend, communicating with the daemon via D-Bus) during heavy testing, which can be observed with the crude `pkmon` utility (`Ctrl-C` gets you out :wink:), so Storeman Installer now tries to detect these "hangs" and to counter them: If that happens, its run time can be up to slightly more than 1 minute.  In the worst case a stalled PackakgeKit daemon (and with it its `pkcon` client process(es)) stalls Storeman Installer, until the PackageKit daemon reaches its idle time out of 300 seconds (5 minutes; this could theoretically happen three times, resulting in a likely unsuccessful run time of more than 15 minutes).
* You can follow Storeman Installer's actions with a `tail -f /var/log/harbour-storeman-installer.log.txt`, but mind that this file has to exist before telling `tail` to read it.  Storeman Installer will create this log file during its installation, but here you want to start the `tail -f` right *before* that happens.  This can be easly achieved by:<br />
`[defaultuser@sailfishos ] devel-su`<br />
`[root@sailfishos ] touch /var/log/harbour-storeman-installer.log.txt`<br />
`[root@sailfishos ] chmod 0664 /var/log/harbour-storeman-installer.log.txt`<br />
`[root@sailfishos ] chhgrp ssu /var/log/harbour-storeman-installer.log.txt`<br />
Open another terminal window on or ssh session to your device and execute:<br />
`[defaultuser@sailfishos ] tail -f /var/log/harbour-storeman-installer.log.txt`<br />
Then return to the first terminal window or ssh session:<br />
`[root@sailfishos ] pkcon --install-local <path/to/downloaded/harbour-storeman-installer-?.?.?-*.noarch.rpm>`  # Insert real values for `?` (a single character, here a single digit number) and `*` (multiple characters).<br />
If you have already enabled a package repository, which offers Storeman Installer (e.g. OpenRepos/olf or SailfischOS:Chum), a simpler command works, without manually downloading the *harbour-storeman-installer* RPM package:<br />
`[root@sailfishos ] pkcon install harbour-storeman-installer`<br />
BTW, you can list all installed or online available (but not installed) Storeman-related packages by issueing:<br />
`[defaultuser@sailfishos ] pkcon search name storeman`
 
