#!/usr/bin/env python3
"""
Test script to verify view fixes: emojis, AQI, high/low temps, and rounded temperatures
"""

import requests
import json

def test_view_fixes():
    """Test all the view fixes"""
    print("🔧 Testing View Fixes")
    print("=" * 50)
    
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "Morgan Hill, CA", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                weather = data['data']
                
                print("✅ TRMNL View Data:")
                print(f"   Location: {weather.get('location_name')}")
                print(f"   Region: {weather.get('location_region')}")
                print(f"   Condition: {weather.get('condition_text')}")
                
                # Test temperature rounding
                print(f"\n🌡️  Temperature Data:")
                print(f"   Current: {weather.get('temp_c')}°C (should be integer)")
                print(f"   Feels Like: {weather.get('feels_like_c')}°C (should be integer)")
                print(f"   Wind Chill: {weather.get('windchill_c')}°C (should be integer)")
                print(f"   High: {weather.get('tomorrow_max_c')}°C (should be integer)")
                print(f"   Low: {weather.get('tomorrow_min_c')}°C (should be integer)")
                
                # Test wind data
                print(f"\n💨 Wind Data:")
                print(f"   Speed: {weather.get('wind_kph')} kph (should be integer)")
                print(f"   Direction: {weather.get('wind_dir')}")
                
                # Test UV and AQI
                print(f"\n☀️  UV & Air Quality:")
                print(f"   UV Index: {weather.get('uv_index')} (should be integer)")
                print(f"   AQI: {weather.get('aqi_us')} (should show number or —)")
                
                # Test emojis in condition
                condition = weather.get('condition_text', '')
                print(f"\n🎨 Weather Condition Emojis:")
                print(f"   Condition: {condition}")
                if 'Sunny' in condition or 'Clear' in condition:
                    print("   Expected emoji: ☀️")
                elif 'Cloudy' in condition or 'Overcast' in condition:
                    print("   Expected emoji: ☁️")
                elif 'Rain' in condition or 'Drizzle' in condition:
                    print("   Expected emoji: 🌧️")
                elif 'Storm' in condition or 'Thunder' in condition:
                    print("   Expected emoji: ⛈️")
                elif 'Snow' in condition or 'Blizzard' in condition:
                    print("   Expected emoji: ❄️")
                elif 'Fog' in condition or 'Mist' in condition:
                    print("   Expected emoji: 🌫️")
                else:
                    print("   Expected emoji: 🌤️")
                
                # Test quote with bold words
                if 'weather_quote' in weather:
                    quote = weather['weather_quote']
                    print(f"\n📖 Weather Quote:")
                    print(f"   Quote: {quote['quote']}")
                    print(f"   Author: {quote['author']}")
                    
                    if '<strong>' in quote['quote']:
                        print("   ✅ Bold tags present")
                    else:
                        print("   ⚠️  No bold tags found")
                else:
                    print(f"\n❌ No weather quote found")
                
                # Verify all temperatures are integers
                temp_fields = ['temp_c', 'feels_like_c', 'windchill_c', 'tomorrow_max_c', 'tomorrow_min_c', 'wind_kph', 'uv_index']
                all_integers = True
                
                for field in temp_fields:
                    value = weather.get(field)
                    if value is not None and value != "—":
                        if not isinstance(value, int):
                            print(f"   ❌ {field}: {value} is not an integer")
                            all_integers = False
                
                if all_integers:
                    print(f"\n✅ All temperatures and numeric values are integers!")
                else:
                    print(f"\n❌ Some values are not integers")
                
                return True
            else:
                print(f"❌ API Error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_different_locations():
    """Test with different locations to verify fixes work everywhere"""
    print(f"\n" + "=" * 50)
    print("🌍 Testing Different Locations")
    print("=" * 50)
    
    locations = [
        "San Francisco, CA",
        "New York, NY", 
        "London, UK",
        "Tokyo, Japan"
    ]
    
    for location in locations:
        print(f"\n📍 Testing {location}:")
        try:
            response = requests.post(
                "http://localhost:8000/weather/trmnl-view",
                json={"location": location, "include_air_quality": True},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    weather = data['data']
                    print(f"   ✅ {weather.get('location_name')}: {weather.get('temp_c')}°C")
                    print(f"   AQI: {weather.get('aqi_us')}, UV: {weather.get('uv_index')}")
                    print(f"   High: {weather.get('tomorrow_max_c')}°C, Low: {weather.get('tomorrow_min_c')}°C")
                else:
                    print(f"   ❌ Error: {data.get('error')}")
            else:
                print(f"   ❌ HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")

def main():
    """Run all view fix tests"""
    print("🚀 View Fixes Test Suite")
    print("=" * 50)
    
    # Check if service is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Service not running. Please start with: python3 main.py")
            return
    except:
        print("❌ Service not running. Please start with: python3 main.py")
        return
    
    print("✅ Service is running")
    
    # Run tests
    success = test_view_fixes()
    test_different_locations()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 View fixes test completed!")
        print("\n✅ Expected fixes:")
        print("   - All temperatures rounded to integers")
        print("   - AQI shows number or —")
        print("   - High/Low temps displayed")
        print("   - Emojis working for weather conditions")
        print("   - Bold words in quotes")
    else:
        print("❌ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
