# /bin/bash


BUILD_DIR=$(dirname "$(pwd)")
ROOT_DIR=$(dirname "$BUILD_DIR")

docker build -f "$BUILD_DIR/dockerfiles/Dockerfile" -t local-trading-analytics:latest "$ROOT_DIR/backend/."