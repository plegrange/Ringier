#!/bin/bash

# Enable Docker BuildKit
export DOCKER_BUILDKIT=1

# Build the Docker image with caching support
docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --cache-from=myapp:cache \
  --tag myapp:latest \
  .

# After the build is done, tag the cache image
docker tag myapp:latest myapp:cache
