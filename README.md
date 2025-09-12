# TRMNL Weather Plugin

A Python microservice that fetches weather data from [WeatherAPI.com](http://weatherapi.com) and sends it to TRMNL webhooks.

## Features

- 🌤️ **Current Weather**: Get real-time weather data for any location
- 📅 **Weather Forecast**: Get up to 14-day weather forecasts
- 🌍 **Global Coverage**: Weather data for millions of locations worldwide
- 🔗 **TRMNL Integration**: Automatic webhook delivery to TRMNL
- 📚 **Literary Quotes**: AI-generated quotes from classic literature matching weather conditions
- ⏰ **Smart Caching**: Quotes refresh every 30 minutes automatically
- 🚀 **FastAPI**: Modern, fast web framework with automatic API documentation
- 🐳 **Docker Ready**: Containerized deployment with Docker Compose
- 📊 **Air Quality**: Optional air quality data inclusion
- 🔄 **Background Processing**: Non-blocking webhook delivery

## API Endpoints

### Health Check
- `GET /` - Basic API information
- `GET /health` - Health check endpoint

### Weather Data
- `POST /weather/current` - Get current weather data
- `POST /weather/forecast` - Get weather forecast (1-14 days)
- `POST /weather/send-to-trmnl` - Get weather data and send to TRMNL webhook
- `POST /weather/trmnl-view` - Get simplified weather data for TRMNL views
- `POST /weather/quote` - Get weather-matching literary quote
- `GET /quotes/cache-stats` - Get quote cache statistics

## Quick Start

### 1. Prerequisites

- Python 3.11+
- [WeatherAPI.com](http://weatherapi.com) API key
- [Google Gemini API](https://ai.google.dev/) key (for literary quotes)
- TRMNL webhook URL

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd trmnl-weather

# Install dependencies
pip install -r requirements.txt

# Set up secrets file
cp .secrets.example .secrets
# Edit .secrets with your API keys
```

### 3. Testing

```bash
# Run comprehensive tests
python3 tests/test_local.py

# Test specific functionality
python3 tests/test_api.py
python3 tests/test_docker.py
```

### 4. Configuration

Create a `.secrets` file with your API keys (this file is ignored by Git for security):

```bash
# Copy the template
cp .secrets.example .secrets

# Edit with your actual API keys
nano .secrets
```

Your `.secrets` file should contain:

```env
WEATHER_API_KEY=your_actual_weatherapi_key
GEMINI_API_KEY=your_actual_gemini_key
TRMNL_WEBHOOK_URL=https://usetrmnl.com/api/custom_plugins/dfd4f07e-ea4f-4ae5-b45a-3fa97894abf1
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

**Security Note**: The `.secrets` file is automatically ignored by Git to prevent accidental commits of sensitive data.

### 4. Running the Service

#### Option 1: Quick Start (Recommended)
```bash
# Make scripts executable
chmod +x start.sh start-ubuntu.sh start-docker.sh

# For most systems
./start.sh

# For Ubuntu/Debian with externally managed Python
./start-ubuntu.sh

# For Docker (most reliable)
./start-docker.sh
```

#### Option 2: Manual Setup
```bash
# Development
python3 main.py

# Production with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Option 3: Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t trmnl-weather .
docker run -p 8000:8000 --env-file .secrets trmnl-weather
```

### Ubuntu/Debian Specific Notes

If you encounter "externally managed environment" errors on Ubuntu:

#### Quick Fix (Recommended)
```bash
# Run as root
sudo ./setup-ubuntu.sh
```

#### Manual Fix
```bash
# Install dependencies with --break-system-packages
sudo apt install python3-pip python3-venv python3-full
pip3 install --break-system-packages -r requirements.txt
python3 main.py
```

#### Alternative Options
1. **Use the Ubuntu script**: `./start-ubuntu.sh`
2. **Use Docker**: `./start-docker.sh` (most reliable)
3. **Use systemd service**: `sudo ./setup-ubuntu.sh` (production ready)

## API Usage

### Get Current Weather

```bash
curl -X POST "http://localhost:8000/weather/current" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "London",
    "include_air_quality": true
  }'
```

### Get Weather Forecast

```bash
curl -X POST "http://localhost:8000/weather/forecast" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "New York",
    "days": 3,
    "include_air_quality": false
  }'
```

### Send to TRMNL Webhook

```bash
curl -X POST "http://localhost:8000/weather/send-to-trmnl" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Tokyo",
    "days": 1,
    "include_air_quality": true
  }'
```

### Get TRMNL View Data

```bash
curl -X POST "http://localhost:8000/weather/trmnl-view" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Tokyo",
    "days": 1,
    "include_air_quality": true
  }'
```

### Get Weather Quote

```bash
curl -X POST "http://localhost:8000/weather/quote" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "London",
    "days": 1,
    "include_air_quality": true
  }'
```

### Get Quote Cache Stats

```bash
curl -X GET "http://localhost:8000/quotes/cache-stats"
```

## Request/Response Format

### Request Body
```json
{
  "location": "string (required) - City name, coordinates, or IP address",
  "days": "integer (optional) - Number of forecast days (1-14, default: 1)",
  "include_air_quality": "boolean (optional) - Include air quality data (default: false)"
}
```

### TRMNL View Response Format
The `/weather/trmnl-view` endpoint returns simplified data perfect for TRMNL views:

```json
{
  "success": true,
  "data": {
    "location_name": "London",
    "location_region": "City of London, Greater London",
    "timezone": "Europe/London",
    "temp_c": 11,
    "feels_like_c": 9.5,
    "condition_text": "Partly cloudy",
    "wind_kph": 6.1,
    "wind_dir": "SW",
    "windchill_c": 7.4,
    "tomorrow_max_c": 13.2,
    "tomorrow_min_c": 9.2,
    "uv_index": 1,
    "aqi_us": 1,
    "formatted_time": "08:30 AM"
  }
}
```

### Response Format
```json
{
  "success": true,
  "data": {
    "location": {
      "name": "London",
      "region": "City of London, Greater London",
      "country": "United Kingdom",
      "lat": 51.52,
      "lon": -0.11,
      "tz_id": "Europe/London",
      "localtime_epoch": 1613896955,
      "localtime": "2021-02-21 8:42"
    },
    "current": {
      "last_updated_epoch": 1613896210,
      "last_updated": "2021-02-21 08:30",
      "temp_c": 11,
      "temp_f": 51.8,
      "is_day": 1,
      "condition": {
        "text": "Partly cloudy",
        "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
        "code": 1003
      },
      "wind_mph": 3.8,
      "wind_kph": 6.1,
      "wind_degree": 220,
      "wind_dir": "SW",
      "pressure_mb": 1009,
      "pressure_in": 30.3,
      "precip_mm": 0.1,
      "precip_in": 0,
      "humidity": 82,
      "cloud": 75,
      "feelslike_c": 9.5,
      "feelslike_f": 49.2,
      "vis_km": 10,
      "vis_miles": 6,
      "uv": 1,
      "gust_mph": 10.5,
      "gust_kph": 16.9,
      "air_quality": {
        "co": 230.3,
        "no2": 13.5,
        "o3": 54.3,
        "so2": 7.9,
        "pm2_5": 8.6,
        "pm10": 11.3,
        "us-epa-index": 1,
        "gb-defra-index": 1
      }
    }
  }
}
```

## API Documentation

Once the service is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Error Handling

The service includes comprehensive error handling:

- **400 Bad Request**: Invalid request parameters
- **401 Unauthorized**: Invalid API key
- **404 Not Found**: Location not found
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Server-side errors

## Logging

The service logs all requests, errors, and webhook deliveries. Logs include:
- Request details and parameters
- API response status codes
- Webhook delivery status
- Error messages and stack traces

## Development

### Project Structure

```
trmnl-weather/
├── main.py              # FastAPI application
├── config.py            # Configuration management
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── env.example         # Environment variables template
└── README.md           # This file
```

### Adding New Features

1. **New Weather Endpoints**: Add new methods to `WeatherAPIService`
2. **Data Processing**: Add data transformation in the service methods
3. **Webhook Integration**: Extend `TRMNLWebhookService` for new payload formats
4. **Configuration**: Add new settings to `config.py`

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the [WeatherAPI.com documentation](http://weatherapi.com)
2. Review the API logs for error details
3. Verify your API keys and webhook URLs
4. Check the service health endpoint

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request
