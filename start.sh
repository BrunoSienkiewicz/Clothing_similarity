#!/usr/bin/env bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

set -euo pipefail

# check is there a docker-compose command, if not, use "docker compose" instead.
if [ -x "$(command -v docker-compose)" ]; then
    dc=docker-compose
else
    dc="docker compose"
fi

export COMPOSE_FILE="${PROJECT_DIR}/docker-compose.yaml"
if [ $# -gt 0 ]; then
    exec $dc run --rm airflow-cli "${@}"
else
    exec $dc run --rm airflow-cli
fi
