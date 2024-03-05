#!/bin/bash

# Define variables
DOCKERFILE_NAME="Dockerfile_BrainMaskTool_light"
IMAGE_TAG="brainmasktool_light:v0.1"
IMAGE_LABEL="brainmasktool_light"

# Build the docker image for the brain mask tool
docker build --tag "${IMAGE_TAG}" --label "${IMAGE_LABEL}" --file "${DOCKERFILE_NAME}" "$(pwd)"
