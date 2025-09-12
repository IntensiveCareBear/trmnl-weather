#!/usr/bin/env python3
"""
Example script demonstrating the weather quote functionality
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:8000"
LOCATIONS = ["London", "New York", "Tokyo", "Paris", "Sydney"]

def get_weather_quote(location: str):
    """Get a weather quote for a specific location"""
    url = f"{API_BASE_URL}/weather/quote"
    payload = {
        "location": location,
        "days": 1,
        "include_air_quality": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather quote for {location}: {e}")
        return None

def get_trmnl_view_with_quote(location: str):
    """Get TRMNL view data with weather quote"""
    url = f"{API_BASE_URL}/weather/trmnl-view"
    payload = {
        "location": location,
        "days": 1,
        "include_air_quality": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching TRMNL view for {location}: {e}")
        return None

def display_quote(quote_data):
    """Display a weather quote nicely"""
    if not quote_data or not quote_data.get('success'):
        print("❌ No quote available")
        return
    
    quote = quote_data['data']
    print("📖 Weather Quote")
    print("=" * 50)
    print(f"\"{quote['quote']}\"")
    print(f"   — {quote['author']}, {quote['work']}")
    print(f"   Weather: {quote['weather_condition']}")
    print(f"   Location: {quote['location']}")
    print(f"   Generated: {quote['timestamp']}")
    print()

def display_trmnl_view(data):
    """Display TRMNL view data with quote"""
    if not data or not data.get('success'):
        print("❌ No data available")
        return
    
    weather = data['data']
    
    print("🌤️  Weather with Literary Quote")
    print("=" * 50)
    print(f"Location: {weather['location_name']}, {weather['location_region']}")
    print(f"Temperature: {weather['temp_c']}°C (feels like {weather['feels_like_c']}°C)")
    print(f"Condition: {weather['condition_text']}")
    print(f"Wind Chill: {weather['windchill_c']}°C")
    print(f"UV Index: {weather['uv_index']} | AQI: {weather['aqi_us']}")
    print()
    
    if 'weather_quote' in weather:
        quote = weather['weather_quote']
        print("📖 Literary Quote:")
        print(f"\"{quote['quote']}\"")
        print(f"   — {quote['author']}, {quote['work']}")
        print()
    else:
        print("📖 No quote available for this weather condition")
        print()

def get_cache_stats():
    """Get quote cache statistics"""
    try:
        response = requests.get(f"{API_BASE_URL}/quotes/cache-stats", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching cache stats: {e}")
        return None

def main():
    """Main function"""
    print("📚 TRMNL Weather Quote Generator")
    print("=" * 60)
    
    # Test individual quote generation
    print("Testing individual quote generation...")
    for location in LOCATIONS[:2]:  # Test first 2 locations
        print(f"\n📍 Getting quote for {location}...")
        quote_data = get_weather_quote(location)
        if quote_data:
            display_quote(quote_data)
        time.sleep(2)  # Rate limiting
    
    print("\n" + "=" * 60)
    
    # Test TRMNL view with quotes
    print("Testing TRMNL view with quotes...")
    for location in LOCATIONS[:2]:  # Test first 2 locations
        print(f"\n📍 Getting TRMNL view for {location}...")
        view_data = get_trmnl_view_with_quote(location)
        if view_data:
            display_trmnl_view(view_data)
        time.sleep(2)  # Rate limiting
    
    print("\n" + "=" * 60)
    
    # Show cache statistics
    print("Cache Statistics:")
    stats = get_cache_stats()
    if stats and stats.get('success'):
        data = stats['data']
        print(f"Total cached quotes: {data['total_cached_quotes']}")
        print(f"Cache keys: {', '.join(data['cache_keys'])}")
        print(f"Last updates: {json.dumps(data['last_updates'], indent=2)}")
    else:
        print("❌ Could not retrieve cache statistics")

if __name__ == "__main__":
    main()
