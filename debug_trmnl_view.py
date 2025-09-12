#!/usr/bin/env python3
"""
Debug script to test TRMNL view data and see what's being sent
"""

import requests
import json

def test_trmnl_view_data():
    """Test what data is being returned for TRMNL view"""
    print("🔍 Testing TRMNL View Data")
    print("=" * 40)
    
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            
            if data['success']:
                weather_data = data['data']
                print(f"\n📍 Location: {weather_data['location_name']}")
                print(f"🌡️  Temperature: {weather_data['temp_c']}°C")
                print(f"🌤️  Condition: {weather_data['condition_text']}")
                
                # Check if quote is present
                if 'weather_quote' in weather_data:
                    quote = weather_data['weather_quote']
                    print(f"\n📖 QUOTE FOUND:")
                    print(f"   Quote: \"{quote['quote']}\"")
                    print(f"   Author: {quote['author']}")
                    print(f"   Work: {quote['work']}")
                    print(f"   Weather: {quote['weather_condition']}")
                else:
                    print("\n❌ NO QUOTE FOUND")
                    print(f"Available keys: {list(weather_data.keys())}")
                
                # Show the full response for debugging
                print(f"\n📊 Full Response:")
                print(json.dumps(weather_data, indent=2))
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_quote_endpoint():
    """Test the quote endpoint directly"""
    print("\n🔍 Testing Quote Endpoint")
    print("=" * 40)
    
    try:
        response = requests.post(
            "http://localhost:8000/weather/quote",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data['success']}")
            
            if data['success']:
                quote_data = data['data']
                print(f"📖 Quote: \"{quote_data['quote']}\"")
                print(f"👤 Author: {quote_data['author']}")
                print(f"📚 Work: {quote_data['work']}")
            else:
                print(f"❌ Quote Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_cache_stats():
    """Test quote cache statistics"""
    print("\n🔍 Testing Cache Stats")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/quotes/cache-stats", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                stats = data['data']
                print(f"📊 Cached quotes: {stats['total_cached_quotes']}")
                print(f"🔑 Cache keys: {stats['cache_keys']}")
            else:
                print(f"❌ Cache stats error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_trmnl_view_data()
    test_quote_endpoint()
    test_cache_stats()
