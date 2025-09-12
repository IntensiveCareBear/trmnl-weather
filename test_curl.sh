#!/bin/bash

# TRMNL Weather Plugin - Manual Testing with curl
# Make sure the service is running: python3 main.py

echo "🧪 TRMNL Weather Plugin - Manual Testing"
echo "========================================"

BASE_URL="http://localhost:8000"
LOCATION="London"

echo ""
echo "1. 🏥 Health Check"
echo "------------------"
curl -s "$BASE_URL/health" | jq '.'

echo ""
echo "2. 📊 Root Endpoint"
echo "------------------"
curl -s "$BASE_URL/" | jq '.'

echo ""
echo "3. 🌤️  Current Weather"
echo "---------------------"
curl -s -X POST "$BASE_URL/weather/current" \
  -H "Content-Type: application/json" \
  -d "{\"location\": \"$LOCATION\", \"include_air_quality\": true}" | jq '.'

echo ""
echo "4. 📅 Weather Forecast"
echo "---------------------"
curl -s -X POST "$BASE_URL/weather/forecast" \
  -H "Content-Type: application/json" \
  -d "{\"location\": \"$LOCATION\", \"days\": 3, \"include_air_quality\": true}" | jq '.'

echo ""
echo "5. 🎯 TRMNL View (POST)"
echo "----------------------"
curl -s -X POST "$BASE_URL/weather/trmnl-view" \
  -H "Content-Type: application/json" \
  -d "{\"location\": \"$LOCATION\", \"include_air_quality\": true}" | jq '.'

echo ""
echo "6. 🎯 TRMNL View (GET - Default Location)"
echo "----------------------------------------"
curl -s "$BASE_URL/weather/trmnl-view" | jq '.'

echo ""
echo "7. 📖 Weather Quote"
echo "------------------"
curl -s -X POST "$BASE_URL/weather/quote" \
  -H "Content-Type: application/json" \
  -d "{\"location\": \"$LOCATION\", \"include_air_quality\": true}" | jq '.'

echo ""
echo "8. 📊 Quote Cache Stats"
echo "----------------------"
curl -s "$BASE_URL/quotes/cache-stats" | jq '.'

echo ""
echo "9. 🌍 Test Different Locations"
echo "-----------------------------"
for city in "New York" "Tokyo" "Paris" "Sydney"; do
  echo "Testing $city..."
  curl -s -X POST "$BASE_URL/weather/trmnl-view" \
    -H "Content-Type: application/json" \
    -d "{\"location\": \"$city\", \"include_air_quality\": true}" | jq '.data.location_name, .data.temp_c'
  echo ""
done

echo "✅ Testing complete!"
echo ""
echo "🌐 Service URL: $BASE_URL"
echo "📖 API Docs: $BASE_URL/docs"
echo "🛑 Stop service: Ctrl+C (if running python3 main.py)"
