#!/usr/bin/env python3
"""
Test script to verify TRMNL data format and quote inclusion
"""

import requests
import json

def test_trmnl_data_format():
    """Test the exact data format being sent to TRMNL"""
    print("🔍 Testing TRMNL Data Format")
    print("=" * 40)
    
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {data['success']}")
            
            if data['success']:
                weather_data = data['data']
                
                # Check if quote exists
                if 'weather_quote' in weather_data:
                    quote = weather_data['weather_quote']
                    print(f"\n📖 QUOTE FOUND:")
                    print(f"   Quote: \"{quote['quote']}\"")
                    print(f"   Author: {quote['author']}")
                    print(f"   Work: {quote['work']}")
                    print(f"   Weather: {quote['weather_condition']}")
                    
                    # Show the exact data structure
                    print(f"\n📊 Quote Data Structure:")
                    print(json.dumps(quote, indent=2))
                else:
                    print(f"\n❌ NO QUOTE FOUND")
                    print(f"Available keys: {list(weather_data.keys())}")
                
                # Show all data keys
                print(f"\n📋 All Data Keys:")
                for key in weather_data.keys():
                    value = weather_data[key]
                    if isinstance(value, dict):
                        print(f"   {key}: {type(value).__name__} with keys {list(value.keys())}")
                    else:
                        print(f"   {key}: {type(value).__name__} = {value}")
                
                # Show the complete response
                print(f"\n📄 Complete Response:")
                print(json.dumps(weather_data, indent=2))
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_different_locations():
    """Test quotes for different locations"""
    print("\n🌍 Testing Different Locations")
    print("=" * 40)
    
    locations = ["London", "Paris", "Tokyo", "New York"]
    
    for location in locations:
        try:
            response = requests.post(
                "http://localhost:8000/weather/trmnl-view",
                json={"location": location, "include_air_quality": True},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success'] and 'weather_quote' in data['data']:
                    quote = data['data']['weather_quote']
                    print(f"✅ {location}: \"{quote['quote'][:50]}...\" - {quote['author']}")
                else:
                    print(f"❌ {location}: No quote found")
            else:
                print(f"❌ {location}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {location}: {e}")

if __name__ == "__main__":
    test_trmnl_data_format()
    test_different_locations()
