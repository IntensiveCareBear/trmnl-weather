#!/usr/bin/env python3
"""
Cache management script for weather quotes
"""

import requests
import json

def show_cache_stats():
    """Show current cache statistics"""
    try:
        response = requests.get("http://localhost:8000/quotes/cache-stats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                stats = data['data']
                print("📊 Quote Cache Statistics")
                print("=" * 30)
                print(f"Total cached quotes: {stats['total_cached_quotes']}")
                print(f"Cache keys: {', '.join(stats['cache_keys'])}")
                print(f"Last updates: {json.dumps(stats['last_updates'], indent=2)}")
            else:
                print(f"❌ Error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

def test_quote_caching():
    """Test quote caching behavior"""
    print("\n🧪 Testing Quote Caching")
    print("=" * 30)
    
    locations = ["London", "Paris", "Tokyo", "New York"]
    
    for location in locations:
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
                    print(f"✅ {location}: \"{quote['quote'][:50]}...\" - {quote['author']}")
                else:
                    print(f"❌ {location}: {data.get('error')}")
            else:
                print(f"❌ {location}: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {location}: {e}")

def main():
    """Main function"""
    print("🗂️  Weather Quote Cache Manager")
    print("=" * 40)
    
    show_cache_stats()
    test_quote_caching()
    
    print("\n💡 Tips:")
    print("- Quotes are cached for 2 hours")
    print("- Fallback quotes are used when API fails")
    print("- Stale quotes are reused to avoid API calls")
    print("- Only 3 quotes are refreshed per background cycle")

if __name__ == "__main__":
    main()
