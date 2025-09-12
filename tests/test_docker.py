#!/usr/bin/env python3
"""
Test script to verify Docker container is working properly
"""

import requests
import time
import sys

def test_docker_service():
    """Test if the Docker service is working"""
    print("🐳 Testing Docker Service")
    print("=" * 40)
    
    # Wait for service to be ready
    print("⏳ Waiting for service to be ready...")
    for i in range(30):
        try:
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ Service is ready!")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("❌ Service not ready after 30 seconds")
        return False
    
    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        print(f"✅ Health check: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test quote endpoint
    print("\n📖 Testing quote endpoint...")
    try:
        response = requests.post(
            "http://localhost:8000/weather/quote",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                quote = data['data']
                print(f"✅ Quote generated: \"{quote['quote'][:50]}...\"")
                print(f"   Author: {quote['author']}")
            else:
                print(f"❌ Quote generation failed: {data.get('error')}")
        else:
            print(f"❌ Quote endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Quote test failed: {e}")
        return False
    
    # Test TRMNL view
    print("\n🌤️  Testing TRMNL view...")
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                weather = data['data']
                print(f"✅ TRMNL view working")
                print(f"   Location: {weather['location_name']}")
                print(f"   Temperature: {weather['temp_c']}°C")
                
                if 'weather_quote' in weather:
                    quote = weather['weather_quote']
                    print(f"✅ Quote included: \"{quote['quote'][:50]}...\"")
                else:
                    print("❌ No quote in TRMNL view")
            else:
                print(f"❌ TRMNL view failed: {data.get('error')}")
        else:
            print(f"❌ TRMNL view failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ TRMNL view test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Docker service is working correctly.")
    return True

if __name__ == "__main__":
    success = test_docker_service()
    sys.exit(0 if success else 1)
