#!/usr/bin/env python3
"""
Test script to verify boldened weather quotes
"""

import requests
import json

def test_bold_quotes():
    """Test that quotes have boldened weather words"""
    print("🔍 Testing Boldened Weather Quotes")
    print("=" * 50)
    
    # Test different weather conditions
    test_conditions = [
        {"location": "London", "condition": "Sunny", "temp": 25, "wind": 10},
        {"location": "New York", "condition": "Rainy", "temp": 15, "wind": 20},
        {"location": "Tokyo", "condition": "Cloudy", "temp": 18, "wind": 5},
        {"location": "Paris", "condition": "Stormy", "temp": 12, "wind": 30},
        {"location": "Sydney", "condition": "Snowy", "temp": -2, "wind": 15}
    ]
    
    for test in test_conditions:
        print(f"\n🌤️  Testing {test['condition']} weather in {test['location']}")
        print("-" * 40)
        
        try:
            response = requests.post(
                "http://localhost:8000/weather/quote",
                json={
                    "location": test['location'],
                    "include_air_quality": True
                },
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    quote = data['data']
                    print(f"✅ Quote generated:")
                    print(f"   Quote: {quote['quote']}")
                    print(f"   Author: {quote['author']}")
                    print(f"   Work: {quote['work']}")
                    
                    # Check if quote contains bold tags
                    if '<strong>' in quote['quote']:
                        print(f"   ✅ Bold tags found!")
                        
                        # Extract bolded words
                        import re
                        bold_words = re.findall(r'<strong>(.*?)</strong>', quote['quote'])
                        if bold_words:
                            print(f"   🔥 Bolded words: {', '.join(bold_words)}")
                    else:
                        print(f"   ⚠️  No bold tags found")
                else:
                    print(f"   ❌ Error: {data.get('error')}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Request failed: {e}")

def test_trmnl_view_with_bold_quotes():
    """Test TRMNL view with boldened quotes"""
    print(f"\n" + "=" * 50)
    print("🎯 Testing TRMNL View with Bold Quotes")
    print("=" * 50)
    
    try:
        response = requests.post(
            "http://localhost:8000/weather/trmnl-view",
            json={"location": "London", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                weather = data['data']
                print(f"✅ TRMNL View Data:")
                print(f"   Location: {weather.get('location_name')}")
                print(f"   Temperature: {weather.get('temp_c')}°C")
                print(f"   Condition: {weather.get('condition_text')}")
                
                if 'weather_quote' in weather:
                    quote = weather['weather_quote']
                    print(f"\n📖 Weather Quote:")
                    print(f"   Quote: {quote['quote']}")
                    print(f"   Author: {quote['author']}")
                    
                    # Check for bold tags
                    if '<strong>' in quote['quote']:
                        print(f"   ✅ Bold tags present in TRMNL data!")
                        
                        # Extract bolded words
                        import re
                        bold_words = re.findall(r'<strong>(.*?)</strong>', quote['quote'])
                        if bold_words:
                            print(f"   🔥 Bolded words: {', '.join(bold_words)}")
                    else:
                        print(f"   ⚠️  No bold tags in TRMNL data")
                else:
                    print(f"   ❌ No weather quote in TRMNL data")
            else:
                print(f"   ❌ Error: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Request failed: {e}")

def test_manual_boldening():
    """Test the boldening function directly"""
    print(f"\n" + "=" * 50)
    print("🔧 Testing Manual Boldening Function")
    print("=" * 50)
    
    # Import the gemini service to test the function directly
    try:
        from gemini_service import GeminiQuoteService
        
        # Create a test instance
        gemini_service = GeminiQuoteService("test_key")
        
        # Test quotes with different weather conditions
        test_quotes = [
            {
                "quote": "The sun was shining brightly in the clear sky.",
                "condition": "Sunny",
                "temp": 25,
                "wind": 10
            },
            {
                "quote": "The wind howled through the stormy night.",
                "condition": "Stormy", 
                "temp": 15,
                "wind": 30
            },
            {
                "quote": "Rain fell gently on the quiet street.",
                "condition": "Rainy",
                "temp": 18,
                "wind": 5
            }
        ]
        
        for test in test_quotes:
            print(f"\n🧪 Testing: {test['condition']}")
            print(f"   Original: {test['quote']}")
            
            boldened = gemini_service._bolden_weather_words(
                test['quote'], 
                test['condition'], 
                test['temp'], 
                test['wind']
            )
            
            print(f"   Boldened: {boldened}")
            
            # Check if any words were boldened
            if '<strong>' in boldened:
                import re
                bold_words = re.findall(r'<strong>(.*?)</strong>', boldened)
                print(f"   ✅ Bolded words: {', '.join(bold_words)}")
            else:
                print(f"   ⚠️  No words were boldened")
                
    except Exception as e:
        print(f"   ❌ Error testing boldening function: {e}")

def main():
    """Run all bold quote tests"""
    print("🚀 Bold Weather Quotes Test Suite")
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
    test_bold_quotes()
    test_trmnl_view_with_bold_quotes()
    test_manual_boldening()
    
    print("\n" + "=" * 50)
    print("🎉 Bold Quote Testing Complete!")
    print("\n💡 What to expect:")
    print("   - Weather-related words should be <strong>bolded</strong>")
    print("   - Words like 'sun', 'wind', 'rain', 'cloud' should be highlighted")
    print("   - Bold tags should appear in both API responses and TRMNL views")

if __name__ == "__main__":
    main()
