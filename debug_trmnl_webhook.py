#!/usr/bin/env python3
"""
Debug script to check TRMNL webhook data delivery
"""

import requests
import json
import time

def test_webhook_delivery():
    """Test what data is being sent to TRMNL webhook"""
    print("🔍 TRMNL Webhook Delivery Debug")
    print("=" * 50)
    
    # Test the TRMNL view endpoint
    print("1. Testing TRMNL View Endpoint...")
    try:
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
                print(f"\n📊 Data being returned to client:")
                print(f"   Location: {weather_data.get('location_name')}")
                print(f"   Temperature: {weather_data.get('temp_c')}°C")
                print(f"   Condition: {weather_data.get('condition_text')}")
                
                # Check for quote
                if 'weather_quote' in weather_data:
                    quote = weather_data['weather_quote']
                    print(f"   📖 Quote: \"{quote['quote'][:50]}...\"")
                else:
                    print(f"   ❌ No quote in response")
                
                # Show the exact structure
                print(f"\n📋 Complete Response Structure:")
                print(json.dumps(weather_data, indent=2))
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_webhook_payload():
    """Test the exact payload being sent to TRMNL webhook"""
    print("\n" + "=" * 50)
    print("2. Testing Webhook Payload Format...")
    
    # Get the raw weather data that would be sent to webhook
    try:
        response = requests.post(
            "http://localhost:8000/weather/current",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                raw_weather = data['data']
                
                # This is what gets sent to TRMNL webhook
                webhook_payload = {
                    "merge_variables": raw_weather
                }
                
                print(f"📦 Webhook Payload Structure:")
                print(f"   Top level keys: {list(webhook_payload.keys())}")
                print(f"   merge_variables keys: {list(webhook_payload['merge_variables'].keys())}")
                
                # Check if this matches what TRMNL expects
                print(f"\n🔍 Key Data Points in Webhook:")
                current = raw_weather.get('current', {})
                location = raw_weather.get('location', {})
                
                print(f"   Location: {location.get('name', 'N/A')}")
                print(f"   Temperature: {current.get('temp_c', 'N/A')}°C")
                print(f"   Condition: {current.get('condition', {}).get('text', 'N/A')}")
                print(f"   Air Quality: {current.get('air_quality', {})}")
                
                # Show the complete webhook payload
                print(f"\n📄 Complete Webhook Payload:")
                print(json.dumps(webhook_payload, indent=2)[:1000] + "...")
                
            else:
                print(f"❌ API Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_trmnl_specific_endpoint():
    """Test the dedicated TRMNL webhook endpoint"""
    print("\n" + "=" * 50)
    print("3. Testing Dedicated TRMNL Webhook Endpoint...")
    
    try:
        response = requests.post(
            "http://localhost:8000/weather/send-to-trmnl",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TRMNL Webhook Response: {data['success']}")
            if 'data' in data:
                print(f"   Message: {data['data'].get('message', 'N/A')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

def check_webhook_url():
    """Check the webhook URL configuration"""
    print("\n" + "=" * 50)
    print("4. Checking Webhook Configuration...")
    
    try:
        # Read the .secrets file to check webhook URL
        with open('.secrets', 'r') as f:
            content = f.read()
            print("📋 .secrets file content:")
            for line in content.split('\n'):
                if 'TRMNL_WEBHOOK_URL' in line:
                    print(f"   {line}")
                elif 'WEATHER_API_KEY' in line:
                    print(f"   {line[:20]}...")
                elif 'GEMINI_API_KEY' in line:
                    print(f"   {line[:20]}...")
    except Exception as e:
        print(f"❌ Could not read .secrets file: {e}")

def test_manual_webhook():
    """Test sending data manually to TRMNL webhook"""
    print("\n" + "=" * 50)
    print("5. Manual Webhook Test...")
    
    # Get the webhook URL from .secrets
    webhook_url = None
    try:
        with open('.secrets', 'r') as f:
            for line in f:
                if line.startswith('TRMNL_WEBHOOK_URL='):
                    webhook_url = line.split('=')[1].strip()
                    break
    except:
        pass
    
    if not webhook_url:
        print("❌ No webhook URL found in .secrets file")
        return
    
    print(f"🌐 Webhook URL: {webhook_url}")
    
    # Create a test payload
    test_payload = {
        "merge_variables": {
            "location_name": "Test Location",
            "temp_c": 20,
            "condition_text": "Sunny",
            "weather_quote": {
                "quote": "Test quote for debugging",
                "author": "Test Author",
                "work": "Test Work"
            }
        }
    }
    
    try:
        print("📤 Sending test payload to TRMNL...")
        response = requests.post(
            webhook_url,
            json=test_payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Test payload sent successfully!")
        else:
            print(f"❌ Webhook returned error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Manual webhook test failed: {e}")

def main():
    """Run all debug tests"""
    print("🚀 TRMNL Webhook Debug Suite")
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
    
    # Run all tests
    test_webhook_delivery()
    test_webhook_payload()
    test_trmnl_specific_endpoint()
    check_webhook_url()
    test_manual_webhook()
    
    print("\n" + "=" * 50)
    print("🔍 Debug Complete!")
    print("\n💡 Common Issues:")
    print("   1. Check if webhook URL is correct in .secrets")
    print("   2. Verify TRMNL device is connected to internet")
    print("   3. Check TRMNL device logs for errors")
    print("   4. Ensure webhook URL matches your TRMNL plugin ID")

if __name__ == "__main__":
    main()
