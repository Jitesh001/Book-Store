#!/bin/bash

# Default argument if no argument is passed
TAG=${1:-"dev"}

# Replace the tag in the docker-compose.yaml file
sed -i "s@\(image: pixiejitesh/bookstore-backend:\).*\$@\1$TAG@" docker-compose.yaml
# sed -i '' "s@\(image: pixiejitesh/bookstore-backend:\).*\$@\1$TAG@" docker-compose.yaml
echo "Docker image tag set to: $TAG"

# Generate the doppler.env file
doppler secrets download --no-file --format env --project book_store --config dev_jitesh > doppler.env
echo "Doppler env file generated."

# Deploy the Image for the branch specified
docker compose pull && docker compose down && doppler run -- docker compose up -d
echo "Deployment completed with tag: $TAG"
