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

# Configure logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
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
        
        logger.info(f"📤 Sending weather data to TRMNL webhook: {self.webhook_url}")
        logger.info(f"📊 Payload keys: {list(payload.keys())}")
        logger.info(f"📊 Weather data keys: {list(weather_data.keys()) if weather_data else 'None'}")
        
        async with httpx.AsyncClient() as client:
            try:
                logger.info(f"🌐 Making HTTP POST request to TRMNL...")
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=30.0
                )
                
                logger.info(f"📡 TRMNL webhook response status: {response.status_code}")
                logger.info(f"📡 Response headers: {dict(response.headers)}")
                
                response.raise_for_status()
                logger.info(f"✅ Successfully sent weather data to TRMNL webhook: {response.status_code}")
                
                # Log response body for debugging
                try:
                    response_json = response.json()
                    logger.info(f"📄 TRMNL response body: {response_json}")
                except Exception as json_e:
                    logger.info(f"📄 TRMNL response body (text): {response.text}")
                
                return True
            except httpx.HTTPStatusError as e:
                logger.error(f"❌ TRMNL webhook HTTP error: {e.response.status_code}")
                logger.error(f"❌ Error response text: {e.response.text}")
                logger.error(f"❌ Request URL: {self.webhook_url}")
                return False
            except Exception as e:
                logger.error(f"❌ Unexpected error sending to TRMNL webhook: {str(e)}")
                logger.error(f"❌ Error type: {type(e).__name__}")
                return False

# Initialize services
weather_service = WeatherAPIService(settings.WEATHER_API_KEY)
trmnl_service = TRMNLWebhookService(settings.TRMNL_WEBHOOK_URL)
gemini_service = GeminiQuoteService(settings.GEMINI_API_KEY)
data_transformer = WeatherDataTransformer(gemini_service)

# Scheduled task for automatic webhook updates
async def scheduled_weather_update():
    """Send weather data to TRMNL webhook at configured intervals"""
    while True:
        try:
            logger.info(f"🔄 Running scheduled weather update (every {settings.UPDATE_INTERVAL_MINUTES} minutes)...")
            logger.info(f"📍 Default location: {settings.DEFAULT_LOCATION}")
            logger.info(f"🔗 TRMNL webhook URL: {settings.TRMNL_WEBHOOK_URL}")
            
            # Get forecast data for default location (includes current + tomorrow's forecast)
            logger.info(f"🌤️ Fetching forecast data for {settings.DEFAULT_LOCATION}...")
            weather_data = await weather_service.get_forecast(
                settings.DEFAULT_LOCATION,
                days=1,
                include_air_quality=True
            )
            logger.info(f"📊 Raw weather data received: {list(weather_data.keys()) if weather_data else 'None'}")
            
            # Transform data for TRMNL view
            logger.info(f"🔄 Transforming weather data for TRMNL view...")
            trmnl_data = await data_transformer.transform_forecast(weather_data)
            logger.info(f"📱 Transformed data keys: {list(trmnl_data.keys()) if trmnl_data else 'None'}")
            
            # Send to TRMNL webhook
            logger.info(f"📤 Sending transformed data to TRMNL webhook...")
            success = await trmnl_service.send_weather_data(trmnl_data)
            
            if success:
                logger.info(f"✅ Scheduled update sent successfully for {settings.DEFAULT_LOCATION}")
            else:
                logger.error("❌ Scheduled update failed to send to TRMNL webhook")
                
        except Exception as e:
            logger.error(f"❌ Error in scheduled weather update: {str(e)}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
        
        # Wait for configured interval (convert minutes to seconds)
        logger.info(f"⏰ Waiting {settings.UPDATE_INTERVAL_MINUTES} minutes until next update...")
        await asyncio.sleep(settings.UPDATE_INTERVAL_MINUTES * 60)


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
        
        # Get forecast data (includes current + tomorrow's forecast)
        weather_data = await weather_service.get_forecast(
            location, 
            days=1,
            include_air_quality=True
        )
        
        # Transform data for TRMNL view
        transformed_data = await data_transformer.transform_forecast(weather_data)
        
        # Send transformed data to TRMNL webhook in background
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
        if request.days >= 1:
            weather_data = await weather_service.get_forecast(
                request.location,
                request.days,
                request.include_air_quality
            )
            # Transform forecast data for TRMNL view (includes current + forecast)
            trmnl_data = await data_transformer.transform_forecast(weather_data)
        else:
            weather_data = await weather_service.get_current_weather(
                request.location,
                request.include_air_quality
            )
            # Transform current weather data for TRMNL view
            trmnl_data = await data_transformer.transform_current_weather(weather_data)
        
        # Send transformed data to TRMNL webhook in background
        background_tasks.add_task(trmnl_service.send_weather_data, trmnl_data)
        
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

@app.get("/scheduled-updates/status")
async def get_scheduled_updates_status():
    """Get status of scheduled updates"""
    return {
        "enabled": settings.ENABLE_SCHEDULED_UPDATES,
        "interval_minutes": settings.UPDATE_INTERVAL_MINUTES,
        "default_location": settings.DEFAULT_LOCATION,
        "next_update_in": f"~{settings.UPDATE_INTERVAL_MINUTES} minutes"
    }

@app.post("/scheduled-updates/trigger")
async def trigger_scheduled_update():
    """Manually trigger a scheduled update"""
    try:
        logger.info("🔄 Manual trigger of scheduled update...")
        
        # Get current weather data for default location
        weather_data = await weather_service.get_current_weather(
            settings.DEFAULT_LOCATION,
            include_air_quality=True
        )
        
        # Transform data for TRMNL view
        trmnl_data = await data_transformer.transform_current_weather(weather_data)
        
        # Send to TRMNL webhook
        success = await trmnl_service.send_weather_data(trmnl_data)
        
        if success:
            logger.info(f"✅ Manual update sent successfully for {settings.DEFAULT_LOCATION}")
            return TRMNLResponse(success=True, data={
                "message": f"Weather data sent to TRMNL for {settings.DEFAULT_LOCATION}",
                "location": settings.DEFAULT_LOCATION,
                "timestamp": datetime.utcnow().isoformat()
            })
        else:
            return TRMNLResponse(success=False, error="Failed to send data to TRMNL webhook")
            
    except Exception as e:
        logger.error(f"Unexpected error in trigger_scheduled_update: {str(e)}")
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
    logger.info("🚀 TRMNL Weather Plugin starting up...")
    logger.info(f"📍 Default location: {settings.DEFAULT_LOCATION}")
    logger.info(f"🔗 TRMNL webhook URL: {settings.TRMNL_WEBHOOK_URL}")
    logger.info(f"⏰ Update interval: {settings.UPDATE_INTERVAL_MINUTES} minutes")
    logger.info(f"🔄 Scheduled updates enabled: {settings.ENABLE_SCHEDULED_UPDATES}")
    
    # Start scheduled weather updates
    if settings.ENABLE_SCHEDULED_UPDATES:
        logger.info(f"🚀 Starting scheduled weather updates every {settings.UPDATE_INTERVAL_MINUTES} minutes...")
        asyncio.create_task(scheduled_weather_update())
    else:
        logger.info("⏸️  Scheduled updates disabled")
    
    # Start quote refresh task
    asyncio.create_task(refresh_quotes_background())
    logger.info("📚 Background quote refresh task started")
    logger.info("✅ TRMNL Weather Plugin startup complete!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
