#!/bin/bash

# Simple Ubuntu installation script for TRMNL Weather Plugin
# This handles the externally managed environment issue

echo "🌤️  Installing TRMNL Weather Plugin on Ubuntu..."

# Check if .secrets file exists
if [ ! -f .secrets ]; then
    echo "⚠️  .secrets file not found. Creating from template..."
    cp .secrets.example .secrets
    echo "📝 Please edit .secrets file with your API keys before running again."
    echo "   Required: WEATHER_API_KEY"
    exit 1
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
apt update
apt install -y python3-pip python3-venv python3-full curl

# Install Python packages with --break-system-packages
echo "📦 Installing Python dependencies..."
pip3 install --break-system-packages -r requirements.txt

# Start the service
echo "🚀 Starting weather plugin service..."
python3 main.py
