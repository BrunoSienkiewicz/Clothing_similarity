#!/usr/bin/env bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "${PROJECT_DIR}")"

# stop previous running containers
if [ -n "$(docker ps -a | grep "${PROJECT_NAME}")" ]; then
  docker ps -a | grep "${PROJECT_NAME}" | awk '{print $1}' | xargs docker stop
fi
