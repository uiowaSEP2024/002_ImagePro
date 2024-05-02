#!/bin/bash
source aws_common_resources.sh
CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Ask user what they want to build:
# 1. Frontend
# 2. Backend
# 3. Orthanc
# 4. Agent
# 5. Job Monitoring App
# 6. postgres
# 7. All

echo "Please select what you would like to build:"
echo "1. Frontend"
echo "2. Backend"

read -r BUILD_CHOICE

case $BUILD_CHOICE in
    1)
        echo "Building the frontend"
        # Build the frontend
        DOCKERFILE_NAME="frontend/Dockerfile_Frontend_aws"
        IMAGE_TAG="frontend_test"
        IMAGE_LABEL="frontend"
        CONTEXT_DIR="${CLUSTER_DIR}"
        ;;
    2)
        echo "Building the backend"
        # Build the backend
        DOCKERFILE_NAME="backend/Dockerfile_Backend_aws"
        IMAGE_TAG="backend_test"
        IMAGE_LABEL="backend"
        CONTEXT_DIR="${CLUSTER_DIR}"

        ;;
    *)
        echo "Invalid choice"
        ;;
esac

# Build the docker image for the brain mask tool
docker build --tag "${IMAGE_TAG}" --label "${IMAGE_LABEL}" --file "${DOCKERFILE_NAME}" "${CONTEXT_DIR}"

# If building for Kubernetes, tag the image with the ECR registry
BUILD_FOR_KUBERNETES=${BUILD_FOR_KUBERNETES:-"1"}
REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${REPOSITORY_NAME}"

if [ "$BUILD_FOR_KUBERNETES" = "1" ]; then
    # AWS ECR login
    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${REGISTRY}

    # Tag the image for ECR with a versioned tag
    docker tag "${IMAGE_TAG}" "${REGISTRY}:${IMAGE_TAG}"

    # Push the image to AWS ECR
    docker push "${REGISTRY}:${IMAGE_TAG}"
fi
