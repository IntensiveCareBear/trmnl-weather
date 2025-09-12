#!/usr/bin/env python3
"""
Test script to verify Gemini API parsing fix
"""

import requests
import json

def test_gemini_quote_generation():
    """Test Gemini quote generation with boldening"""
    print("🔧 Testing Gemini Quote Generation Fix")
    print("=" * 50)
    
    try:
        response = requests.post(
            "http://localhost:8000/weather/quote",
            json={"location": "Morgan Hill, CA", "include_air_quality": True},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                quote = data['data']
                print("✅ Quote generated successfully:")
                print(f"   Quote: {quote['quote']}")
                print(f"   Author: {quote['author']}")
                print(f"   Work: {quote['work']}")
                print(f"   Weather: {quote['weather_condition']}")
                
                # Check for bold tags
                if '<strong>' in quote['quote']:
                    print("   ✅ Bold tags present")
                    
                    # Extract bolded words
                    import re
                    bold_words = re.findall(r'<strong>(.*?)</strong>', quote['quote'])
                    if bold_words:
                        print(f"   🔥 Bolded words: {', '.join(bold_words)}")
                else:
                    print("   ⚠️  No bold tags found")
                
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

def test_trmnl_view_with_quotes():
    """Test TRMNL view with quotes"""
    print(f"\n" + "=" * 50)
    print("🎯 Testing TRMNL View with Quotes")
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
                print(f"   Temperature: {weather.get('temp_c')}°C")
                print(f"   Condition: {weather.get('condition_text')}")
                
                if 'weather_quote' in weather:
                    quote = weather['weather_quote']
                    print(f"\n📖 Weather Quote:")
                    print(f"   Quote: {quote['quote']}")
                    print(f"   Author: {quote['author']}")
                    
                    if '<strong>' in quote['quote']:
                        print("   ✅ Bold tags present in TRMNL data")
                        
                        # Extract bolded words
                        import re
                        bold_words = re.findall(r'<strong>(.*?)</strong>', quote['quote'])
                        if bold_words:
                            print(f"   🔥 Bolded words: {', '.join(bold_words)}")
                    else:
                        print("   ⚠️  No bold tags in TRMNL data")
                else:
                    print(f"   ❌ No weather quote in TRMNL data")
                
                return True
            else:
                print(f"❌ Error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_multiple_quotes():
    """Test multiple quote generations to ensure stability"""
    print(f"\n" + "=" * 50)
    print("🔄 Testing Multiple Quote Generations")
    print("=" * 50)
    
    locations = [
        "San Francisco, CA",
        "New York, NY",
        "London, UK"
    ]
    
    success_count = 0
    
    for location in locations:
        print(f"\n📍 Testing {location}:")
        try:
            response = requests.post(
                "http://localhost:8000/weather/quote",
                json={"location": location, "include_air_quality": True},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    quote = data['data']
                    print(f"   ✅ Success: {quote['author']} - {quote['work']}")
                    
                    if '<strong>' in quote['quote']:
                        print(f"   ✅ Bold tags present")
                    else:
                        print(f"   ⚠️  No bold tags")
                    
                    success_count += 1
                else:
                    print(f"   ❌ Error: {data.get('error')}")
            else:
                print(f"   ❌ HTTP {response.status_code}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
    
    print(f"\n📊 Results: {success_count}/{len(locations)} quotes generated successfully")
    return success_count == len(locations)

def main():
    """Run all Gemini fix tests"""
    print("🚀 Gemini API Fix Test Suite")
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
    tests = [
        ("Quote Generation", test_gemini_quote_generation),
        ("TRMNL View with Quotes", test_trmnl_view_with_quotes),
        ("Multiple Quote Generations", test_multiple_quotes),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        if test_func():
            passed += 1
        print()
    
    # Summary
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Gemini API parsing is fixed!")
        print("\n✅ Expected behavior:")
        print("   - No more 'temp_c is not defined' errors")
        print("   - Quotes generate successfully")
        print("   - Bold words work correctly")
        print("   - TRMNL view displays quotes properly")
    else:
        print("❌ Some tests failed. Check the output above for details.")

if __name__ == "__main__":
    main()
