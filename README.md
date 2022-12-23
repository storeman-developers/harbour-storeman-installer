# Storeman Installer

**The Storeman Installer for SailfishOS performs the initial installation of the [Storeman OpenRepos client application](https://github.com/storeman-developers/harbour-storeman). Storeman Installer selects, downloads and installs the correct variant of the Storeman application built for the CPU-architecture of the device and the installed SailfishOS release from the SailfishOS-OBS.**

### Background

Starting with version 0.2.9, Storeman is built by the help of the SailfishOS-OBS and initially installed by the Storeman Installer (or manually).  To update from Storeman <&nbsp;0.2.9 (needs SailfishOS ≥&nbsp;3.1.0), one should reinstall Storeman via the Storeman Installer.  After an initial installation of Storeman ≥&nbsp;0.3.0, further updates of Storeman will be performed within Storeman, as usual.

The Storeman Installer works on any SailfishOS release ≥&nbsp;3.1.0 and all supported CPU-architectures (armv7hl, i486 and aarch64).  The current Storeman Installer RPM can be obtained from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest), [OpenRepos.net](https://openrepos.net/content/olf/storeman-installer) and [the SailfishOS-OBS](https://build.merproject.org/package/show/home:olf:harbour-storeman/harbour-storeman-installer).

If you use the SailfishOS:Chum community repository, e.g., via [the SailfishOS:Chum GUI application](https://chumrpm.netlify.app/), you can install Storeman from there, without the indirection via Storeman Installer.

The current RPMs of Storeman proper can be obtained for manual installation from [Storeman's releases section at GitHub](https://github.com/storeman-developers/harbour-storeman/releases); the RPMs of older Storeman releases are also available there, e.g., v0.1.8 which works on SailfishOS 2.2.1.<br />
Alternatively the current RPMs of Storeman proper can be obtained from [the SailfishOS-OBS](https://build.merproject.org/project/show/home:olf:harbour-storeman).

### Important notes

* If you have any troubles with installing, removing or updating packages after a SailfishOS upgrade, try running `devel-su pkcon refresh` in the terminal app.
* Before software can be built for a SailfishOS release at the SailfishOS-OBS, Jolla must create a corresponding "download on demand (DoD)" OBS-repository.  It often takes some time after a new "general availability (GA)" SailfishOS release is published before the corresponding "DoD" repository is being made available, during which installing or updating Storeman by the Storeman Installer or Storeman's self-updating on a device with the new SailfishOS release already installed will fail; consequently this is always the case during the "closed beta (cBeta)" and "early access (EA)" phases of a new SailfishOS release.  Hence one has to either manually set the last prior SailfishOS GA release in the SailfishOS:Chum GUI application or manually download and install or update Storeman built for the last prior SailfishOS GA release, then.
* Disclaimer: Storeman and Storeman Installer may still have flaws, kill your kittens or break your SailfishOS installation!  Although this is very unlikely after years of testing by many users, new flaws may be introduced in any release (as for any software).  Be aware, that the license you implicitly accept by using Storeman excludes any liability.

### Installation instructions

* Initial installation without having Storeman or SailfishOS:Chum already installed
  1. Enable "System → Security → Untrusted software → Allow untrusted software" in the SailfishOS Settings app.
  2. Download the current Storeman Installer RPM from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest), [OpenRepos.net](https://openrepos.net/content/olf/storeman-installer) or [the SailfishOS-OBS](https://build.merproject.org/package/show/home:olf:harbour-storeman/harbour-storeman-installer).
  3. Tap on the "File downloaded" notification on your SailfishOS device or select the downloaded RPM file in a file-manager app and choose "Install" in its pulley menu; then confirm the installation.
  4. Preferably disable "Allow untrusted software" again.

* Installation via Storeman (i.e., updating from Storeman < 0.2.9)
  1. Search for *Installer*
  2. Select the *Storeman Installer* by *olf*<br />
     <sub>Side note: If you select the outdated *Storeman Installer* by *osetr*, that will install an outdated *Storeman*, with which you can install a recent *Storeman*; save yourself this indirection and potential issues with software which was never tested on recent SailfishOS releases by installing a recent *Storeman Installer* by *olf*.</sub>
  3. You need to enable *olf*'s repository in the top pulley menu, if you did not enable it before.
  4. Install *Storeman Installer*

* Installation via SailfishOS:Chum
  1. Search for *Installer* in "Applications"
  2. Select *Storeman Installer*
  3. Install *Storeman Installer*

### Features of Storeman Installer

* The Storeman Installer is automatically removed ("uninstalled") when Storeman is being installed.
* [Storeman Installer 1.3.1](https://github.com/storeman-developers/harbour-storeman-installer/releases/tag/1.3.1) and all later versions are offered as an update candidate for Storeman, if an RPM repository is enabled, which offers the *harbour-storeman-installer* package and Storeman (*harbour-storeman* package) < 0.2.99 is already installed.
* Installing [Storeman Installer 1.3.1](https://github.com/storeman-developers/harbour-storeman-installer/releases/tag/1.3.1) and all later versions also automatically removes an installed Storeman (*harbour-storeman* package) < 0.2.99, which eliminates the former need to manually remove ("uninstall") an old Storeman. 
* [Storeman Installer 1.3.8](https://github.com/storeman-developers/harbour-storeman-installer/releases/tag/1.3.8) and all later versions create a persistent log file `/var/log/harbour-storeman-installer.log.txt`.
* Storeman Installer 2 runs "unattended": I.e., without any manual steps, after its installation has been triggered, until Storeman is installed.
* Storeman Installer is slow, because it calls `pkcon` two (versions before v1.3.8) to three times (releases after v[1.3.8](https://github.com/storeman-developers/harbour-storeman-installer/releases/tag/1.3.8), which acts quite slowly.  The minimal run time for Storeman Installer 2 is about 7 seconds, the typical run time is rather 10 seconds (measured from the moment Storeman Installer's installation has been triggered, until ultimately Storeman is installed).  This is already a lot, but I rarely experienced a stalled Packagekit daemon (for which `pkcon` is just a command line frontend, communicating with the daemon via D-Bus) during heavy testing, which can be observed with the crude `pkmon` utility (`Ctrl-C` gets you out :wink:), so Storeman Installer now tries to detect these "hangs" and to counter them: If that happens its run time can be up to slightly more than 1 minute.  In the worst case a stalled PackakgeKit daemon (and with it its `pkcon` client process(es)) stalls Storeman Installer, until the PackageKit daemon reaches its idle time out of 300 seconds (5 minutes; this could thoretically happen three times, resulting in a likely unsuccessful run time of more than 15 minutes)).
* You can follow Storeman Installer's actions with a `tail -f /var/log/harbour-storeman-installer.log.txt`, but mind that this file has to exist before telling `tail` to read it.  Storeman Installer will create this log file during its installation, but here you want to start the `tail -f` right *before* that happens.  This can be easly achieved by
`[defaultuser@sailfishos ] devel-su`
`[root@sailfishos ] touch /var/log/harbour-storeman-installer.log.txt`
`[root@sailfishos ] chmod 0664 /var/log/harbour-storeman-installer.log.txt`
`[root@sailfishos ] chhgrp ssu /var/log/harbour-storeman-installer.log.txt`
Open another termial window on or ssh session to your device an execute:
`[defaultuser@sailfishos ] tail -f /var/log/harbour-storeman-installer.log.txt`
Then return to the first terminal window or ssh session:
`[root@sailfishos ] pkcon --install-local <path/to/downloaded/harbour-storeman-installer-?.?.?-release*.noarch.rpm>`  # Insert real values for `?` (a single arbitrary character) and `*` (multiple arbitrary characters).
If you have already enabled a package repository, which offers Storeman Installer (e.g. OpenRepos/olf or SailfischOS:Chum), a simpler command works, without manually downloading the *harbour-storeman-installer* RPM package:
`[root@sailfishos ] pkcon install harbour-storeman-installer`
BTW, you can list all installed or online available (but not instaled) Storeman-related packages by issueing:
`[defaultuser@sailfishos ] pkcon search name storeman`
 
