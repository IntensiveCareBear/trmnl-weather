import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file first
load_dotenv()

# Then load from .secrets file if it exists
if os.path.exists('.secrets'):
    load_dotenv('.secrets')

class Settings:
    """Application settings and configuration"""
    
    # Weather API Configuration
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    WEATHER_API_BASE_URL: str = "http://api.weatherapi.com/v1"
    DEFAULT_LOCATION: str = os.getenv("DEFAULT_LOCATION", "London")
    
    # Gemini API Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    
    # TRMNL Webhook Configuration
    TRMNL_WEBHOOK_URL: str = os.getenv(
        "TRMNL_WEBHOOK_URL", 
        "https://usetrmnl.com/api/custom_plugins/dfd4f07e-ea4f-4ae5-b45a-3fa97894abf1"
    )
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # API Configuration
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    
    # Scheduled Updates Configuration
    UPDATE_INTERVAL_MINUTES: int = int(os.getenv("UPDATE_INTERVAL_MINUTES", "30"))
    ENABLE_SCHEDULED_UPDATES: bool = os.getenv("ENABLE_SCHEDULED_UPDATES", "true").lower() == "true"
    
    def validate(self) -> bool:
        """Validate required configuration"""
        if not self.WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY is required")
        return True

# Global settings instance
settings = Settings()

# Validate settings on import
try:
    settings.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please set WEATHER_API_KEY environment variable")
