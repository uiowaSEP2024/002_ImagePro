#!/bin/bash
# Define variables
DOCKERFILE_NAME="Dockerfile_BrainMaskTool_light"
IMAGE_TAG="brainmasktool_light:v0.1"
IMAGE_LABEL="brainmasktool_light"
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=325852638497
REPOSITORY_NAME="fargate_test"

# Build the docker image for the brain mask tool
docker build --tag "${IMAGE_TAG}" --label "${IMAGE_LABEL}" --file "${DOCKERFILE_NAME}" .

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
