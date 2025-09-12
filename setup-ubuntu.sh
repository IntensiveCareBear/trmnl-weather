#!/bin/bash

# Complete Ubuntu setup script for TRMNL Weather Plugin
# This script handles all Ubuntu-specific issues

echo "🌤️  Setting up TRMNL Weather Plugin on Ubuntu..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Update system
echo "📦 Updating system packages..."
apt update && apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
apt install -y python3 python3-pip python3-venv python3-full curl git

# Check if .secrets file exists
if [ ! -f .secrets ]; then
    echo "⚠️  .secrets file not found. Creating from template..."
    cp .secrets.example .secrets
    echo "📝 Please edit .secrets file with your API keys before running again."
    echo "   Required: WEATHER_API_KEY"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install --break-system-packages -r requirements.txt

# Create systemd service
echo "📦 Creating systemd service..."
cp trmnl-weather.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable trmnl-weather

# Start the service
echo "🚀 Starting weather plugin service..."
systemctl start trmnl-weather

# Check status
echo "📊 Service status:"
systemctl status trmnl-weather --no-pager

echo ""
echo "✅ Setup complete!"
echo "📊 View logs: journalctl -u trmnl-weather -f"
echo "🛑 Stop service: systemctl stop trmnl-weather"
echo "🔄 Restart service: systemctl restart trmnl-weather"
echo "🌐 Service should be running on http://localhost:8000"
