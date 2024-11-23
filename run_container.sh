#!/bin/bash

# Script to build and run the Docker container for the Flask app.

# Usage:
#   ./run_container.sh <image-name> <port>
# Example:
#   ./run_container.sh docx-to-pdf-converter 8080

# Check if the user has provided the required arguments
if [ $# -ne 2 ]; then
  echo "Usage: $0 <image-name> <port>"
  echo "Example: $0 docx-to-pdf-converter 8080"
  exit 1
fi

# Variables
IMAGE_NAME=$1
PORT=$2

echo "Building the Docker image..."
# Build the Docker image
docker build -t $IMAGE_NAME .

# Check if the build was successful
if [ $? -ne 0 ]; then
  echo "Docker build failed. Exiting..."
  exit 1
fi

echo "Docker image built successfully."

# Run the Docker container
echo "Running the Docker container on port $PORT..."
docker run -d -p $PORT:8080 --name d2p $IMAGE_NAME

# Check if the container started successfully
if [ $? -ne 0 ]; then
  echo "Failed to run the Docker container. Exiting..."
  exit 1
fi

echo "Docker container is running."
echo "Access the app at: http://localhost:$PORT"
