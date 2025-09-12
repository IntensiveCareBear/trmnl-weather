#!/bin/bash

# TRMNL Weather Plugin Startup Script for Ubuntu/Debian
# This script handles externally managed Python environments

echo "🌤️  Starting TRMNL Weather Plugin on Ubuntu..."

# Check if .secrets file exists
if [ ! -f .secrets ]; then
    echo "⚠️  .secrets file not found. Creating from template..."
    cp .secrets.example .secrets
    echo "📝 Please edit .secrets file with your API keys before running again."
    echo "   Required: WEATHER_API_KEY"
    exit 1
fi

# Check if WEATHER_API_KEY is set in .secrets
if ! grep -q "WEATHER_API_KEY=your_weatherapi_key_here" .secrets; then
    echo "✅ Secrets configuration found"
else
    echo "❌ Please set WEATHER_API_KEY in .secrets file"
    exit 1
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv curl

# Try to create virtual environment
echo "📦 Creating virtual environment..."
if python3 -m venv venv 2>/dev/null; then
    echo "✅ Virtual environment created successfully"
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "⚠️  Virtual environment creation failed. Using system Python..."
    echo "📦 Installing dependencies system-wide..."
    
    # Handle externally managed environment
    pip3 install --break-system-packages -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies. Trying with --user flag..."
        pip3 install --user -r requirements.txt
    fi
fi

# Start the service
echo "🚀 Starting weather plugin service..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    python main.py
else
    python3 main.py
fi
