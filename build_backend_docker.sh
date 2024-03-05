#!/bin/bash

# Define variables
DOCKERFILE_NAME="Dockerfile_Backend"
IMAGE_LABEL="job_monitoring_app_backend"
IMAGE_TAG="${IMAGE_LABEL}:latest"


# Build the docker image for the backend
docker build --tag "${IMAGE_TAG}" --label "${IMAGE_LABEL}" --file "${DOCKERFILE_NAME}" "$(pwd)"
