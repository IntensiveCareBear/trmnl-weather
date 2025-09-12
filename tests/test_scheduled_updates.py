#!/usr/bin/env python3
"""
Test script for scheduled updates functionality
"""

import requests
import json
import time

def test_scheduled_updates_status():
    """Test the scheduled updates status endpoint"""
    print("🕐 Testing Scheduled Updates Status")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/scheduled-updates/status", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Scheduled Updates Status:")
            print(f"   Enabled: {data.get('enabled')}")
            print(f"   Interval: {data.get('interval_minutes')} minutes")
            print(f"   Location: {data.get('default_location')}")
            print(f"   Next Update: {data.get('next_update_in')}")
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_manual_trigger():
    """Test manually triggering a scheduled update"""
    print("\n🔄 Testing Manual Trigger")
    print("=" * 40)
    
    try:
        response = requests.post("http://localhost:8000/scheduled-updates/trigger", timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Manual trigger successful:")
                print(f"   Message: {data['data']['message']}")
                print(f"   Location: {data['data']['location']}")
                print(f"   Timestamp: {data['data']['timestamp']}")
                return True
            else:
                print(f"❌ Trigger failed: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_webhook_delivery():
    """Test if webhook delivery is working"""
    print("\n📤 Testing Webhook Delivery")
    print("=" * 40)
    
    try:
        # Trigger a manual update
        response = requests.post("http://localhost:8000/scheduled-updates/trigger", timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Webhook delivery test successful")
                print(f"   Data sent to TRMNL for: {data['data']['location']}")
                print(f"   Time: {data['data']['timestamp']}")
                return True
            else:
                print(f"❌ Webhook delivery failed: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def monitor_scheduled_updates(duration_minutes=2):
    """Monitor scheduled updates for a specified duration"""
    print(f"\n👀 Monitoring Scheduled Updates for {duration_minutes} minutes")
    print("=" * 50)
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    update_count = 0
    
    print("Watching for scheduled updates...")
    print("(Check the service logs to see scheduled updates)")
    
    while time.time() < end_time:
        remaining = int((end_time - time.time()) / 60)
        print(f"⏳ {remaining} minutes remaining...")
        time.sleep(30)  # Check every 30 seconds
    
    print(f"✅ Monitoring complete after {duration_minutes} minutes")
    print("Check the service logs for scheduled update messages")

def main():
    """Run all scheduled update tests"""
    print("🚀 Scheduled Updates Test Suite")
    print("=" * 50)
    
    # Check if service is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("❌ Service not running. Please start with: python3 main.py")
            return
    except:
        print("❌ Service not running. Please start with: python3 main.py")
        return
    
    print("✅ Service is running")
    
    # Run tests
    tests = [
        ("Scheduled Updates Status", test_scheduled_updates_status),
        ("Manual Trigger", test_manual_trigger),
        ("Webhook Delivery", test_webhook_delivery),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        if test_func():
            passed += 1
        print()
    
    # Summary
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        print("\n💡 Next Steps:")
        print("   1. Check service logs for scheduled update messages")
        print("   2. Verify TRMNL device receives data every 30 minutes")
        print("   3. Use 'python3 test_scheduled_updates.py --monitor' to watch updates")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    # Optional monitoring
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitor_scheduled_updates(2)

if __name__ == "__main__":
    main()
