# Caching docker images for CI runs at GitHub

## Issue description

If a CI configuration (i.e., a "GitHub action") requires a docker image to run, it downloads such images for each CI run.  These repeated downloads of docker images, which are often hundreds of megabytes to gigabytes large, significantly slow down each CI run and consume vast amounts of network bandwidth.

### Specific issue

Specifically, using the Sailfish-SDK images provided by Coderus for a CI run results in downloading [a docker image between 1 GB and 3,5 GB in size](https://hub.docker.com/r/coderus/sailfishos-platform-sdk/tags) (depending on the SDK / SailfishOS version to build for) up to three times (once for each of the supported architectures: aarch64, armv7hl and i486) from an external "docker registry" (here: [Docker Hub](https://hub.docker.com/)).  This affects the [simple variant of using these images](https://github.com/storeman-developers/harbour-storeman-installer/blob/master/.github/workflows/build.yml#L24) (by directly using the [`coderus/github-sfos-build` "action"](https://github.com/CODeRUS/github-sfos-build)) and [the more sophisticated one](https://github.com/sailfishos-patches/patchmanager/blob/master/.github/workflows/build.yml#L34) alike.

## Issue analysis

### Initial assessment

Caching "locally" means, with the measure(s) provided at GitHub, e.g., GitHub "actions".  Ultimately all these solutions use [GitHub's "action" `cache`](https://github.com/actions/cache), which provides 10 GB of cache, expiring its content when unaccessed for a week.  But as some research shows, there are many variants and indirections how to utilise this `cache` "action".

### Alternative solutions

Other "solutions", as an external, caching proxy server, are implicitly not very effective.

Reducing the size of the docker images used is always a valid approach, has some potential (many docker images carry large amounts of unnecessary cruft), but is time consuming and futile, as the creation and distribution of such images are inviting to a "quick & dirty" approach (i.e., they way quicker and easier to create and distributed than optimised).

The only real alternative solution is to host the images "locally" at GitHub, i.e. at [GitHub's container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).  For an introduction, see GitHub's documentation for [creating, managing and distributing "GitHub packages"](https://docs.github.com/en/packages).

### Properties of GitHub's "action" `cache`

* The ["action" `cache`](https://github.com/actions/cache) seems to be implicitly run in the context of the user `runner`.  While a `sudo su` executed as part of a `run:` statement is effective for subsequent shell commands (tested with the Ubuntu-Linux runner environment provided by GitHub in 2023), I have not found a way to let an "action" run in a different user context.

* The "action" `cache` only accepts download targets (i.e., local paths) to be configured as items to cache, not download sources.

* The first two properties of GitHub's "action" `cache` prevent to simply cache the images downloaded by the local docker instance, usually (in 2023) [in `/var/lib/docker/overlay2/`](https://www.freecodecamp.org/news/where-are-docker-images-stored-docker-container-paths-explained/#docker-images).

