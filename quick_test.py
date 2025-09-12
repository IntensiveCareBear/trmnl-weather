#!/usr/bin/env python3
"""
Quick test to check if quotes are working
"""

import requests
import json

def test_api():
    """Quick API test"""
    print("🔍 Quick API Test")
    print("=" * 30)
    
    # Test health
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test quote endpoint
    print("\n📖 Testing quote endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/weather/quote",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Success: {data.get('success')}")
        
        if data.get('success'):
            quote = data['data']
            print(f"Quote: {quote['quote'][:50]}...")
            print(f"Author: {quote['author']}")
        else:
            print(f"Error: {data.get('error')}")
            
    except Exception as e:
        print(f"❌ Quote test failed: {e}")
    
    # Test TRMNL view
    print("\n🌤️  Testing TRMNL view...")
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Success: {data.get('success')}")
        
        if data.get('success'):
            weather = data['data']
            print(f"Location: {weather['location_name']}")
            print(f"Temperature: {weather['temp_c']}°C")
            
            if 'weather_quote' in weather:
                quote = weather['weather_quote']
                print(f"✅ Quote found: {quote['quote'][:50]}...")
                print(f"Author: {quote['author']}")
            else:
                print("❌ No weather_quote in response")
                print(f"Available keys: {list(weather.keys())}")
        else:
            print(f"Error: {data.get('error')}")
            
    except Exception as e:
        print(f"❌ TRMNL view test failed: {e}")

if __name__ == "__main__":
    test_api()
