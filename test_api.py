#!/usr/bin/env python3
"""
Simple test script for the TRMNL Weather Plugin API
"""

import requests
import json
import time
import sys

# Configuration
BASE_URL = "http://localhost:8000"
TEST_LOCATION = "London"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        response.raise_for_status()
        print(f"✅ Health check passed: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_current_weather():
    """Test current weather endpoint"""
    print("Testing current weather endpoint...")
    try:
        payload = {
            "location": TEST_LOCATION,
            "include_air_quality": True
        }
        response = requests.post(
            f"{BASE_URL}/weather/current",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ Current weather test passed")
        print(f"   Location: {data['data']['location']['name']}")
        print(f"   Temperature: {data['data']['current']['temp_c']}°C")
        print(f"   Condition: {data['data']['current']['condition']['text']}")
        return True
    except Exception as e:
        print(f"❌ Current weather test failed: {e}")
        return False

def test_forecast():
    """Test forecast endpoint"""
    print("Testing forecast endpoint...")
    try:
        payload = {
            "location": TEST_LOCATION,
            "days": 3,
            "include_air_quality": False
        }
        response = requests.post(
            f"{BASE_URL}/weather/forecast",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ Forecast test passed")
        print(f"   Location: {data['data']['location']['name']}")
        print(f"   Forecast days: {len(data['data']['forecast']['forecastday'])}")
        return True
    except Exception as e:
        print(f"❌ Forecast test failed: {e}")
        return False

def test_trmnl_webhook():
    """Test TRMNL webhook endpoint"""
    print("Testing TRMNL webhook endpoint...")
    try:
        payload = {
            "location": TEST_LOCATION,
            "days": 1,
            "include_air_quality": True
        }
        response = requests.post(
            f"{BASE_URL}/weather/send-to-trmnl",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ TRMNL webhook test passed")
        print(f"   Success: {data['success']}")
        if 'data' in data:
            print(f"   Message: {data['data'].get('message', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ TRMNL webhook test failed: {e}")
        return False

def test_trmnl_view():
    """Test TRMNL view endpoint"""
    print("Testing TRMNL view endpoint...")
    try:
        payload = {
            "location": TEST_LOCATION,
            "days": 1,
            "include_air_quality": True
        }
        response = requests.post(
            f"{BASE_URL}/weather/trmnl-view",
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ TRMNL view test passed")
        print(f"   Location: {data['data']['location_name']}")
        print(f"   Temperature: {data['data']['temp_c']}°C")
        print(f"   Wind Chill: {data['data']['windchill_c']}°C")
        print(f"   UV Index: {data['data']['uv_index']}")
        print(f"   AQI: {data['data']['aqi_us']}")
        if 'weather_quote' in data['data']:
            quote = data['data']['weather_quote']
            print(f"   Quote: \"{quote['quote'][:50]}...\" - {quote['author']}")
        return True
    except Exception as e:
        print(f"❌ TRMNL view test failed: {e}")
        return False

def test_weather_quote():
    """Test weather quote endpoint"""
    print("Testing weather quote endpoint...")
    try:
        payload = {
            "location": TEST_LOCATION,
            "days": 1,
            "include_air_quality": True
        }
        response = requests.post(
            f"{BASE_URL}/weather/quote",
            json=payload,
            timeout=60  # Longer timeout for AI generation
        )
        response.raise_for_status()
        data = response.json()
        print(f"✅ Weather quote test passed")
        if data['success']:
            quote_data = data['data']
            print(f"   Quote: \"{quote_data['quote'][:50]}...\"")
            print(f"   Author: {quote_data['author']}")
            print(f"   Work: {quote_data['work']}")
        else:
            print(f"   Quote generation failed: {data.get('error', 'Unknown error')}")
        return True
    except Exception as e:
        print(f"❌ Weather quote test failed: {e}")
        return False

def test_quote_cache_stats():
    """Test quote cache stats endpoint"""
    print("Testing quote cache stats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/quotes/cache-stats", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Quote cache stats test passed")
        print(f"   Cached quotes: {data['data']['total_cached_quotes']}")
        return True
    except Exception as e:
        print(f"❌ Quote cache stats test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting TRMNL Weather Plugin API Tests")
    print("=" * 50)
    
    # Wait for service to be ready
    print("Waiting for service to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            if response.status_code == 200:
                print("✅ Service is ready!")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("❌ Service not ready after 30 seconds")
        sys.exit(1)
    
    # Run tests
    tests = [
        test_health,
        test_current_weather,
        test_forecast,
        test_trmnl_webhook,
        test_trmnl_view,
        test_weather_quote,
        test_quote_cache_stats
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
