# Storeman Installer

**The Storeman Installer for SailfishOS performs the initial installation of the [Storeman OpenRepos client application](https://github.com/storeman-developers/harbour-storeman-installer). Storeman Installer selects, downloads and installs the correct variant of the Storeman application built for the CPU-architecture of the device and the installed SailfishOS release from the SailfishOS-OBS.**

### Background

Starting with version 0.2.9, Storeman is built by the help of the SailfishOS-OBS and initially installed by the Storeman Installer (or manually).  To update from Storeman < 0.2.9, one must remove ("uninstall") Storeman *before* installing the Storeman Installer or manually installing Storeman ≥ 0.2.9.  After an initial installation of Storeman ≥ 0.2.9, further updates of Storeman will be performed within Storeman, as usual. 

The Storeman Installer works on any SailfishOS release and CPU-architecture, though the recent Storeman releases only support SailfishOS ≥ 3.1.0.  The current Storeman Installer can be obtained from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest).

If you use the SailfishOS:Chum community repository, e.g., via [the SailfishOS:Chum GUI application](https://chumrpm.netlify.app/), you can download and install Storeman from there, without the indirection via Storeman Installer.

The current Storeman proper can be obtained for manual installation from [Storeman's releases section at GitHub](https://github.com/storeman-developers/harbour-storeman/releases); the RPMs of older Storeman releases are also available there.

### Important notes

* If you have any troubles with installing, removing or updating packages after a SailfishOS upgrade, try running `devel-su pkcon refresh` in the terminal app.
* An OBS "download on demand (DoD)" repository must be created by Jolla for every SailfishOS release, before software can be built for a SailfishOS release.  It often takes some time after a new SailfishOS release before the correspondig "DoD" OBS-repository is being made available.  If you want to install or update Storeman in this situation, Storeman Installer and Storeman's self-updating will fail, hence one has to either manually set the last prior SailfishOS release in the SailfishOS:Chum GUI application or fully manually download and install or update Storeman; this is always true for users of "closed beta (cBeta)" and "early access (EA)" releases of SailfishOS.  
* Disclaimer: Storeman and Storeman Installer may still have flaws, kill your kittens or break your SailfishOS installation!  Although this is very unlikely after years of testing by many users, new flaws may be introduced in any release (as for any software).  Be aware, that the license you implicitly accept by using Storeman excludes any liability.

### Installation instructions

* Enable "System → Security → Untrusted software → Allow untrusted software" in the SailfishOS Settings app.
* Download the current Storeman Installer from [its "latest release" page at GitHub](https://github.com/storeman-developers/harbour-storeman-installer/releases/latest) or any other way described in the section "[Background](#background)".
* Tap on the "File downloaded" notification on your SailfishOS device or select the downloaded RPM file in a file-manager app and select "Install" in its pulley menu; then confirm the installation.
* Preferrably disable "Allow untrusted software" again.
* Tap on the "Storeman Installer" icon in the device's app grid ("launcher") and wait until the Storeman installation finishes - the "Storeman Installer" icon should be replaced by the icon of Storeman proper, even though the icons look the same, their text is different.
* The Storeman Installer is automatically removed ("uninstalled") when Storeman is installed.
