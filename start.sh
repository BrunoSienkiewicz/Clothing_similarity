#!/usr/bin/env bash

if [ "$1" = -h ]; then
  echo "Usage: $0 [clean]"
  exit 1
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "${PROJECT_DIR}")"

# stop previous running containers
docker ps -a | grep "${PROJECT_NAME}" | awk '{print $1}' | xargs docker stop

# remove previous containers
if [ -n "$(docker ps -a | grep "${PROJECT_NAME}")" ] && [ "$1" == "clean" ]; then
  docker ps -a | grep "${PROJECT_NAME}" | awk '{print $1}' | xargs docker rm
fi

set -euo pipefail

# check is there a docker-compose command, if not, use "docker compose" instead.
if [ -x "$(command -v docker-compose)" ]; then
    dc=docker-compose
else
    dc="docker compose"
fi

export AIRFLOW_PROJ_DIR="${PROJECT_DIR}/monorepo/airflow"
export AIRFLOW_COMPOSE_FILE="${AIRFLOW_PROJ_DIR}/airflow.compose.yml"

if [ ! -f "${AIRFLOW_PROJ_DIR}/.env" ]; then
  echo -e "AIRFLOW_UID=$(id -u)" > "${AIRFLOW_PROJ_DIR}/.env"
  echo -e "AIRFLOW_GID=0" >> "${AIRFLOW_PROJ_DIR}/.env"
fi

${dc} -p "${PROJECT_NAME}" -f "${AIRFLOW_COMPOSE_FILE}" up -d
