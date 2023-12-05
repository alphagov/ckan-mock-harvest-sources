#!/bin/bash

set -eux

build () {
  if [ "${ARCH}" = "amd64" ]; then
    docker build . -t "ghcr.io/alphagov/dynamic-${APP}:${1}" -f "dynamic/Dockerfile"
    docker build . -t "ghcr.io/alphagov/static-${APP}:${1}" -f "static/Dockerfile"
  else
    docker buildx build --platform "linux/${ARCH}" . -t "ghcr.io/alphagov/dynamic-${APP}:${1}" -f "dynamic/Dockerfile"
    docker buildx build --platform "linux/${ARCH}" . -t "ghcr.io/alphagov/static-${APP}:${1}" -f "static/Dockerfile"
  fi
}

DOCKER_TAG="${GITHUB_SHA}"

if [[ -n ${GH_REF:-} ]]; then
  DOCKER_TAG="${GH_REF}"
fi

build "${DOCKER_TAG}"

if [[ -n ${DRY_RUN:-} ]]; then
  echo "Dry run; not pushing to registry"
else
  docker push "ghcr.io/alphagov/dynamic-${APP}:${DOCKER_TAG}"
  docker push "ghcr.io/alphagov/static-${APP}:${DOCKER_TAG}"
fi
