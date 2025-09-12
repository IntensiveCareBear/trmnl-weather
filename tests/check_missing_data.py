#!/usr/bin/env python3
"""
Quick check to see what data might be missing from the TRMNL view
"""

import requests
import json

def check_data():
    """Check what data is available and what might be missing"""
    print("🔍 Checking TRMNL View Data Availability")
    print("=" * 50)
    
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
                
                print("📊 Available Data Fields:")
                print("=" * 30)
                
                # Check all fields that should be in the view
                fields_to_check = {
                    'temp_c': 'Current Temperature',
                    'feels_like_c': 'Feels Like',
                    'windchill_c': 'Wind Chill',
                    'tomorrow_max_c': 'High Temperature',
                    'tomorrow_min_c': 'Low Temperature',
                    'uv_index': 'UV Index',
                    'aqi_us': 'AQI',
                    'wind_kph': 'Wind Speed',
                    'wind_dir': 'Wind Direction',
                    'condition_text': 'Weather Condition',
                    'location_name': 'Location',
                    'location_region': 'Region',
                    'formatted_time': 'Update Time',
                    'weather_quote': 'Weather Quote'
                }
                
                missing_fields = []
                present_fields = []
                
                for field, description in fields_to_check.items():
                    value = weather.get(field)
                    if value is not None and value != '':
                        present_fields.append((field, description, value))
                    else:
                        missing_fields.append((field, description))
                
                print("✅ Present Fields:")
                for field, desc, value in present_fields:
                    print(f"   {field:20} ({desc:20}): {value}")
                
                print(f"\n❌ Missing/Empty Fields:")
                if missing_fields:
                    for field, desc in missing_fields:
                        print(f"   {field:20} ({desc:20}): MISSING")
                else:
                    print("   None - all fields present!")
                
                print(f"\n📱 Current View Layout:")
                print("   Main Section:")
                print(f"     - Current Temp: {weather.get('temp_c', 'MISSING')}°C")
                print(f"     - Feels Like: {weather.get('feels_like_c', 'MISSING')}°C")
                print(f"     - Low Temp: {weather.get('tomorrow_min_c', 'MISSING')}°C")
                print("   Stats Grid (4 columns):")
                print(f"     - UV Index: {weather.get('uv_index', 'MISSING')}")
                print(f"     - AQI: {weather.get('aqi_us', 'MISSING')}")
                print(f"     - Wind: {weather.get('wind_kph', 'MISSING')} kph")
                print(f"     - High: {weather.get('tomorrow_max_c', 'MISSING')}°C")
                
                return len(missing_fields) == 0
            else:
                print(f"❌ API error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

if __name__ == "__main__":
    success = check_data()
    print(f"\n{'✅' if success else '❌'} Data check {'passed' if success else 'failed'}")
