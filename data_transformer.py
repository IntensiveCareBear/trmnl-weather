"""
Data transformation service to convert WeatherAPI.com responses 
into simplified format for TRMNL view
"""

from typing import Dict, Any, Optional
from datetime import datetime
import pytz
from gemini_service import GeminiQuoteService, WeatherQuote

class WeatherDataTransformer:
    """Transform WeatherAPI.com data into TRMNL view format"""
    
    def __init__(self, gemini_service: Optional[GeminiQuoteService] = None):
        self.gemini_service = gemini_service
    
    async def transform_current_weather(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform current weather data for TRMNL view"""
        location = data.get('location', {})
        current = data.get('current', {})
        air_quality = current.get('air_quality', {})
        
        # Get tomorrow's forecast if available
        forecast = data.get('forecast', {})
        tomorrow_data = None
        if forecast and forecast.get('forecastday'):
            tomorrow_data = forecast['forecastday'][0].get('day', {})
        
        # Get weather quote if Gemini service is available
        quote_data = None
        if self.gemini_service:
            try:
                quote = await self.gemini_service.get_weather_quote(
                    location.get('name', 'Unknown'),
                    {
                        'condition_text': current.get('condition', {}).get('text', ''),
                        'temp_c': current.get('temp_c', 0),
                        'wind_kph': current.get('wind_kph', 0)
                    }
                )
                if quote:
                    quote_data = {
                        'quote': quote.quote,
                        'author': quote.author,
                        'work': quote.work,
                        'weather_condition': quote.weather_condition
                    }
            except Exception as e:
                print(f"Error getting weather quote: {e}")
        
        result = {
            # Location info
            'location_name': location.get('name', 'Unknown'),
            'location_region': location.get('region', ''),
            'timezone': location.get('tz_id', ''),
            
            # Current weather
            'temp_c': current.get('temp_c'),
            'feels_like_c': current.get('feelslike_c'),
            'condition_text': current.get('condition', {}).get('text', ''),
            
            # Wind info
            'wind_kph': current.get('wind_kph'),
            'wind_dir': current.get('wind_dir', ''),
            'windchill_c': current.get('windchill_c'),
            
            # Temperature range (tomorrow's forecast)
            'tomorrow_max_c': tomorrow_data.get('maxtemp_c') if tomorrow_data else None,
            'tomorrow_min_c': tomorrow_data.get('mintemp_c') if tomorrow_data else None,
            
            # UV Index
            'uv_index': current.get('uv', 0),
            
            # Air Quality Index (US EPA)
            'aqi_us': air_quality.get('us-epa-index', 0),
            
            # Timestamp
            'formatted_time': WeatherDataTransformer._format_timestamp(
                current.get('last_updated_epoch'),
                location.get('tz_id')
            )
        }
        
        # Add quote data if available
        if quote_data:
            result['weather_quote'] = quote_data
        
        return result
    
    async def transform_forecast(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform forecast data for TRMNL view"""
        location = data.get('location', {})
        current = data.get('current', {})
        forecast = data.get('forecast', {})
        
        # Get tomorrow's data (first forecast day)
        tomorrow_data = None
        if forecast and forecast.get('forecastday'):
            tomorrow_data = forecast['forecastday'][0].get('day', {})
        
        air_quality = current.get('air_quality', {})
        
        # Get weather quote if Gemini service is available
        quote_data = None
        if self.gemini_service:
            try:
                quote = await self.gemini_service.get_weather_quote(
                    location.get('name', 'Unknown'),
                    {
                        'condition_text': current.get('condition', {}).get('text', ''),
                        'temp_c': current.get('temp_c', 0),
                        'wind_kph': current.get('wind_kph', 0)
                    }
                )
                if quote:
                    quote_data = {
                        'quote': quote.quote,
                        'author': quote.author,
                        'work': quote.work,
                        'weather_condition': quote.weather_condition
                    }
            except Exception as e:
                print(f"Error getting weather quote: {e}")
        
        result = {
            # Location info
            'location_name': location.get('name', 'Unknown'),
            'location_region': location.get('region', ''),
            'timezone': location.get('tz_id', ''),
            
            # Current weather
            'temp_c': current.get('temp_c'),
            'feels_like_c': current.get('feelslike_c'),
            'condition_text': current.get('condition', {}).get('text', ''),
            
            # Wind info
            'wind_kph': current.get('wind_kph'),
            'wind_dir': current.get('wind_dir', ''),
            'windchill_c': current.get('windchill_c'),
            
            # Temperature range (tomorrow's forecast)
            'tomorrow_max_c': tomorrow_data.get('maxtemp_c') if tomorrow_data else None,
            'tomorrow_min_c': tomorrow_data.get('mintemp_c') if tomorrow_data else None,
            
            # UV Index
            'uv_index': current.get('uv', 0),
            
            # Air Quality Index (US EPA)
            'aqi_us': air_quality.get('us-epa-index', 0),
            
            # Timestamp
            'formatted_time': WeatherDataTransformer._format_timestamp(
                current.get('last_updated_epoch'),
                location.get('tz_id')
            )
        }
        
        # Add quote data if available
        if quote_data:
            result['weather_quote'] = quote_data
        
        return result
    
    @staticmethod
    def _format_timestamp(epoch: Optional[int], timezone_str: Optional[str]) -> str:
        """Format timestamp for display"""
        if not epoch:
            return "—"
        
        try:
            # Convert epoch to datetime
            dt = datetime.fromtimestamp(epoch)
            
            # Apply timezone if available
            if timezone_str:
                tz = pytz.timezone(timezone_str)
                dt = dt.replace(tzinfo=pytz.UTC).astimezone(tz)
            
            # Format as readable time
            return dt.strftime("%I:%M %p")
        except Exception:
            return "—"
    
    @staticmethod
    def get_aqi_status(aqi_value: int) -> str:
        """Get AQI status description"""
        if aqi_value <= 1:
            return "Good"
        elif aqi_value <= 2:
            return "Moderate"
        elif aqi_value <= 3:
            return "Unhealthy for Sensitive Groups"
        elif aqi_value <= 4:
            return "Unhealthy"
        elif aqi_value <= 5:
            return "Very Unhealthy"
        else:
            return "Hazardous"
    
    @staticmethod
    def get_uv_status(uv_value: int) -> str:
        """Get UV index status description"""
        if uv_value <= 2:
            return "Low"
        elif uv_value <= 5:
            return "Moderate"
        elif uv_value <= 7:
            return "High"
        elif uv_value <= 10:
            return "Very High"
        else:
            return "Extreme"
