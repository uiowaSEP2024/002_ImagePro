source aws_common_resources.sh

# Get the directory of the script
CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PARENT_DIR_2X_UP="$(dirname $(dirname ${CURRENT_DIR}))"
echo "Parent directory: ${PARENT_DIR_2X_UP}"

# TODO Make these variables be dynamically set based on inputs from the user
DOCKERFILE_NAME="Dockerfile_Frontend_aws"
IMAGE_TAG="frontend_test"
IMAGE_LABEL="frontend"
CONTEXT_DIR="${PARENT_DIR_2X_UP}"

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
