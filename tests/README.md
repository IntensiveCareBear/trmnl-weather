# TRMNL Weather Plugin - Tests

This directory contains all test files and debugging utilities for the TRMNL Weather Plugin.

## Test Files

### Core Tests
- `test_api.py` - Complete API endpoint testing suite
- `test_local.py` - Local testing with comprehensive checks
- `test_docker.py` - Docker container testing
- `test_scheduled_updates.py` - Scheduled updates functionality testing

### Feature Tests
- `test_bold_quotes.py` - Weather quote boldening functionality
- `test_gemini_fix.py` - Gemini API parsing and quote generation
- `test_view_fixes.py` - TRMNL view display fixes (emojis, AQI, temperatures)
- `test_location.py` - Location configuration testing
- `test_webhook_format.py` - TRMNL webhook data format testing

### Debug Utilities
- `debug_quote.py` - Quote generation debugging
- `debug_transformer.py` - Data transformation debugging
- `debug_trmnl_view.py` - TRMNL view debugging
- `debug_trmnl_webhook.py` - Webhook delivery debugging
- `check_config.py` - Configuration validation
- `manage_cache.py` - Quote cache management

### Example Scripts
- `example_quotes.py` - Quote generation examples
- `example_trmnl_usage.py` - TRMNL integration examples
- `quick_test.py` - Quick functionality tests

### Manual Testing
- `test_curl.sh` - Manual curl command testing
- `trmnl_device_troubleshooting.md` - TRMNL device troubleshooting guide

## Running Tests

### Run All Tests
```bash
# From the project root
python3 tests/test_local.py
```

### Run Specific Tests
```bash
# Test API endpoints
python3 tests/test_api.py

# Test Docker functionality
python3 tests/test_docker.py

# Test scheduled updates
python3 tests/test_scheduled_updates.py

# Test quote functionality
python3 tests/test_bold_quotes.py
```

### Manual Testing
```bash
# Run curl tests
bash tests/test_curl.sh

# Quick test
python3 tests/quick_test.py
```

## Debugging

If you encounter issues, use the debug utilities:

```bash
# Debug quote generation
python3 tests/debug_quote.py

# Debug data transformation
python3 tests/debug_transformer.py

# Debug TRMNL view
python3 tests/debug_trmnl_view.py

# Debug webhook delivery
python3 tests/debug_trmnl_webhook.py
```

## Test Data

All tests use the default location from your `.secrets` file or can be configured with specific locations as needed.
