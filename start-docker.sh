#!/bin/bash

# TRMNL Weather Plugin Docker Startup Script
# This is the most reliable way to run on Ubuntu

echo "🐳 Starting TRMNL Weather Plugin with Docker..."

# Check if .secrets file exists
if [ ! -f .secrets ]; then
    echo "⚠️  .secrets file not found. Creating from template..."
    cp .secrets.example .secrets
    echo "📝 Please edit .secrets file with your API keys before running again."
    echo "   Required: WEATHER_API_KEY"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker >/dev/null 2>&1; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "⚠️  Please log out and back in for Docker permissions to take effect."
    echo "   Then run this script again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose >/dev/null 2>&1; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Build and start the service
echo "🚀 Building and starting weather plugin service..."
docker-compose up --build -d

echo "✅ Service started! Check status with: docker-compose ps"
echo "📊 View logs with: docker-compose logs -f"
echo "🛑 Stop service with: docker-compose down"
