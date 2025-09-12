#!/usr/bin/env python3
"""
Comprehensive local testing script for TRMNL Weather Plugin
"""

import requests
import json
import time
import sys

# Configuration
BASE_URL = "http://localhost:8000"
TEST_LOCATIONS = ["London", "New York", "Tokyo", "Paris"]

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")

def print_result(test_name, success, details=""):
    """Print test result"""
    status = "✅" if success else "❌"
    print(f"{status} {test_name}")
    if details:
        print(f"   {details}")

def test_health():
    """Test health endpoint"""
    print_header("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_result("Health Check", True, f"Status: {data.get('status')}")
            return True
        else:
            print_result("Health Check", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result("Health Check", False, f"Error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print_header("Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            print_result("Root Endpoint", True, "API info available")
            return True
        else:
            print_result("Root Endpoint", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        print_result("Root Endpoint", False, f"Error: {e}")
        return False

def test_current_weather(location="London"):
    """Test current weather endpoint"""
    print_header(f"Current Weather - {location}")
    try:
        response = requests.post(
            f"{BASE_URL}/weather/current",
            json={"location": location, "include_air_quality": True},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                weather = data['data']['current']
                print_result("Current Weather", True, 
                    f"Temp: {weather.get('temp_c')}°C, Condition: {weather.get('condition', {}).get('text')}")
                return True
            else:
                print_result("Current Weather", False, f"API Error: {data.get('error')}")
                return False
        else:
            print_result("Current Weather", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        print_result("Current Weather", False, f"Error: {e}")
        return False

def test_forecast(location="London"):
    """Test forecast endpoint"""
    print_header(f"Weather Forecast - {location}")
    try:
        response = requests.post(
            f"{BASE_URL}/weather/forecast",
            json={"location": location, "days": 3, "include_air_quality": True},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                forecast = data['data']['forecast']['forecastday']
                print_result("Weather Forecast", True, f"Got {len(forecast)} days of forecast")
                return True
            else:
                print_result("Weather Forecast", False, f"API Error: {data.get('error')}")
                return False
        else:
            print_result("Weather Forecast", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        print_result("Weather Forecast", False, f"Error: {e}")
        return False

def test_trmnl_view(location="London"):
    """Test TRMNL view endpoint"""
    print_header(f"TRMNL View - {location}")
    try:
        response = requests.post(
            f"{BASE_URL}/weather/trmnl-view",
            json={"location": location, "include_air_quality": True},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                weather = data['data']
                print_result("TRMNL View", True, 
                    f"Location: {weather.get('location_name')}, Temp: {weather.get('temp_c')}°C")
                
                # Check for quote
                if 'weather_quote' in weather:
                    quote = weather['weather_quote']
                    print(f"   📖 Quote: \"{quote['quote'][:50]}...\"")
                    print(f"   👤 Author: {quote['author']}")
                else:
                    print("   ⚠️  No weather quote found")
                
                return True
            else:
                print_result("TRMNL View", False, f"API Error: {data.get('error')}")
                return False
        else:
            print_result("TRMNL View", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        print_result("TRMNL View", False, f"Error: {e}")
        return False

def test_trmnl_view_default():
    """Test TRMNL view with default location"""
    print_header("TRMNL View (Default Location)")
    try:
        response = requests.get(f"{BASE_URL}/weather/trmnl-view", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                weather = data['data']
                print_result("TRMNL View (Default)", True, 
                    f"Location: {weather.get('location_name')}, Temp: {weather.get('temp_c')}°C")
                return True
            else:
                print_result("TRMNL View (Default)", False, f"API Error: {data.get('error')}")
                return False
        else:
            print_result("TRMNL View (Default)", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        print_result("TRMNL View (Default)", False, f"Error: {e}")
        return False

def test_weather_quote(location="London"):
    """Test weather quote endpoint"""
    print_header(f"Weather Quote - {location}")
    try:
        response = requests.post(
            f"{BASE_URL}/weather/quote",
            json={"location": location, "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                quote = data['data']
                print_result("Weather Quote", True, f"Generated quote for {location}")
                print(f"   📖 \"{quote['quote'][:80]}...\"")
                print(f"   👤 {quote['author']} - {quote['work']}")
                return True
            else:
                print_result("Weather Quote", False, f"API Error: {data.get('error')}")
                return False
        else:
            print_result("Weather Quote", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        print_result("Weather Quote", False, f"Error: {e}")
        return False

def test_quote_cache_stats():
    """Test quote cache statistics"""
    print_header("Quote Cache Statistics")
    try:
        response = requests.get(f"{BASE_URL}/quotes/cache-stats", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_result("Quote Cache Stats", True, f"Cache stats retrieved")
            print(f"   📊 {json.dumps(data, indent=2)}")
            return True
        else:
            print_result("Quote Cache Stats", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        print_result("Quote Cache Stats", False, f"Error: {e}")
        return False

def test_multiple_locations():
    """Test with multiple locations"""
    print_header("Multiple Locations Test")
    results = []
    
    for location in TEST_LOCATIONS:
        print(f"\n🌍 Testing {location}...")
        success = test_current_weather(location)
        results.append((location, success))
    
    print(f"\n📊 Location Test Results:")
    for location, success in results:
        status = "✅" if success else "❌"
        print(f"   {status} {location}")
    
    return all(success for _, success in results)

def main():
    """Run all tests"""
    print("🚀 TRMNL Weather Plugin - Local Testing Suite")
    print("=" * 60)
    
    # Wait for service to be ready
    print("⏳ Waiting for service to be ready...")
    for i in range(30):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Service is ready!")
                break
        except:
            pass
        time.sleep(1)
    else:
        print("❌ Service not ready after 30 seconds")
        print("Please start the service first:")
        print("  python3 main.py")
        print("  or")
        print("  docker-compose -f docker-compose-working.yml up -d")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("Current Weather", lambda: test_current_weather("London")),
        ("Weather Forecast", lambda: test_forecast("London")),
        ("TRMNL View (POST)", lambda: test_trmnl_view("London")),
        ("TRMNL View (GET)", test_trmnl_view_default),
        ("Weather Quote", lambda: test_weather_quote("London")),
        ("Quote Cache Stats", test_quote_cache_stats),
        ("Multiple Locations", test_multiple_locations),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
        print()
    
    # Summary
    print_header("Test Summary")
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your weather service is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    print(f"\n🌐 Service is running at: {BASE_URL}")
    print(f"📖 API Documentation: {BASE_URL}/docs")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
