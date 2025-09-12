# TRMNL Device Troubleshooting Guide

## ✅ Webhook Status: WORKING
- **Status**: 200 OK ✅
- **Data Delivery**: Successful ✅
- **Issue Location**: TRMNL Device/Plugin Side

## 🔍 TRMNL Device Troubleshooting Steps

### 1. Check TRMNL Plugin Configuration

#### Plugin Settings:
- **Plugin ID**: `dfd4f07e-ea4f-4ae5-b45a-3fa97894abf1`
- **Status**: Should be "Active" or "Enabled"
- **Update Frequency**: Check if it's set to update regularly

#### View Configuration:
- **View File**: Make sure you're using the correct view file
- **View Name**: Check if the view is properly named and selected
- **View Format**: Ensure the view matches the data structure

### 2. Check TRMNL Device Status

#### Device Connection:
- **Internet**: Ensure device has stable internet connection
- **TRMNL Service**: Check if TRMNL service is running on device
- **Last Update**: Check when the device last received data

#### Device Logs:
- Look for any error messages in device logs
- Check for data parsing errors
- Verify webhook data is being received

### 3. Verify Data Structure Match

The webhook is sending this data structure:
```json
{
  "merge_variables": {
    "location_name": "London",
    "temp_c": 12,
    "condition_text": "Partly Cloudy",
    "feels_like_c": 10,
    "wind_kph": 21,
    "wind_dir": "SW",
    "windchill_c": 8,
    "uv_index": 1,
    "aqi_us": 1,
    "formatted_time": "06:30 PM",
    "weather_quote": {
      "quote": "The wind, which had been threatening...",
      "author": "Charlotte Brontë",
      "work": "Jane Eyre",
      "weather_condition": "Partly Cloudy"
    }
  }
}
```

### 4. Common TRMNL Issues

#### Issue 1: View Not Selected
- **Problem**: Plugin is working but no view is selected
- **Fix**: Go to TRMNL settings and select the weather view

#### Issue 2: View Template Mismatch
- **Problem**: View template doesn't match data structure
- **Fix**: Update view template to use correct field names

#### Issue 3: Device Cache
- **Problem**: Device is showing cached/old data
- **Fix**: Restart TRMNL device or clear cache

#### Issue 4: Update Frequency
- **Problem**: Device not updating frequently enough
- **Fix**: Check update frequency settings

### 5. Testing Steps

#### Step 1: Check Plugin Status
```bash
# Check if plugin is active in TRMNL dashboard
# Look for plugin ID: dfd4f07e-ea4f-4ae5-b45a-3fa97894abf1
```

#### Step 2: Verify View Selection
- Go to TRMNL device settings
- Check if weather view is selected
- Verify view template matches data structure

#### Step 3: Test Manual Update
- Try manually triggering a plugin update
- Check if data appears after manual trigger

#### Step 4: Check Device Logs
- Look for any error messages
- Check for data parsing issues
- Verify webhook data reception

### 6. Debug Commands

#### Check Webhook Data:
```bash
# Get the exact data being sent
python3 test_webhook_format.py

# Check webhook payload
cat webhook_payload.json
```

#### Test Different Views:
```bash
# Test with different view templates
# Make sure the view uses the correct field names
```

### 7. TRMNL-Specific Solutions

#### Solution 1: Restart TRMNL Service
- Restart the TRMNL service on your device
- This often resolves caching issues

#### Solution 2: Update Plugin Settings
- Go to TRMNL dashboard
- Find your weather plugin
- Check all settings and update frequency

#### Solution 3: Re-select View
- Go to device settings
- Deselect and re-select the weather view
- This forces a refresh

#### Solution 4: Check View Template
- Ensure view template uses correct field names
- Update template if needed

### 8. Expected Behavior

When working correctly, you should see:
- **Location**: London (or your configured location)
- **Temperature**: Current temperature in Celsius
- **Condition**: Weather condition text
- **Quote**: Literary quote matching weather
- **Other Data**: Wind, UV, AQI, etc.

### 9. Next Steps

1. **Check TRMNL Dashboard**: Verify plugin is active
2. **Check Device Settings**: Ensure view is selected
3. **Check Device Logs**: Look for error messages
4. **Test Manual Update**: Try triggering manually
5. **Contact TRMNL Support**: If issues persist

## 🎯 Summary

The webhook is working perfectly (200 OK), so the issue is on the TRMNL device side. Focus on:
- Plugin configuration
- View selection
- Device status
- Data structure matching
