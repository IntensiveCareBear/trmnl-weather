#!/usr/bin/env python3
"""
Test script to verify location configuration
"""

import requests
import json

def test_location_configuration():
    """Test location configuration"""
    print("🌍 Testing Location Configuration")
    print("=" * 40)
    
    # Test 1: Default location (GET endpoint)
    print("1. Testing Default Location (GET /weather/trmnl-view)")
    try:
        response = requests.get("http://localhost:8000/weather/trmnl-view", timeout=30)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                weather = data['data']
                print(f"   ✅ Location: {weather.get('location_name')}")
                print(f"   🌡️  Temperature: {weather.get('temp_c')}°C")
                print(f"   🌤️  Condition: {weather.get('condition_text')}")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
    
    # Test 2: Specific location (POST endpoint)
    print("\n2. Testing Specific Location (POST /weather/trmnl-view)")
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "Morgan Hill, CA", "include_air_quality": True},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                weather = data['data']
                print(f"   ✅ Location: {weather.get('location_name')}")
                print(f"   🌡️  Temperature: {weather.get('temp_c')}°C")
                print(f"   🌤️  Condition: {weather.get('condition_text')}")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
    
    # Test 3: Different locations
    print("\n3. Testing Different Locations")
    locations = ["San Francisco, CA", "Los Angeles, CA", "New York, NY"]
    
    for location in locations:
        try:
            response = requests.post(
                "http://localhost:8000/weather/trmnl-view",
                json={"location": location, "include_air_quality": True},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    weather = data['data']
                    print(f"   ✅ {location}: {weather.get('location_name')} - {weather.get('temp_c')}°C")
                else:
                    print(f"   ❌ {location}: Error - {data.get('error')}")
            else:
                print(f"   ❌ {location}: HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ {location}: Request failed - {e}")

def test_webhook_with_new_location():
    """Test webhook with new location"""
    print("\n" + "=" * 40)
    print("4. Testing Webhook with New Location")
    
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "Morgan Hill, CA", "include_air_quality": True},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                weather = data['data']
                print(f"   ✅ Webhook will send data for: {weather.get('location_name')}")
                print(f"   🌡️  Temperature: {weather.get('temp_c')}°C")
                print(f"   🌤️  Condition: {weather.get('condition_text')}")
                
                # Check for quote
                if 'weather_quote' in weather:
                    quote = weather['weather_quote']
                    print(f"   📖 Quote: \"{quote['quote'][:50]}...\"")
                else:
                    print(f"   ⚠️  No quote found")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Request failed: {e}")

if __name__ == "__main__":
    test_location_configuration()
    test_webhook_with_new_location()
    
    print("\n" + "=" * 40)
    print("💡 Tips:")
    print("   - Default location is set in .secrets file")
    print("   - Use POST endpoint to specify different locations")
    print("   - GET endpoint uses the default location")
    print("   - Restart service after changing .secrets file")
