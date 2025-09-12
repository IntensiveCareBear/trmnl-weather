#!/usr/bin/env python3
"""
Test script to verify that forecast data is now being retrieved for high/low temperatures
"""

import requests
import json

def test_forecast_data():
    """Test that forecast data is now being retrieved"""
    print("🔧 Testing Forecast Data Fix")
    print("=" * 50)
    
    try:
        # Test the TRMNL view endpoint with default days=1
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "Morgan Hill, CA", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                weather = data['data']
                
                print("✅ Forecast Data Test Results:")
                print(f"   Location: {weather.get('location_name')}")
                print(f"   Current Temp: {weather.get('temp_c')}°C")
                print(f"   Feels Like: {weather.get('feels_like_c')}°C")
                
                # Check the critical missing fields
                print(f"\n🌡️  Temperature Range:")
                high_temp = weather.get('tomorrow_max_c')
                low_temp = weather.get('tomorrow_min_c')
                
                print(f"   High Temperature: {high_temp}°C")
                print(f"   Low Temperature: {low_temp}°C")
                
                if high_temp is not None and low_temp is not None:
                    print(f"   ✅ SUCCESS: Both high and low temperatures are now available!")
                    return True
                else:
                    print(f"   ❌ FAILED: High/Low temperatures still missing")
                    if high_temp is None:
                        print(f"      - tomorrow_max_c is None")
                    if low_temp is None:
                        print(f"      - tomorrow_min_c is None")
                    return False
            else:
                print(f"❌ API returned success=false: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_direct_forecast_api():
    """Test the forecast API directly to see raw data"""
    print(f"\n🔍 Testing Direct Forecast API")
    print("=" * 30)
    
    try:
        # Test the forecast endpoint directly
        response = requests.post(
            "http://localhost:8000/weather/forecast",
            json={"location": "Morgan Hill, CA", "days": 1, "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                forecast_data = data['data']
                
                print("📊 Raw Forecast Data Structure:")
                print(f"   Location: {forecast_data.get('location', {}).get('name')}")
                
                # Check forecast structure
                forecast = forecast_data.get('forecast', {})
                forecastday = forecast.get('forecastday', [])
                
                print(f"   Forecast days available: {len(forecastday)}")
                
                if forecastday:
                    first_day = forecastday[0]
                    day_data = first_day.get('day', {})
                    
                    print(f"   Tomorrow's data:")
                    print(f"     - Max temp: {day_data.get('maxtemp_c')}°C")
                    print(f"     - Min temp: {day_data.get('mintemp_c')}°C")
                    print(f"     - Condition: {day_data.get('condition', {}).get('text')}")
                    
                    return True
                else:
                    print(f"   ❌ No forecast day data found")
                    return False
            else:
                print(f"❌ Forecast API error: {data.get('error')}")
                return False
        else:
            print(f"❌ Forecast HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Forecast request failed: {e}")
        return False

def main():
    """Run the forecast fix tests"""
    print("🚀 Testing Forecast Data Fix")
    print("=" * 50)
    
    # Test direct forecast API first
    forecast_success = test_direct_forecast_api()
    
    print(f"\n" + "=" * 50)
    
    # Test TRMNL view with forecast data
    view_success = test_forecast_data()
    
    print(f"\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Direct Forecast API: {'✅ PASS' if forecast_success else '❌ FAIL'}")
    print(f"   TRMNL View with Forecast: {'✅ PASS' if view_success else '❌ FAIL'}")
    
    if forecast_success and view_success:
        print(f"\n🎉 SUCCESS: Forecast data is now working!")
        print(f"   High and low temperatures should now be available in the TRMNL view")
    else:
        print(f"\n❌ FAILED: Forecast data still has issues")
        print(f"   Check the service logs and API responses")

if __name__ == "__main__":
    main()
