#!/usr/bin/env python3
"""
Example script showing how to use the TRMNL Weather Plugin
to get simplified weather data for TRMNL views
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"
LOCATION = "London"  # Change this to your desired location

def get_trmnl_weather_data(location: str):
    """Get weather data formatted for TRMNL view"""
    url = f"{API_BASE_URL}/weather/trmnl-view"
    payload = {
        "location": location,
        "days": 1,
        "include_air_quality": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather_summary(data):
    """Display a simple weather summary"""
    if not data or not data.get('success'):
        print("❌ Failed to get weather data")
        return
    
    weather = data['data']
    
    print("🌤️  Weather Summary")
    print("=" * 30)
    print(f"Location: {weather['location_name']}, {weather['location_region']}")
    print(f"Temperature: {weather['temp_c']}°C (feels like {weather['feels_like_c']}°C)")
    print(f"Condition: {weather['condition_text']}")
    print(f"Wind Chill: {weather['windchill_c']}°C")
    print(f"High/Low: {weather['tomorrow_max_c']}°C / {weather['tomorrow_min_c']}°C")
    print(f"UV Index: {weather['uv_index']}")
    print(f"AQI: {weather['aqi_us']}")
    print(f"Wind: {weather['wind_kph']} kph {weather['wind_dir']}")
    print(f"Updated: {weather['formatted_time']} {weather['timezone']}")

def main():
    """Main function"""
    print("🚀 TRMNL Weather Plugin Example")
    print("=" * 40)
    
    # Get weather data
    print(f"Fetching weather data for {LOCATION}...")
    data = get_trmnl_weather_data(LOCATION)
    
    if data:
        display_weather_summary(data)
        
        # Show the raw data structure for TRMNL view
        print("\n📊 Raw Data for TRMNL View:")
        print("=" * 40)
        print(json.dumps(data['data'], indent=2))
    else:
        print("❌ Failed to get weather data")

if __name__ == "__main__":
    main()
