#!/bin/bash

# Docker startup script for TRMNL Weather Plugin
echo "🐳 Starting TRMNL Weather Plugin with Docker..."

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans

# Clean up any orphaned networks
echo "🧹 Cleaning up networks..."
docker network prune -f

# Build and start with the working configuration
echo "🚀 Building and starting service..."
docker-compose -f docker-compose-working.yml up --build -d

# Wait for service to be ready
echo "⏳ Waiting for service to be ready..."
sleep 10

# Test the service
echo "🧪 Testing service..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Service is running successfully!"
    echo "📊 Service status:"
    docker-compose -f docker-compose-working.yml ps
    
    echo ""
    echo "🌐 Service is available at: http://localhost:8000"
    echo "📖 API docs: http://localhost:8000/docs"
    echo "📊 View logs: docker-compose -f docker-compose-working.yml logs -f"
    echo "🛑 Stop service: docker-compose -f docker-compose-working.yml down"
else
    echo "❌ Service failed to start properly"
    echo "📊 Container logs:"
    docker-compose -f docker-compose-working.yml logs
fi
