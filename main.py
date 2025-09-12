from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
from typing import Optional, Dict, Any
import logging
from datetime import datetime
import asyncio
from config import settings
from data_transformer import WeatherDataTransformer
from gemini_service import GeminiQuoteService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TRMNL Weather Plugin", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class WeatherRequest(BaseModel):
    location: str
    days: Optional[int] = 1
    include_air_quality: Optional[bool] = False

class WeatherData(BaseModel):
    location: Dict[str, Any]
    current: Dict[str, Any]
    forecast: Optional[Dict[str, Any]] = None

class TRMNLResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Weather API service
class WeatherAPIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = settings.WEATHER_API_BASE_URL
    
    async def get_current_weather(self, location: str, include_air_quality: bool = False) -> Dict[str, Any]:
        """Fetch current weather data for a location"""
        url = f"{self.base_url}/current.json"
        params = {
            "key": self.api_key,
            "q": location,
            "aqi": "yes" if include_air_quality else "no"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Weather API error: {e.response.status_code} - {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail="Weather API error")
            except Exception as e:
                logger.error(f"Unexpected error fetching weather: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")
    
    async def get_forecast(self, location: str, days: int = 1, include_air_quality: bool = False) -> Dict[str, Any]:
        """Fetch weather forecast for a location"""
        url = f"{self.base_url}/forecast.json"
        params = {
            "key": self.api_key,
            "q": location,
            "days": min(days, 14),  # API limit is 14 days
            "aqi": "yes" if include_air_quality else "no"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Weather API error: {e.response.status_code} - {e.response.text}")
                raise HTTPException(status_code=e.response.status_code, detail="Weather API error")
            except Exception as e:
                logger.error(f"Unexpected error fetching forecast: {str(e)}")
                raise HTTPException(status_code=500, detail="Internal server error")

# TRMNL webhook service
class TRMNLWebhookService:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    async def send_weather_data(self, weather_data: Dict[str, Any]) -> bool:
        """Send weather data to TRMNL webhook"""
        payload = {
            "merge_variables": weather_data
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30.0
                )
                response.raise_for_status()
                logger.info(f"Successfully sent weather data to TRMNL webhook: {response.status_code}")
                return True
            except httpx.HTTPStatusError as e:
                logger.error(f"TRMNL webhook error: {e.response.status_code} - {e.response.text}")
                return False
            except Exception as e:
                logger.error(f"Unexpected error sending to TRMNL webhook: {str(e)}")
                return False

# Initialize services
weather_service = WeatherAPIService(settings.WEATHER_API_KEY)
trmnl_service = TRMNLWebhookService(settings.TRMNL_WEBHOOK_URL)
gemini_service = GeminiQuoteService(settings.GEMINI_API_KEY)
data_transformer = WeatherDataTransformer(gemini_service)

@app.get("/")
async def root():
    return {"message": "TRMNL Weather Plugin API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/weather/current")
async def get_current_weather(request: WeatherRequest, background_tasks: BackgroundTasks):
    """Get current weather and optionally send to TRMNL webhook"""
    try:
        weather_data = await weather_service.get_current_weather(
            request.location, 
            request.include_air_quality
        )
        
        # Send to TRMNL webhook in background
        background_tasks.add_task(trmnl_service.send_weather_data, weather_data)
        
        return TRMNLResponse(success=True, data=weather_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_current_weather: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/weather/forecast")
async def get_weather_forecast(request: WeatherRequest, background_tasks: BackgroundTasks):
    """Get weather forecast and optionally send to TRMNL webhook"""
    try:
        forecast_data = await weather_service.get_forecast(
            request.location,
            request.days,
            request.include_air_quality
        )
        
        # Send to TRMNL webhook in background
        background_tasks.add_task(trmnl_service.send_weather_data, forecast_data)
        
        return TRMNLResponse(success=True, data=forecast_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_weather_forecast: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/weather/send-to-trmnl")
async def send_weather_to_trmnl(request: WeatherRequest, background_tasks: BackgroundTasks):
    """Get weather data and send directly to TRMNL webhook"""
    try:
        if request.days > 1:
            weather_data = await weather_service.get_forecast(
                request.location,
                request.days,
                request.include_air_quality
            )
        else:
            weather_data = await weather_service.get_current_weather(
                request.location,
                request.include_air_quality
            )
        
        # Send to TRMNL webhook
        success = await trmnl_service.send_weather_data(weather_data)
        
        if success:
            return TRMNLResponse(success=True, data={"message": "Weather data sent to TRMNL successfully"})
        else:
            return TRMNLResponse(success=False, error="Failed to send data to TRMNL webhook")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in send_weather_to_trmnl: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/weather/trmnl-view")
async def get_weather_trmnl_view_default(background_tasks: BackgroundTasks):
    """Get TRMNL view with default location"""
    try:
        # Use default location from config
        location = settings.DEFAULT_LOCATION
        
        # Get current weather data
        weather_data = await weather_service.get_current_weather(
            location, 
            include_air_quality=True
        )
        
        # Transform data for TRMNL view
        transformed_data = await transformer.transform_current_weather(weather_data)
        
        # Send to TRMNL webhook in background
        background_tasks.add_task(trmnl_service.send_weather_data, transformed_data)
        
        return TRMNLResponse(success=True, data=transformed_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_weather_trmnl_view_default: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/weather/trmnl-view")
async def get_weather_trmnl_view(request: WeatherRequest, background_tasks: BackgroundTasks):
    """Get weather data formatted specifically for TRMNL view"""
    try:
        if request.days > 1:
            weather_data = await weather_service.get_forecast(
                request.location,
                request.days,
                request.include_air_quality
            )
            # Transform forecast data for TRMNL view
            trmnl_data = await data_transformer.transform_forecast(weather_data)
        else:
            weather_data = await weather_service.get_current_weather(
                request.location,
                request.include_air_quality
            )
            # Transform current weather data for TRMNL view
            trmnl_data = await data_transformer.transform_current_weather(weather_data)
        
        # Send original data to TRMNL webhook in background
        background_tasks.add_task(trmnl_service.send_weather_data, weather_data)
        
        return TRMNLResponse(success=True, data=trmnl_data)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_weather_trmnl_view: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/weather/quote")
async def get_weather_quote(request: WeatherRequest):
    """Get a weather-matching quote for a location"""
    try:
        # Get current weather data first
        weather_data = await weather_service.get_current_weather(
            request.location,
            request.include_air_quality
        )
        
        # Get quote
        quote = await gemini_service.get_weather_quote(
            request.location,
            {
                'condition_text': weather_data.get('current', {}).get('condition', {}).get('text', ''),
                'temp_c': weather_data.get('current', {}).get('temp_c', 0),
                'wind_kph': weather_data.get('current', {}).get('wind_kph', 0)
            }
        )
        
        if quote:
            return TRMNLResponse(success=True, data={
                'quote': quote.quote,
                'author': quote.author,
                'work': quote.work,
                'weather_condition': quote.weather_condition,
                'location': quote.location,
                'timestamp': quote.timestamp.isoformat()
            })
        else:
            return TRMNLResponse(success=False, error="Failed to generate weather quote")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_weather_quote: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/quotes/cache-stats")
async def get_quote_cache_stats():
    """Get statistics about the quote cache"""
    try:
        stats = gemini_service.get_cache_stats()
        return TRMNLResponse(success=True, data=stats)
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def refresh_quotes_background():
    """Background task to refresh quotes every 2 hours"""
    while True:
        try:
            await asyncio.sleep(7200)  # 2 hours
            await gemini_service.refresh_quotes()
            logger.info("Quote cache refreshed")
        except Exception as e:
            logger.error(f"Error refreshing quotes: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Start background tasks on startup"""
    asyncio.create_task(refresh_quotes_background())
    logger.info("Background quote refresh task started")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
