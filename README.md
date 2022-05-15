# Storeman Installer

**The Storeman Installer for SailfishOS performs the initial installation of the [Storeman OpenRepos client application](https://github.com/storeman-developers/harbour-storeman). Storeman Installer selects, downloads and installs the correct variant of the Storeman application built for the CPU-architecture of the device and the installed SailfishOS release from the SailfishOS-OBS.**

### Background

Starting with version 0.2.9, Storeman is built by the help of the SailfishOS-OBS and initially installed by the Storeman Installer (or manually).  To update from Storeman < 0.2.9, one must remove ("uninstall") Storeman *before* installing the Storeman Installer or manually installing Storeman ≥ 0.2.9.  After an initial installation of Storeman ≥ 0.2.9, further updates of Storeman will be performed within Storeman, as usual. 

The Storeman Installer works on any SailfishOS release ≥ 3.1.0 and all CPU-architectures.  The current Storeman Installer RPM can be obtained from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest), [OpenRepos](https://openrepos.net/content/olf/storeman-installer) and [the SailfishOS-OBS](https://build.sailfishos.org/package/show/home:olf:harbour-storeman/harbour-storeman-installer).

If you use the SailfishOS:Chum community repository, e.g., via [the SailfishOS:Chum GUI application](https://chumrpm.netlify.app/), you can install Storeman from there, without the indirection via Storeman Installer.

The current RPMs of Storeman proper can be obtained for manual installation from [Storeman's releases section at GitHub](https://github.com/storeman-developers/harbour-storeman/releases); the RPMs of older Storeman releases are also available there, e.g., v0.1.8 which works on SailfishOS 2.2.1.<br />
Alternatively the current RPMs of Storeman proper can be obtained from [the SailfishOS-OBS](https://build.sailfishos.org/project/show/home:olf:harbour-storeman).

### Important notes

* If you have any troubles with installing, removing or updating packages after a SailfishOS upgrade, try running `devel-su pkcon refresh` in the terminal app.
* Before software can be built for a SailfishOS release at the SailfishOS-OBS, Jolla must create a corresponding "download on demand (DoD)" OBS-repository.  It often takes some time after a new "general availability (GA)" SailfishOS release is published before the corresponding "DoD" repository is being made available, during which installing or updating Storeman by the Storeman Installer or Storeman's self-updating on a device with the new SailfishOS release already installed will fail; consequently this is always the case during the "closed beta (cBeta)" and "early access (EA)" phases of a new SailfishOS release.  Hence one has to either manually set the last prior SailfishOS GA release in the SailfishOS:Chum GUI application or manually download and install or update Storeman built for the last prior SailfishOS GA release, then.
* Disclaimer: Storeman and Storeman Installer may still have flaws, kill your kittens or break your SailfishOS installation!  Although this is very unlikely after years of testing by many users, new flaws may be introduced in any release (as for any software).  Be aware, that the license you implicitly accept by using Storeman excludes any liability.

### Installation instructions

* Enable "System → Security → Untrusted software → Allow untrusted software" in the SailfishOS Settings app.
* Download the current Storeman Installer RPM from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest), [OpenRepos](https://openrepos.net/content/olf/storeman-installer) or [the SailfishOS-OBS](https://build.sailfishos.org/package/show/home:olf:harbour-storeman/harbour-storeman-installer).
* Tap on the "File downloaded" notification on your SailfishOS device or select the downloaded RPM file in a file-manager app and choose "Install" in its pulley menu; then confirm the installation.
* Preferrably disable "Allow untrusted software" again.
* Tap on the "Storeman Installer" icon in the device's app grid ("launcher") and wait until the Storeman installation finishes - the "Storeman Installer" icon should be replaced by the icon of Storeman proper, even though the icons look the same, their text is different.
* The Storeman Installer is automatically removed ("uninstalled") when Storeman is being installed.
