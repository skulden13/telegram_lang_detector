#!/usr/bin/env bash

set -euo pipefail

deploy_env_file="${DEPLOY_ENV_FILE:-.env.deploy}"

if [[ -f "$deploy_env_file" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$deploy_env_file"
    set +a
fi

required_variables=(
    DEPLOY_SSH_USER
    DEPLOY_SSH_HOST
    DEPLOY_SSH_KEY
    DEPLOY_REMOTE_DIR
)

for variable_name in "${required_variables[@]}"; do
    if [[ -z "${!variable_name:-}" ]]; then
        echo "Missing required environment variable: $variable_name" >&2
        exit 1
    fi
done

deploy_ssh_key="${DEPLOY_SSH_KEY/#\~/$HOME}"

if [[ ! -f "$deploy_ssh_key" ]]; then
    echo "SSH key not found: $deploy_ssh_key" >&2
    exit 1
fi

printf -v remote_dir_quoted '%q' "$DEPLOY_REMOTE_DIR"

ssh \
    -i "$deploy_ssh_key" \
    -o IdentitiesOnly=yes \
    "${DEPLOY_SSH_USER}@${DEPLOY_SSH_HOST}" \
    "cd -- $remote_dir_quoted && git pull --rebase && docker compose up -d --build"
