#!/bin/bash

# Check if Docker is installed, if not, install it
if ! command -v docker &> /dev/null; then
  echo "Docker not found. Installing Docker..."
  # Install Docker for Mac
  if [[ "$(uname -s)" == "Darwin" ]]; then
    brew install --cask docker
  # Install Docker for Linux (Ubuntu)
  elif [[ -f "/etc/lsb-release" ]] && grep -q "Ubuntu" "/etc/lsb-release"; then
    sudo apt update
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
  else
    echo "Unsupported operating system. Please install Docker manually."
    exit 1
  fi
fi

# Check if Kind is installed, if not, install it
if ! command -v kind &> /dev/null; then
  echo "Kind not found. Installing Kind..."
  GO111MODULE="on" go get sigs.k8s.io/kind@v0.11.1
fi

# Check if Kind cluster exists, if not, create it
if [[ $(kind get clusters) != *"kind"* ]]; then
  echo "Kind cluster not found. Creating a Kind cluster..."
  kind create cluster
else
  echo "Kind cluster already exists."
fi

kubectl cluster-info --context kind-kind

kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.10.1/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.10.1/serving-core.yaml
kubectl wait --for=condition=Ready pod --all -n knative-serving --timeout=-1s

echo "Knative installation complete!"
