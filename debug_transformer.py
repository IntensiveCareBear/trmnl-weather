#!/usr/bin/env python3
"""
Debug the data transformer to see why quotes aren't being included
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_transformer import WeatherDataTransformer
from gemini_service import GeminiQuoteService
from config import settings

async def test_transformer():
    """Test the data transformer directly"""
    print("🔍 Testing Data Transformer")
    print("=" * 40)
    
    # Initialize services
    gemini_service = GeminiQuoteService(settings.GEMINI_API_KEY)
    transformer = WeatherDataTransformer(gemini_service)
    
    # Mock weather data
    mock_weather_data = {
        'location': {
            'name': 'London',
            'region': 'City of London, Greater London',
            'tz_id': 'Europe/London'
        },
        'current': {
            'temp_c': 12.1,
            'feelslike_c': 10.1,
            'condition': {
                'text': 'Partly Cloudy'
            },
            'wind_kph': 21.2,
            'wind_dir': 'SW',
            'windchill_c': 10.0,
            'uv': 0.0,
            'air_quality': {
                'us-epa-index': 1
            },
            'last_updated_epoch': 1640995200
        },
        'forecast': {
            'forecastday': [{
                'day': {
                    'maxtemp_c': 15.0,
                    'mintemp_c': 8.0
                }
            }]
        }
    }
    
    print("📊 Mock Weather Data:")
    print(f"   Location: {mock_weather_data['location']['name']}")
    print(f"   Condition: {mock_weather_data['current']['condition']['text']}")
    print(f"   Temperature: {mock_weather_data['current']['temp_c']}°C")
    
    # Test quote generation
    print("\n🤖 Testing Quote Generation:")
    try:
        quote = await gemini_service.get_weather_quote(
            'London',
            {
                'condition_text': 'Partly Cloudy',
                'temp_c': 12.1,
                'wind_kph': 21.2
            }
        )
        
        if quote:
            print(f"✅ Quote generated: \"{quote.quote[:50]}...\"")
            print(f"   Author: {quote.author}")
            print(f"   Work: {quote.work}")
        else:
            print("❌ No quote generated")
    except Exception as e:
        print(f"❌ Quote generation error: {e}")
    
    # Test transformer
    print("\n🔄 Testing Data Transformer:")
    try:
        result = await transformer.transform_current_weather(mock_weather_data)
        
        print(f"✅ Transformer result keys: {list(result.keys())}")
        
        if 'weather_quote' in result:
            quote_data = result['weather_quote']
            print(f"✅ Quote included in result:")
            print(f"   Quote: \"{quote_data['quote'][:50]}...\"")
            print(f"   Author: {quote_data['author']}")
        else:
            print("❌ No weather_quote in transformer result")
            print(f"Available keys: {list(result.keys())}")
            
    except Exception as e:
        print(f"❌ Transformer error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_transformer())
