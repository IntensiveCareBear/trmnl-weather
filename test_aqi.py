#!/usr/bin/env python3
"""
Test script to check AQI data from WeatherAPI
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.secrets')

def test_aqi_data():
    """Test AQI data from WeatherAPI"""
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        print("❌ No WeatherAPI key found")
        return
    
    print("🌤️  Testing AQI data from WeatherAPI")
    print("=" * 40)
    
    # Test with London
    url = f"http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': 'London',
        'aqi': 'yes'
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check current weather
            current = data.get('current', {})
            print(f"\n📍 Location: {data.get('location', {}).get('name', 'Unknown')}")
            print(f"🌡️  Temperature: {current.get('temp_c', 'N/A')}°C")
            
            # Check air quality
            air_quality = current.get('air_quality', {})
            print(f"\n🌬️  Air Quality Data:")
            print(f"   Raw data: {air_quality}")
            
            if air_quality:
                print(f"   US EPA Index: {air_quality.get('us-epa-index', 'N/A')}")
                print(f"   US EPA Index (alt): {air_quality.get('us_epa_index', 'N/A')}")
                print(f"   EPA: {air_quality.get('epa', 'N/A')}")
                print(f"   GB Defra Index: {air_quality.get('gb-defra-index', 'N/A')}")
                print(f"   All keys: {list(air_quality.keys())}")
            else:
                print("   ❌ No air quality data available")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_aqi_data()
