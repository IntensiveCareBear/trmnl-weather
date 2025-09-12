"""
Gemini API service for fetching weather-matching quotes from classic literature
"""

import httpx
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class WeatherQuote:
    """Weather quote data structure"""
    quote: str
    author: str
    work: str
    weather_condition: str
    timestamp: datetime
    location: str

class GeminiQuoteService:
    """Service for fetching weather-matching quotes from Gemini AI"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.quotes_cache: Dict[str, WeatherQuote] = {}
        self.last_update: Dict[str, datetime] = {}
        self.update_interval = timedelta(minutes=30)
    
    async def get_weather_quote(self, location: str, weather_data: Dict[str, Any]) -> Optional[WeatherQuote]:
        """Get a weather-matching quote for the given location and weather data"""
        cache_key = f"{location}_{weather_data.get('condition_text', 'unknown')}"
        
        # Check if we have a recent quote in cache
        if self._is_quote_fresh(cache_key):
            logger.info(f"Returning cached quote for {location}")
            return self.quotes_cache.get(cache_key)
        
        # Generate new quote
        try:
            quote = await self._generate_quote(location, weather_data)
            if quote:
                self.quotes_cache[cache_key] = quote
                self.last_update[cache_key] = datetime.utcnow()
                logger.info(f"Generated new quote for {location}: {weather_data.get('condition_text', 'unknown')}")
                return quote
        except Exception as e:
            logger.error(f"Error generating quote for {location}: {str(e)}")
            # Return cached quote if available, even if stale
            return self.quotes_cache.get(cache_key)
        
        return None
    
    def _is_quote_fresh(self, cache_key: str) -> bool:
        """Check if the cached quote is still fresh"""
        if cache_key not in self.quotes_cache or cache_key not in self.last_update:
            return False
        
        time_since_update = datetime.utcnow() - self.last_update[cache_key]
        return time_since_update < self.update_interval
    
    async def _generate_quote(self, location: str, weather_data: Dict[str, Any]) -> Optional[WeatherQuote]:
        """Generate a weather-matching quote using Gemini API"""
        condition = weather_data.get('condition_text', 'unknown weather')
        temp_c = weather_data.get('temp_c', 0)
        wind_speed = weather_data.get('wind_kph', 0)
        
        # Create a detailed prompt for Gemini
        prompt = self._create_weather_prompt(location, condition, temp_c, wind_speed)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/models/gemini-pro:generateContent",
                    headers={
                        "Content-Type": "application/json",
                        "x-goog-api-key": self.api_key
                    },
                    json={
                        "contents": [{
                            "parts": [{
                                "text": prompt
                            }]
                        }],
                        "generationConfig": {
                            "temperature": 0.7,
                            "topK": 40,
                            "topP": 0.95,
                            "maxOutputTokens": 300
                        }
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                
                result = response.json()
                return self._parse_gemini_response(result, condition, location)
                
        except httpx.HTTPStatusError as e:
            logger.error(f"Gemini API error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error calling Gemini API: {str(e)}")
            return None
    
    def _create_weather_prompt(self, location: str, condition: str, temp_c: float, wind_speed: float) -> str:
        """Create a detailed prompt for Gemini based on weather conditions"""
        
        # Determine weather mood and characteristics
        weather_mood = self._get_weather_mood(condition, temp_c, wind_speed)
        
        prompt = f"""
Find a beautiful, poetic quote from classic literature that matches this weather condition:

Location: {location}
Weather: {condition}
Temperature: {temp_c}°C
Wind: {wind_speed} km/h
Mood: {weather_mood}

Please provide:
1. A quote from classic literature (pre-1950) that captures the essence of this weather
2. The author's name
3. The title of the work
4. A brief explanation of why this quote matches the weather

Format your response as JSON:
{{
    "quote": "the actual quote text",
    "author": "Author Name",
    "work": "Book/Work Title",
    "explanation": "brief explanation of the connection"
}}

Focus on quotes that evoke the feeling, atmosphere, or mood of this specific weather condition. Choose from well-known classic authors like Shakespeare, Dickens, Austen, Bronte, Twain, etc.
"""
        return prompt
    
    def _get_weather_mood(self, condition: str, temp_c: float, wind_speed: float) -> str:
        """Determine the mood/atmosphere of the weather"""
        condition_lower = condition.lower()
        
        if any(word in condition_lower for word in ['sunny', 'clear', 'bright']):
            return "cheerful, bright, optimistic"
        elif any(word in condition_lower for word in ['cloudy', 'overcast', 'grey']):
            return "melancholic, contemplative, subdued"
        elif any(word in condition_lower for word in ['rain', 'drizzle', 'shower']):
            return "romantic, nostalgic, peaceful"
        elif any(word in condition_lower for word in ['storm', 'thunder', 'lightning']):
            return "dramatic, powerful, intense"
        elif any(word in condition_lower for word in ['snow', 'blizzard', 'winter']):
            return "serene, magical, quiet"
        elif any(word in condition_lower for word in ['fog', 'mist', 'haze']):
            return "mysterious, ethereal, dreamlike"
        elif temp_c > 25:
            return "lazy, languid, warm"
        elif temp_c < 5:
            return "crisp, invigorating, cold"
        elif wind_speed > 20:
            return "energetic, restless, dynamic"
        else:
            return "calm, peaceful, gentle"
    
    def _parse_gemini_response(self, response: Dict[str, Any], condition: str, location: str) -> Optional[WeatherQuote]:
        """Parse Gemini API response and create WeatherQuote object"""
        try:
            # Extract text from Gemini response
            candidates = response.get('candidates', [])
            if not candidates:
                logger.error("No candidates in Gemini response")
                return None
            
            content = candidates[0].get('content', {})
            parts = content.get('parts', [])
            if not parts:
                logger.error("No parts in Gemini response content")
                return None
            
            text = parts[0].get('text', '')
            if not text:
                logger.error("No text in Gemini response")
                return None
            
            # Try to parse JSON from the response
            # Sometimes Gemini includes extra text, so we need to extract JSON
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.error("No JSON found in Gemini response")
                return None
            
            json_text = text[json_start:json_end]
            quote_data = json.loads(json_text)
            
            return WeatherQuote(
                quote=quote_data.get('quote', ''),
                author=quote_data.get('author', 'Unknown'),
                work=quote_data.get('work', 'Unknown Work'),
                weather_condition=condition,
                timestamp=datetime.utcnow(),
                location=location
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini response: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {str(e)}")
            return None
    
    async def refresh_quotes(self) -> None:
        """Refresh all cached quotes that are older than the update interval"""
        current_time = datetime.utcnow()
        stale_keys = []
        
        for cache_key, last_update in self.last_update.items():
            if current_time - last_update >= self.update_interval:
                stale_keys.append(cache_key)
        
        logger.info(f"Refreshing {len(stale_keys)} stale quotes")
        
        # Remove stale quotes (they'll be regenerated on next request)
        for key in stale_keys:
            if key in self.quotes_cache:
                del self.quotes_cache[key]
            if key in self.last_update:
                del self.last_update[key]
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics about the quote cache"""
        return {
            "total_cached_quotes": len(self.quotes_cache),
            "cache_keys": list(self.quotes_cache.keys()),
            "last_updates": {k: v.isoformat() for k, v in self.last_update.items()}
        }
