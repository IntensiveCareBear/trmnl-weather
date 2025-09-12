#!/usr/bin/env python3
"""
Test script to verify the exact webhook data format being sent to TRMNL
"""

import requests
import json

def test_webhook_data_format():
    """Test the exact data format being sent to TRMNL"""
    print("🔍 Testing TRMNL Webhook Data Format")
    print("=" * 50)
    
    try:
        # Test the TRMNL view endpoint
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {data['success']}")
            
            if data['success']:
                weather_data = data['data']
                
                # This is what gets sent to TRMNL webhook
                webhook_payload = {
                    "merge_variables": weather_data
                }
                
                print(f"\n📦 Webhook Payload Structure:")
                print(f"   Top level: {list(webhook_payload.keys())}")
                print(f"   merge_variables: {list(webhook_payload['merge_variables'].keys())}")
                
                # Show key data points
                print(f"\n🌤️  Key Weather Data:")
                print(f"   Location: {weather_data.get('location_name')}")
                print(f"   Temperature: {weather_data.get('temp_c')}°C")
                print(f"   Condition: {weather_data.get('condition_text')}")
                print(f"   Feels Like: {weather_data.get('feels_like_c')}°C")
                print(f"   Wind: {weather_data.get('wind_kph')} kph {weather_data.get('wind_dir')}")
                print(f"   Wind Chill: {weather_data.get('windchill_c')}°C")
                print(f"   UV Index: {weather_data.get('uv_index')}")
                print(f"   AQI: {weather_data.get('aqi_us')}")
                print(f"   Time: {weather_data.get('formatted_time')}")
                
                # Check for quote
                if 'weather_quote' in weather_data:
                    quote = weather_data['weather_quote']
                    print(f"\n📖 Weather Quote:")
                    print(f"   Quote: \"{quote['quote']}\"")
                    print(f"   Author: {quote['author']}")
                    print(f"   Work: {quote['work']}")
                    print(f"   Weather: {quote['weather_condition']}")
                else:
                    print(f"\n❌ No weather quote found")
                
                # Show the complete payload (truncated)
                print(f"\n📄 Complete Webhook Payload (first 1000 chars):")
                payload_str = json.dumps(webhook_payload, indent=2)
                print(payload_str[:1000] + "..." if len(payload_str) > 1000 else payload_str)
                
                # Save full payload to file for inspection
                with open('webhook_payload.json', 'w') as f:
                    json.dump(webhook_payload, f, indent=2)
                print(f"\n💾 Full payload saved to: webhook_payload.json")
                
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_manual_webhook_send():
    """Test sending data manually to TRMNL webhook"""
    print(f"\n" + "=" * 50)
    print("📤 Testing Manual Webhook Send...")
    
    # Read webhook URL from .secrets
    webhook_url = None
    try:
        with open('.secrets', 'r') as f:
            for line in f:
                if line.startswith('TRMNL_WEBHOOK_URL='):
                    webhook_url = line.split('=')[1].strip()
                    break
    except Exception as e:
        print(f"❌ Could not read .secrets file: {e}")
        return
    
    if not webhook_url:
        print("❌ No webhook URL found in .secrets file")
        return
    
    print(f"🌐 Webhook URL: {webhook_url}")
    
    # Get the actual data that would be sent
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                weather_data = data['data']
                webhook_payload = {
                    "merge_variables": weather_data
                }
                
                print("📤 Sending data to TRMNL webhook...")
                webhook_response = requests.post(
                    webhook_url,
                    json=webhook_payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30
                )
                
                print(f"📥 Webhook Response Status: {webhook_response.status_code}")
                print(f"📥 Webhook Response Body: {webhook_response.text}")
                
                if webhook_response.status_code == 200:
                    print("✅ Data sent successfully to TRMNL!")
                else:
                    print(f"❌ TRMNL webhook returned error: {webhook_response.status_code}")
                    
            else:
                print(f"❌ Could not get weather data: {data.get('error')}")
        else:
            print(f"❌ Could not get weather data: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Manual webhook test failed: {e}")

if __name__ == "__main__":
    test_webhook_data_format()
    test_manual_webhook_send()
