#!/usr/bin/env bash

msg() {
    printf "\033[1;32m%s\n\033[0m" "$1"
}

set -e
msg "Building..."
docker-compose -f docker-compose.yml build 

msg "Pushing images..."
docker-compose -f docker-compose.yml push

msg "Updating docker-machine to clash..."
eval $(docker-machine env --shell bash clash)

msg "Deploying with docker..."
docker-compose -f docker-compose.yml pull
docker-compose -f docker-compose.yml up -d --remove-orphans

msg "Success."
