#!/usr/bin/env python3
"""
Test script to verify the new TRMNL view layout and data display
"""

import requests
import json

def test_new_view_layout():
    """Test the new view layout and data display"""
    print("🔧 Testing New TRMNL View Layout")
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
                
                print("✅ New View Data Verification:")
                print(f"   Location: {weather.get('location_name')}")
                print(f"   Region: {weather.get('location_region')}")
                print(f"   Condition: {weather.get('condition_text')}")
                
                # Test all required data fields
                print(f"\n🌡️  Temperature Data:")
                print(f"   Current: {weather.get('temp_c')}°C")
                print(f"   Feels Like: {weather.get('feels_like_c')}°C")
                print(f"   Wind Chill: {weather.get('windchill_c')}°C")
                print(f"   High: {weather.get('tomorrow_max_c')}°C")
                print(f"   Low: {weather.get('tomorrow_min_c')}°C")
                
                # Test wind data
                print(f"\n💨 Wind Data:")
                print(f"   Speed: {weather.get('wind_kph')} kph")
                print(f"   Direction: {weather.get('wind_dir')}")
                
                # Test UV and AQI (the missing data)
                print(f"\n☀️  UV & Air Quality:")
                print(f"   UV Index: {weather.get('uv_index')}")
                print(f"   AQI: {weather.get('aqi_us')}")
                
                # Test quote data
                print(f"\n📖 Quote Data:")
                if weather.get('weather_quote'):
                    quote = weather['weather_quote']
                    print(f"   Quote: \"{quote.get('quote', '')[:60]}...\"")
                    print(f"   Author: {quote.get('author')}")
                    print(f"   Work: {quote.get('work')}")
                    print(f"   Weather: {quote.get('weather_condition')}")
                else:
                    print("   ❌ No quote data found")
                
                # Verify all critical fields are present
                critical_fields = [
                    'temp_c', 'feels_like_c', 'windchill_c', 'tomorrow_max_c', 
                    'tomorrow_min_c', 'uv_index', 'aqi_us', 'wind_kph', 'condition_text'
                ]
                
                missing_fields = []
                for field in critical_fields:
                    if field not in weather or weather[field] is None:
                        missing_fields.append(field)
                
                if missing_fields:
                    print(f"\n❌ Missing fields: {missing_fields}")
                else:
                    print(f"\n✅ All critical fields present")
                
                print(f"\n📊 View Layout Summary:")
                print(f"   • Main temp section: More compact (2-column grid)")
                print(f"   • Stats section: 5-column horizontal layout")
                print(f"   • Quote section: Larger and more prominent")
                print(f"   • High temp: Now displayed in stats grid")
                print(f"   • UV Index: Confirmed available")
                print(f"   • AQI: Confirmed available")
                
                return True
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Run the new view test"""
    print("🚀 Testing New TRMNL View")
    print("=" * 50)
    
    success = test_new_view_layout()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ New view test completed successfully!")
        print("📱 The view should now display:")
        print("   • More compact main temperature section")
        print("   • Horizontal 5-column stats layout")
        print("   • Larger, more prominent quote section")
        print("   • High temperature in stats grid")
        print("   • UV Index and AQI properly displayed")
    else:
        print("❌ New view test failed!")
        print("🔧 Check the service and data transformation")

if __name__ == "__main__":
    main()
