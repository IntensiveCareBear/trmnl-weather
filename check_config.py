#!/usr/bin/env python3
"""
Check configuration and API keys
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
if os.path.exists('.secrets'):
    load_dotenv('.secrets')

def check_config():
    """Check if all required configuration is set"""
    print("🔧 Configuration Check")
    print("=" * 30)
    
    # Check Weather API key
    weather_key = os.getenv('WEATHER_API_KEY', '')
    if weather_key and weather_key != 'your_weatherapi_key_here':
        print(f"✅ Weather API Key: {weather_key[:10]}...")
    else:
        print("❌ Weather API Key: Not set or using placeholder")
    
    # Check Gemini API key
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    if gemini_key and gemini_key != 'your_gemini_api_key_here':
        print(f"✅ Gemini API Key: {gemini_key[:10]}...")
    else:
        print("❌ Gemini API Key: Not set or using placeholder")
    
    # Check TRMNL webhook
    webhook_url = os.getenv('TRMNL_WEBHOOK_URL', '')
    if webhook_url:
        print(f"✅ TRMNL Webhook: {webhook_url[:30]}...")
    else:
        print("❌ TRMNL Webhook: Not set")
    
    print("\n📁 Files:")
    print(f"✅ .secrets exists: {os.path.exists('.secrets')}")
    print(f"✅ .secrets.example exists: {os.path.exists('.secrets.example')}")
    print(f"✅ .gitignore exists: {os.path.exists('.gitignore')}")
    
    # Check if .secrets is in .gitignore
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
            if '.secrets' in gitignore_content:
                print("✅ .secrets is in .gitignore")
            else:
                print("❌ .secrets is NOT in .gitignore")

if __name__ == "__main__":
    check_config()
