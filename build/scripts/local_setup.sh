# /bin/bash

export BUILD_DIR=$(dirname "$(pwd)")
export ROOT_DIR=$(dirname "$BUILD_DIR")

docker compose -f "$BUILD_DIR/composers/Docker-compose.yaml" down
docker compose -f "$BUILD_DIR/composers/Docker-compose.yaml" up -d