#!/bin/bash

# TRMNL Weather Plugin Startup Script

echo "🌤️  Starting TRMNL Weather Plugin..."

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

# Check if we're on Ubuntu/Debian and install python3-venv if needed
if command -v apt >/dev/null 2>&1; then
    if ! python3 -m venv --help >/dev/null 2>&1; then
        echo "📦 Installing python3-venv package..."
        sudo apt update && sudo apt install -y python3-venv
    fi
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    if ! python3 -m venv venv; then
        echo "❌ Failed to create virtual environment. Trying alternative approach..."
        echo "📦 Installing dependencies system-wide (not recommended for production)..."
        pip3 install -r requirements.txt
        echo "⚠️  Dependencies installed system-wide. Consider using a virtual environment for production."
        echo "🚀 Starting weather plugin service..."
        python3 main.py
        exit 0
    fi
fi

echo "📦 Installing dependencies..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "❌ Virtual environment not found. Installing system-wide..."
    echo "⚠️  Using --break-system-packages flag for externally managed environment..."
    pip3 install --break-system-packages -r requirements.txt
fi

# Start the service
echo "🚀 Starting weather plugin service..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    python main.py
else
    python3 main.py
fi
