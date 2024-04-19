#!/bin/bash

# Get the directory of the script
CURRENT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# Apply the frontend deployment to ECK
kubectl apply -f "${CURRENT_DIR}/aws_frontend_kube_deployment.yaml"
# Apply the frontend service to ECK
kubectl apply -f "${CURRENT_DIR}/aws_frontend_kube_service.yaml"

#kubectl apply -f "${CURRENT_DIR}/aws_frontend_ingress.yaml"


# Check the status of the deployment
kubectl get events --sort-by='.metadata.creationTimestamp'
