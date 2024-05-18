#!/usr/bin/env bash

set -ex

# Arguments:
#
# 1: registry, name, and tag of base image
# 2: registry, name, and tag of image to be created
# 3: name of Python distribution produced by this repo

scriptdir=$(realpath "$(dirname "${BASH_SOURCE[0]}")")
# source directory must be mounted at the same path inside the build
# container as it will be mounted when GitHub Actions launches the
# container, because Hatch uses the path as part of the identity of
# the virtual environments it creates
containersrcdir="/__w/${GITHUB_REPOSITORY##*/}/${GITHUB_REPOSITORY##*/}"
base_image=${1}; shift
image_name=${1}; shift
dist_name=${1}; shift

lint_deps=(shellcheck)
proj_deps=()
proj_build_deps=()

hatchenvs=(lint ci)

c=$(buildah from "${base_image}")

build_cmd() {
    buildah run --network host "${c}" -- "$@"
}

build_cmd_with_source() {
    buildah run --network host --volume "$(realpath "${scriptdir}/.."):${containersrcdir}" --workingdir "${containersrcdir}" "${c}" -- "$@"
}

build_cmd apt update --quiet=2
build_cmd apt install --yes --quiet=2 "${lint_deps[@]}" "${proj_deps[@]}" "${proj_build_deps[@]}"

for env in "${hatchenvs[@]}"; do
    # this looks weird... but it causes Hatch to create the env,
    # install all of the project's dependencies and the project,
    # then runs 'uv pip' to uninstall the project, leaving the env
    # in place with the dependencies
    build_cmd_with_source hatch env create "${env}"
    build_cmd_with_source hatch -e "${env}" run uv pip uninstall "${dist_name}"
done

if [ -n "${proj_build_deps[*]}" ]
then
    build_cmd apt remove --yes --purge "${proj_build_deps[@]}"
fi
build_cmd apt autoremove --yes --purge
build_cmd apt clean autoclean
build_cmd sh -c "rm -rf /var/lib/apt/lists/*"
build_cmd uv cache clean

if buildah images --quiet "${image_name}"; then
    buildah rmi "${image_name}"
fi
buildah commit --squash --rm "${c}" "${image_name}"
