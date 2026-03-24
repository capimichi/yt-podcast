#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
ENV_FILE="$PROJECT_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
  printf 'Missing .env file at %s\n' "$ENV_FILE" >&2
  exit 1
fi

read_env_value() {
  key="$1"
  value=$(grep -E "^${key}=" "$ENV_FILE" | tail -n 1 | cut -d '=' -f 2-)
  printf '%s' "$value"
}

DEPLOY_USERNAME=$(read_env_value DEPLOY_USERNAME)
DEPLOY_HOST=$(read_env_value DEPLOY_HOST)
DEPLOY_PORT=$(read_env_value DEPLOY_PORT)
DEPLOY_PATH=$(read_env_value DEPLOY_PATH)

: "${DEPLOY_USERNAME:?Missing DEPLOY_USERNAME in .env}"
: "${DEPLOY_HOST:?Missing DEPLOY_HOST in .env}"
: "${DEPLOY_PORT:?Missing DEPLOY_PORT in .env}"
: "${DEPLOY_PATH:?Missing DEPLOY_PATH in .env}"

REMOTE_COMMAND=$(cat <<EOF
set -eu
cd "$DEPLOY_PATH"
git pull --ff-only origin master
if [ -f docker-compose.override.yml ]; then
  docker compose -f docker-compose.yml -f docker-compose.override.yml up -d --build
elif [ -f compose.override.yml ]; then
  docker compose -f docker-compose.yml -f compose.override.yml up -d --build
else
  docker compose up -d --build
fi
EOF
)

ssh -p "$DEPLOY_PORT" "$DEPLOY_USERNAME@$DEPLOY_HOST" "$REMOTE_COMMAND"
