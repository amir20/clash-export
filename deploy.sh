#!/usr/bin/env bash

msg() {
    printf "\033[1;32m%s\n\033[0m" "$1"
}

set -e

msg "Updating docker-machine to clash..."
eval $(docker-machine env --shell bash clash-vultr)

msg "Deploying with docker..."
docker-compose -f docker-compose.yml up -d --build

msg "Success."
