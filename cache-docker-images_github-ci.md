# Caching docker images for CI runs at GitHub

## Issue description

If a CI configuration (i.e., a "GitHub action") requires a docker image to run, it downloads such images for each CI run.  These repeated downloads of docker images, which are often hundreds of megabytes to gigabytes large, significantly slow down each CI run and consume vast amounts of network bandwith.

### Specific issue

Specifically, using the SailfishOS-SDK images provided by Coderus for a CI run results in downloading [a docker image between ~ 1 GB and ~ 4 GB in size](https://hub.docker.com/r/coderus/sailfishos-platform-sdk/tags) (depending on the SDK / SailfishOS version to build for) up to three times (once for each of the supported architectures: aarch64, armv7hl and i486) from an external "docker registry" (here: [Docker Hub](https://hub.docker.com/))).
