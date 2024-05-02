#!/bin/bash


# Common Environment Variables for AWS Cluster
# This should allow us to dry out our scripts and only have to source this file

CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
CLUSTER_DIR="$(dirname "${CURRENT_DIR}")"

## PATHS FOR JOB MONITORING APP
JOB_MONITORING_DIR="${CLUSTER_DIR}/job_monitoring_app"
# shellcheck disable=SC2034
FRONTEND_DIR="${JOB_MONITORING_DIR}/frontend"
# shellcheck disable=SC2034
BACKEND_DIR="${JOB_MONITORING_DIR}/backend"
# shellcheck disable=SC2034
TRACKER_API_DIR="${JOB_MONITORING_DIR}/tracker_api"

## DOCKERFILES FOR JOB MONITORING APP
# Should we update the naming convention for the Dockerfiles?
# shellcheck disable=SC2034
FRONTEND_DOCKERFILE="${CURRENT_DIR}/frontend/Dockerfile_Frontend_aws"
# TODO - Update the Dockerfile for the backend once we move it to the cluster directory
# shellcheck disable=SC2034
BACKEND_DOCKERFILE="${CURRENT_DIR}/backend/Dockerfile_Backend_aws"
# shellcheck disable=SC2034
ORTHANC_DOCKERFILE="${CURRENT_DIR}/Orthanc/Dockerfile_Orthanc_aws"
# shellcheck disable=SC2034
LISTENER_DOCKERFILE="${CURRENT_DIR}/listening/Dockerfile_ReceiverLoop"
# shellcheck disable=SC2034
STUDY_DOCKERFILE="${CURRENT_DIR}/study/Dockerfile_Study"

# shellcheck disable=SC2034
BRAINMASKTOOL_DOCKERFILE="${CLUSTER_DIR}/Dockerfile_BrainMaskTool_light"
## PATHS FOR ORTHANC and AGENT

# shellcheck disable=SC2034
ORTHANC_DIR="${CLUSTER_DIR}/example_tool/Orthanc"
# shellcheck disable=SC2034
AGENT_DIR="${CLUSTER_DIR}/internal_servers"



## AWS CONFIGURATION
# shellcheck disable=SC2034
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=325852638497
REPOSITORY_NAME="manual_gui_ecr"
