# Caching docker images for CI runs at GitHub

## Issue description

If a CI configuration (i.e., a "GitHub action") requires a docker image to run, it downloads such images for each CI run.  These repeated downloads of docker images, which are often hundreds of megabytes to gigabytes large, significantly slow down each CI run and consume vast amounts of network bandwidth.

### Specific issue

Specifically, using the Sailfish-SDK images provided by Coderus for a CI run results in downloading [a docker image between 1 GB and 3,5 GB in size](https://hub.docker.com/r/coderus/sailfishos-platform-sdk/tags) (depending on the SDK / SailfishOS version to build for) up to three times (once for each of the supported architectures: aarch64, armv7hl and i486) from an external "docker registry" (here: [Docker Hub](https://hub.docker.com/)).  This affects the [simple variant of using these images](https://github.com/storeman-developers/harbour-storeman-installer/blob/master/.github/workflows/build.yml#L24) (by directly using the [`coderus/github-sfos-build` "action"](https://github.com/CODeRUS/github-sfos-build)) and [the more sophisticated one](https://github.com/sailfishos-patches/patchmanager/blob/master/.github/workflows/build.yml#L34) alike.

## Issue analysis

### Initial assessment

Caching "locally" means, with the measure(s) provided at GitHub, e.g., GitHub "actions".  Ultimately all these solutions use [GitHub's `action/cache`](https://github.com/actions/cache), which provides (as of 2023) 10 GB of cache, expiring cached items [LRU based](https://en.wikipedia.org/wiki/Cache_replacement_policies#LRU) or when an item was not accessed for a week.  But as some research shows, there are many variants and indirections how to utilise GitHub's `action/cache`.

### Alternative solutions

Other "solutions", as an external, caching proxy server, are implicitly not very effective.

Reducing the size of docker images is always a valid approach, has some potential (many docker images carry large amounts of unnecessary cruft), but is time consuming and futile, as the creation and distribution of such images are inviting to a "quick & dirty" approach (i.e., they are much quicker and easier to create and distribute than optimised).

The only real alternative solution is to host container images "locally" at GitHub, i.e., at [GitHub's container registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).  For an introduction, see GitHub's documentation for [creating, managing and distributing "GitHub packages"](https://docs.github.com/en/packages).

### Basic properties of GitHub's `action/cache`

* The [`action/cache`](https://github.com/actions/cache) seems to be implicitly run in the context of the user `runner`.  While a `sudo su` executed as part of a `run:` statement is effective for subsequent shell commands (tested with the Ubuntu-Linux runner environment provided by GitHub in 2023), I have not found a way to let an "action" run in a different user context.

* The `action/cache` only accepts download targets (i.e., local paths) to be configured as items to cache, not download sources.

* These first two properties of GitHub's `action/cache` prevent to simply cache the images downloaded by the local docker instance, usually (in 2023) [in `/var/lib/docker/overlay2/`](https://www.freecodecamp.org/news/where-are-docker-images-stored-docker-container-paths-explained/#docker-images) on Linux (utilising [overlayfs](https://www.kernel.org/doc/Documentation/filesystems/overlayfs.txt)), because `/var/lib/docker` and all its sub-directories are assigned to the user and group `root` and provide no access for others.  Adding the user `runner` to the group `root` does not help, because this only provides search permission in directories (i.e., the `x` bit is set for directories), but still no access to the files in `/var/lib/docker/[<storage-driver>](https://docs.docker.com/storage/storagedriver/overlayfs-driver/)/`.

* The `action/cache` only caches items used in a *successful* CI run.  Sometimes it makes sense to always cache items, which are known be independent of the outcome of a CI run, e.g., classic prerequisites for it; exactly what the Sailfish-SDK images constitute for building software for SailfishOS at GitHub.
  
  Others have also noticed that long ago and trivially patched the original `action/cache` (e.g., [[1]](https://github.com/actions/cache/compare/main...pat-s:always-upload-cache:main#diff-1243c5424efaaa19bd8e813c5e6f6da46316e63761421b3e5f5c8ced9a36e6b6L24-R24), [[2]](https://github.com/actions/cache/compare/master...gerbal:always-cache:master#diff-1243c5424efaaa19bd8e813c5e6f6da46316e63761421b3e5f5c8ced9a36e6b6L21-R21)), but very often this ultimately results in stale forks.  Hence [applying this trivial change by "live patching"](https://github.com/mxxk/gh-actions-cache-always) is the only maintainable solution, which resulted in [an improved version of the "live patching" approach](https://github.com/actions/cache/issues/92#issuecomment-1263067512).
  
  ~~Unfortunately~~ GitHub has ~~not~~ provided a way to adjust this behaviour by a CI configuration, ~~despite~~ \[see\] [issue \#92](https://github.com/actions/cache/issues/92) (and subsequent issues [\#165](https://github.com/actions/cache/issues/165), [\#334](https://github.com/actions/cache/issues/334) etc.) has been filed for GitHub's `action/cache` long ago.<br />
  *Edit:* [Mostly solved](https://github.com/actions/cache/discussions/1020) by the initial release of `actions/cache/save` and `actions/cache/restore` in December 2022; although [this extension of the original `action/cache`](https://github.com/MartijnHols/actions-cache) still provides a larger feature set and is structurally analog to GitHub's new `actions/cache/save` and `actions/cache/restore`.  This is [now the recommended way of storing items in a cache](https://github.com/actions/cache/tree/main/save#always-save-cache), regardless if the whole action is sucessful or fails; still "live patching" GitHub's original `action/cache` to also cache when the job fails still has some appeal due to the simpler usage of `action/cache` compared to the new `action/cache/save` and `action/cache/restore`, which all three are now and continue to be maintained by GitHub.  As their basic properties are the same (except for this point), the remainder of this document can stay unchanged.
  
  <sup>Plan: Enhance and release [a "live patching" action, which downloads (actually: checks-out), patches and transparently maps to the locally patched version of the original `action/cache`](https://github.com/Olf0/always-cache), ultimately also to the GitHub Marketplace.</sup>

## Exploring the solution space

### Pre-download the container images

The most trivial way to cope with `action/cache`'s access limitations is to pre-download images expicitly.  For this one creates a download directory by issuing `mkdir -p $GITHUB_WORKSPACE/<image-name>` (the `-p` is only used to prevent an error, when the dirctory already exists; `$GITHUB_WORKSPACE` resolves to `/home/runner/<repository-name>/<repository-name>` on Linux (yes, twice `<repository-name>`), GitHub calls this location "runner workspace", it is naturally also the initial PWD), download the image by some third party tool (the docker CLI commands do not allow for setting the download location), then execute a [`docker image load`](https://docs.docker.com/engine/reference/commandline/image_load/) (or [`docker image import`](https://docs.docker.com/engine/reference/commandline/image_import/)) and ultimately continue as before  (e.g., instanciating and starting a docker container by [`docker run`](https://docs.docker.com/engine/reference/commandline/run/)).

Mind that the git repository is also checked out to the "runner workspace" (`$GITHUB_WORKSPACE`) as root directory, so do pay attention to not clobber any files or directories of your source repository.

#### Suitable tools for downloading docker images to arbitrary locations in the local file-system:

#### ● [`download-frozen-image-v2.sh`](https://github.com/moby/moby/blob/master/contrib/download-frozen-image-v2.sh) by the [Moby Project](https://mobyproject.org/)
* Its source code is [hosted at GitHub](https://github.com/moby/moby) and uses the Apache-2.0 license.
* Created and maintained as [a by-product](https://github.com/moby/moby/tree/v23.0.0-rc.1/contrib#readme) of a [lively project](https://github.com/moby/moby/pulse).
* Provides [tagged, stable releases](https://github.com/moby/moby/releases), e.g. (latest as of 2023-01-07), [v20.10.22](https://github.com/moby/moby/blob/v20.10.22/contrib/download-frozen-image-v2.sh).
* Is a simple and small shell-script (< 400 sloc, ~ 13 KBytes), which implicitly documents [how to call it](https://github.com/moby/moby/blob/v23.0.0-rc.1/contrib/download-frozen-image-v2.sh#L18-L22) and [how to utilise it](https://github.com/moby/moby/blob/v23.0.0-rc.1/contrib/download-frozen-image-v2.sh#L429-L431).
* My favorite third-party tool for this approach.

#### ● [Scopeo](https://github.com/containers/skopeo#readme) by the ["Containers" project](https://github.com/containers)
* Its source code is [hosted at GitHub](https://github.com/containers/skopeo) and uses the Apache-2.0 license.
* Created and maintained by a [lively project](https://github.com/containers/skopeo/pulse).
* Provides [tagged, stable releases](https://github.com/containers/skopeo/releases).
* Is a capable container image management utility written in Go, hence first needs to be compiled.

#### ● [storage](https://github.com/containers/storage#readme) also by the ["Containers" project](https://github.com/containers)
* Its source code is [hosted at GitHub](https://github.com/containers/storage) and uses the Apache-2.0 license.
* Created and maintained by a [lively project](https://github.com/containers/storage/pulse).
* Provides [tagged, stable releases](https://github.com/containers/storage/releases).
* Is a capable container storage management library written in Go, hence first needs to be compiled.
* Provides the [`containers-storage` CLI wrapper](https://github.com/containers/storage/tree/main/cmd/containers-storage#readme) for manual and scripting use.

#### ● [docker-drag](https://github.com/NotGlop/docker-drag) by [NotGlop](https://github.com/NotGlop)
* Its source code is [hosted at GitHub](https://github.com/NotGlop/docker-drag) and carries no license.
* Apparently unmaintained.
* Does not provide releases or git tags.
* Is a simple and small Python script (187 sloc, 7,3 KBytes), called [`docker_pull.py`](https://github.com/NotGlop/docker-drag/blob/master/docker_pull.py).

#### ● [docker_pull](https://github.com/ahdrr/docker_pull) by [ahdrr](https://github.com/ahdrr)
* Its source code is [hosted at GitHub](https://github.com/ahdrr/docker_pull) and carries no license.
* Created in 2022.
* Does provide two releases (as of 2023-01-07) and git tags.
* Written in Go, [pre-compiled versions are 11,6 MBytes large](https://github.com/ahdrr/docker_pull/releases).
* Inspired by / an implementation in Go of *docker-drag*, the tool discussed one bullet point above.
* `http` only?

### Use an "action", which utilises `action/cache` 

#### Suitable "actions" to cache downloaded docker images:

#### ● [HTTP Cache Proxy](https://github.com/marketplace/actions/http-cache-proxy) by [Cirrus Labs](https://github.com/cirruslabs)
* Its source code is [hosted at GitHub](https://github.com/cirruslabs/http-cache-action) and uses the MIT license.
* Does provide two releases (as of 2023-01-07) and two corresponding git tags.
* Written in Go.
* Not much used.
* Initially appeared to be an easy and elegant soultion, but …
* `http` only?

#### ● [Build docker images using cache](https://github.com/marketplace/actions/build-docker-images-using-cache) by [Juan Abadie (whoan)](https://github.com/whoan)
* Its source code is [hosted at GitHub](https://github.com/whoan/docker-build-with-cache-action) and uses the MIT license.
* Does provide stable releases and git tags (lots!).
* Written in bash, heavily uses bash specific features.
* Small, the two bash scripts summarised are < 600 sloc, < 15 KBytes.
* Aimed at a different purpose: To cache docker images which are needed for building an own image.
* Initially appeared to be (ab)usable for solely caching the download of docker images, but a little analysis shows, that one would have to dissect the main bash script and adapt it for this purpose: Currently a `docker build` call is unavoidable.

#### ● [Cached Docker Build](https://github.com/marketplace/actions/cached-docker-build) by [Matt Kadenbach (mattes)](https://github.com/mattes)
* Its source code is [hosted at GitHub](https://github.com/mattes/cached-docker-build-action) and uses the Unlicense license.
* Does provide two releases (as of 2023-01-07) and git tags.
* Written in JavaScript.
* Small, summarised < 700 sloc, < 25 KBytes.
* Appears to be unmaintained.
* Nobody seems to use it.
* Appears to be easier to (ab)use for only caching the downloaded docker images than *Build docker images using cache* (discussed one bullet point above).

#### ● [cached-dependencies](https://github.com/marketplace/actions/cached-dependencies) by [Jesse Yang (ktmud)](https://github.com/ktmud)
* Its source code is [hosted at GitHub](https://github.com/ktmud/cached-dependencies) and uses the MIT license.
* Does provide a single git tag.
* Written in TypeScript (Microsoft's superset of JavaScript).
* Smallish, < 100 KBytes.
* Appears to be unmaintained.
* Appears to be a generic caching solution for pulling external dependencies.
* States to be adaptable, includes cache configurations for `pip`, `npm` and `yarn`.
* Despite [extensive documentation](https://github.com/ktmud/cached-dependencies#readme), I fail to quickly comprehend:
  * How to configure a different source (Docker Hub).
  * If it is also limited to downloads in the runner's "workspace".
* Pulled (?) from the "GitHub marketplace" 2023-01-08, see [github.com/marketplace/actions/cached-dependencies](https://github.com/marketplace/actions/cached-dependencies).  2023-01-07 it was still there and is still [found via the search](https://github.com/marketplace?type=actions&query=cached-+)?
  
#### ● [Docker Cache](https://github.com/marketplace/actions/docker-cache) by [ScribeMD](https://github.com/ScribeMD)
* Its source code is [hosted at GitHub](https://github.com/ScribeMD/docker-cache) and uses the MIT license.
* Does provide stable releases and git tags (lots!).
* Comprises a [few TypeScript scripts](https://github.com/ScribeMD/docker-cache/tree/main/src) (Microsoft's superset of JavaScript), which are compiled into two JavaScript scripts ([main/index.js](https://github.com/ScribeMD/docker-cache/blob/main/dist/main/index.js) and [post/index.js](https://github.com/ScribeMD/docker-cache/blob/main/dist/post/index.js)) each 1,17 MiB large (!), plus a tiny [action.yaml](https://github.com/ScribeMD/docker-cache/blob/main/action.yaml) file which calls these.
* Appears to be well maintained.
* Appears to be a generic caching solution for Docker images.
* Explicitly denotes the use case "pull images from Docker Hub"!

#### ● [Rootless Docker](https://github.com/marketplace/actions/rootless-docker) also by [ScribeMD](https://github.com/ScribeMD)
* Its source code is [hosted at GitHub](https://github.com/ScribeMD/rootless-docker) and uses the MIT license.
* Does provide stable releases and git tags (lots!).
* A small, well readable [action.yaml](https://github.com/ScribeMD/rootless-docker/blob/main/action.yaml) file.
* Tiny: 2,65 KBytes
* [Downloads and executes](https://github.com/ScribeMD/rootless-docker/blob/main/action.yaml#L48-L55) directly [`https://get.docker.com/rootless` shell script](https://get.docker.com/rootless) (some 10 KBytes).
* Appears to be well maintained.
* States to provide a set of advantages over running docker conventionally in root mode.
* Renders any specific caching moot, as GitHub's `action/cache` suffices.

## Down-selection of possible solutions to try

1. [Rootless Docker](https://github.com/marketplace/actions/rootless-docker): https://github.com/ScribeMD/rootless-docker
2. [Docker Cache](https://github.com/marketplace/actions/docker-cache): https://github.com/ScribeMD/docker-cache
3. [`download-frozen-image-v2.sh`](https://github.com/moby/moby/blob/master/contrib/download-frozen-image-v2.sh): https://github.com/moby/moby/tree/master/contrib#readme
