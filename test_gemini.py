#!/usr/bin/env python3
"""
Test Gemini API integration directly
"""

import os
import asyncio
from gemini_service import GeminiQuoteService

async def test_gemini_direct():
    """Test Gemini service directly"""
    print("🤖 Testing Gemini API directly...")
    
    # Check if API key is set
    api_key = os.getenv('GEMINI_API_KEY', 'your_gemini_api_key_here')
    if api_key == 'your_gemini_api_key_here':
        print("❌ GEMINI_API_KEY not set or using placeholder")
        print("Please set your actual Gemini API key in .secrets file")
        return
    
    # Initialize service
    service = GeminiQuoteService(api_key)
    
    # Test quote generation
    try:
        quote = await service.get_weather_quote(
            "London",
            {
                'condition_text': 'Partly cloudy',
                'temp_c': 15,
                'wind_kph': 10
            }
        )
        
        if quote:
            print("✅ Quote generated successfully!")
            print(f"📖 Quote: \"{quote.quote}\"")
            print(f"👤 Author: {quote.author}")
            print(f"📚 Work: {quote.work}")
            print(f"🌤️  Weather: {quote.weather_condition}")
        else:
            print("❌ No quote generated")
            
    except Exception as e:
        print(f"❌ Error generating quote: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini_direct())
