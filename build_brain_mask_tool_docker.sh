# Define variables
DOCKERFILE_NAME="Dockerfile_BrainMaskTool"
IMAGE_TAG="brainmasktool:v0.1"
IMAGE_LABEL="brainmasktool"

# Build the docker image for the brain mask tool
docker build --tag $IMAGE_TAG --label $IMAGE_LABEL --file $DOCKERFILE_NAME $(pwd)
