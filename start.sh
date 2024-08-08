#!/usr/bin/env bash

if [ "$1" = -h ]; then
  echo "Usage: $0 [clean]"
  exit 1
fi

sudo ss -lptn 'sport = :8080' | kill $(awk '{print $6}' | cut -d, -f1 | cut -d= -f2)

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="$(basename "${PROJECT_DIR}")"

# stop previous running containers
if [ -n "$(docker ps -a | grep "${PROJECT_NAME}")" ]; then
  docker ps -a | grep "${PROJECT_NAME}" | awk '{print $1}' | xargs docker stop
fi

# remove previous containers
if [ -n "$(docker ps -a | grep "${PROJECT_NAME}")" ] && [ "$1" == "clean" ]; then
  docker ps -a | grep "${PROJECT_NAME}" | awk '{print $1}' | xargs docker rm
  docker image ls | grep "${PROJECT_NAME}" | awk '{print $3}' | xargs docker rmi
fi

set -euo pipefail

# check is there a docker-compose command, if not, use "docker compose" instead.
if [ -x "$(command -v docker-compose)" ]; then
    dc=docker-compose
else
    dc="docker compose"
fi

export AIRFLOW_PROJ_DIR="${PROJECT_DIR}/monorepo/airflow"
export AIRFLOW_COMPOSE_FILE="${AIRFLOW_PROJ_DIR}/docker-compose.yml"

if [ ! -f "${AIRFLOW_PROJ_DIR}/.env" ]; then
  echo -e "AIRFLOW_UID=$(id -u)" > "${AIRFLOW_PROJ_DIR}/.env"
  echo -e "AIRFLOW_GID=0" >> "${AIRFLOW_PROJ_DIR}/.env"
fi

if [ ! -n "$(docker image ls | grep "${PROJECT_NAME}-airflow")" ]; then
  docker build -t "${PROJECT_NAME}-airflow" "${AIRFLOW_PROJ_DIR}"
  export AIRFLOW_IMAGE_NAME="${PROJECT_NAME}-airflow"
fi

${dc} -p "${PROJECT_NAME}" -f "${AIRFLOW_COMPOSE_FILE}" up -d 

export KAFKA_PROJ_DIR="${PROJECT_DIR}/monorepo/kafka"
export KAFKA_COMPOSE_FILE="${KAFKA_PROJ_DIR}/docker-compose.yml"

${dc} -p "${PROJECT_NAME}" -f "${KAFKA_COMPOSE_FILE}" up -d 
