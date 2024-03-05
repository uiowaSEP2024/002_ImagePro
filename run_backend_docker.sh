#!/bin/bash

# Define variables
IMAGE_TAG="job_monitoring_app_backend:latest"
CONTAINER_NAME="job_monitoring_app_backend"

# Run the docker container
docker run -d --name "${CONTAINER_NAME}" -p 8000:8000 -e APP_ENV=development "${IMAGE_TAG}"
