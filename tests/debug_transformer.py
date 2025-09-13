#!/usr/bin/env python3
"""
Debug script to check what's happening in the data transformer
"""

import requests
import json

def debug_data_transformer():
    """Debug the data transformer to see why tomorrow's data is missing"""
    print("🔍 Debugging Data Transformer")
    print("=" * 50)
    
    try:
        # Get raw forecast data
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
                
                # Check the exact structure
                forecast = forecast_data.get('forecast', {})
                print(f"   Forecast keys: {list(forecast.keys())}")
                
                forecastday = forecast.get('forecastday', [])
                print(f"   Forecastday length: {len(forecastday)}")
                
                if forecastday:
                    first_day = forecastday[0]
                    print(f"   First day keys: {list(first_day.keys())}")
                    
                    day_data = first_day.get('day', {})
                    print(f"   Day data keys: {list(day_data.keys())}")
                    
                    print(f"   Tomorrow's raw data:")
                    print(f"     - maxtemp_c: {day_data.get('maxtemp_c')}")
                    print(f"     - mintemp_c: {day_data.get('mintemp_c')}")
                    print(f"     - maxtemp_c type: {type(day_data.get('maxtemp_c'))}")
                    print(f"     - mintemp_c type: {type(day_data.get('mintemp_c'))}")
                    
                    # Test the rounding logic
                    maxtemp = day_data.get('maxtemp_c')
                    mintemp = day_data.get('mintemp_c')
                    
                    print(f"\n🧮 Rounding Logic Test:")
                    print(f"   maxtemp_c: {maxtemp} -> round() -> {round(maxtemp) if maxtemp is not None else None}")
                    print(f"   mintemp_c: {mintemp} -> round() -> {round(mintemp) if mintemp is not None else None}")
                    
                    # Test the full condition
                    tomorrow_data = first_day.get('day', {})
                    max_condition = tomorrow_data and tomorrow_data.get('maxtemp_c') is not None
                    min_condition = tomorrow_data and tomorrow_data.get('mintemp_c') is not None
                    
                    print(f"\n✅ Condition Tests:")
                    print(f"   tomorrow_data exists: {tomorrow_data is not None}")
                    print(f"   tomorrow_data keys: {list(tomorrow_data.keys()) if tomorrow_data else 'None'}")
                    print(f"   maxtemp_c condition: {max_condition}")
                    print(f"   mintemp_c condition: {min_condition}")
                    
                    return True
                else:
                    print(f"   ❌ No forecastday data found")
                    return False
            else:
                print(f"❌ Forecast API error: {data.get('error')}")
                return False
        else:
            print(f"❌ Forecast HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_trmnl_view_debug():
    """Test TRMNL view and debug the transformation"""
    print(f"\n🔧 Testing TRMNL View Transformation")
    print("=" * 40)
    
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
                
                print("📱 TRMNL View Transformed Data:")
                print(f"   tomorrow_max_c: {weather.get('tomorrow_max_c')} (type: {type(weather.get('tomorrow_max_c'))})")
                print(f"   tomorrow_min_c: {weather.get('tomorrow_min_c')} (type: {type(weather.get('tomorrow_min_c'))})")
                
                # Check if they're actually None or 0
                max_val = weather.get('tomorrow_max_c')
                min_val = weather.get('tomorrow_min_c')
                
                print(f"\n🔍 Value Analysis:")
                print(f"   tomorrow_max_c is None: {max_val is None}")
                print(f"   tomorrow_max_c == 0: {max_val == 0}")
                print(f"   tomorrow_max_c == 'None': {max_val == 'None'}")
                
                print(f"   tomorrow_min_c is None: {min_val is None}")
                print(f"   tomorrow_min_c == 0: {min_val == 0}")
                print(f"   tomorrow_min_c == 'None': {min_val == 'None'}")
                
                return True
            else:
                print(f"❌ TRMNL view error: {data.get('error')}")
                return False
        else:
            print(f"❌ TRMNL view HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ TRMNL view request failed: {e}")
        return False

def main():
    """Run the debug tests"""
    print("🚀 Debugging Data Transformer Issue")
    print("=" * 50)
    
    # Debug raw forecast data
    forecast_debug = debug_data_transformer()
    
    # Debug TRMNL view transformation
    view_debug = test_trmnl_view_debug()
    
    print(f"\n" + "=" * 50)
    print("📊 Debug Summary:")
    print(f"   Raw Forecast Data: {'✅ OK' if forecast_debug else '❌ FAIL'}")
    print(f"   TRMNL View Transform: {'✅ OK' if view_debug else '❌ FAIL'}")

if __name__ == "__main__":
    main()