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

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Start the service
echo "🚀 Starting weather plugin service..."
python main.py
