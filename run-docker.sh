#!/bin/bash

# Set image name
IMAGE_NAME="llm-app"
CONTAINER_NAME="llm-container"



# Check if Dockerfile exists
if [ ! -f Dockerfile ]; then
    echo "❌ Error: Dockerfile not found in $(pwd). Please check your path."
    exit 1
fi

# Build the Docker image
echo "🚀 Building Docker image: $IMAGE_NAME..."
docker build ./ -t $IMAGE_NAME .

# Remove any existing container with the same name
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🛑 Stopping and removing existing container: $CONTAINER_NAME..."
    docker stop $CONTAINER_NAME >/dev/null 2>&1
    docker rm $CONTAINER_NAME >/dev/null 2>&1
fi

# Run the container
echo "🐍 Running LLM app in Docker..."
docker run -p 5000:5000 --name $CONTAINER_NAME $IMAGE_NAME

# Success message
echo "✅ LLM app is running at http://localhost:5000"
