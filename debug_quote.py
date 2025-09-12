#!/usr/bin/env python3
"""
Debug script to test quote functionality
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"
LOCATION = "London"

def test_quote_generation():
    """Test if quotes are being generated"""
    print("🔍 Testing quote generation...")
    
    # Test the quote endpoint directly
    try:
        response = requests.post(
            f"{API_BASE_URL}/weather/quote",
            json={"location": LOCATION, "include_air_quality": True},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Quote endpoint response: {data['success']}")
        if data['success']:
            quote_data = data['data']
            print(f"📖 Quote: \"{quote_data['quote'][:100]}...\"")
            print(f"👤 Author: {quote_data['author']}")
            print(f"📚 Work: {quote_data['work']}")
        else:
            print(f"❌ Quote generation failed: {data.get('error')}")
            
    except Exception as e:
        print(f"❌ Quote endpoint error: {e}")

def test_trmnl_view_with_quote():
    """Test TRMNL view with quote data"""
    print("\n🔍 Testing TRMNL view with quotes...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/weather/trmnl-view",
            json={"location": LOCATION, "include_air_quality": True},
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ TRMNL view response: {data['success']}")
        if data['success']:
            weather_data = data['data']
            print(f"📍 Location: {weather_data['location_name']}")
            print(f"🌡️  Temperature: {weather_data['temp_c']}°C")
            
            if 'weather_quote' in weather_data:
                quote = weather_data['weather_quote']
                print(f"📖 Quote found: \"{quote['quote'][:100]}...\"")
                print(f"👤 Author: {quote['author']}")
                print(f"📚 Work: {quote['work']}")
            else:
                print("❌ No weather_quote in response data")
                print(f"📊 Available keys: {list(weather_data.keys())}")
        else:
            print(f"❌ TRMNL view failed: {data.get('error')}")
            
    except Exception as e:
        print(f"❌ TRMNL view error: {e}")

def test_cache_stats():
    """Test quote cache statistics"""
    print("\n🔍 Testing cache statistics...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/quotes/cache-stats", timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Cache stats: {data['success']}")
        if data['success']:
            stats = data['data']
            print(f"📊 Cached quotes: {stats['total_cached_quotes']}")
            print(f"🔑 Cache keys: {stats['cache_keys']}")
        else:
            print(f"❌ Cache stats failed: {data.get('error')}")
            
    except Exception as e:
        print(f"❌ Cache stats error: {e}")

def main():
    """Run all debug tests"""
    print("🐛 TRMNL Weather Quote Debug Tool")
    print("=" * 50)
    
    # Check if service is running
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Service is running")
        else:
            print("❌ Service not responding properly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to service: {e}")
        print("Make sure the service is running on http://localhost:8000")
        return
    
    # Run tests
    test_quote_generation()
    test_trmnl_view_with_quote()
    test_cache_stats()
    
    print("\n" + "=" * 50)
    print("🔍 Debug complete!")

if __name__ == "__main__":
    main()
