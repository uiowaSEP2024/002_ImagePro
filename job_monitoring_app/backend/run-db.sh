#!/bin/bash

# Stop and remove existing containers
echo "===>Stopping existing backend-postgres containers"
docker stop backend-postgres &> /dev/null || true
docker rm backend-postgres &> /dev/null || true

# Start a new docker instance with postgres image
echo "===>Starting new backend-postgres container"
docker run --name backend-postgres \
  -e POSTGRES_PASSWORD=admin1234 \
  -p 5432:5432 \
  -v pg_data:/var/lib/postgresql/data \
  --rm \
  postgres:14
