#!/bin/bash

# Get the directory of the script
CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

INTERNAL_DATA_DIR="orthanc_receiver_agent_data"
if [ ! -d "${INPUT_DIR}" ]; then
  mkdir -p "${INTERNAL_DATA_DIR}"
fi

# Default values
IMAGE_LABEL="orthanc_receiver_agent"
IMAGE_TAG="${IMAGE_LABEL}:latest"
DOCKERFILE_NAME="Dockerfile_OrthancReciever"

docker build --tag "${IMAGE_TAG}" --label "${IMAGE_LABEL}" --file "${DOCKERFILE_NAME}" "$(pwd)"

docker run --rm \
-v "${INTERNAL_DATA_DIR}":/data \
"${IMAGE_TAG}"

#docker run "${IMAGE_TAG}"
