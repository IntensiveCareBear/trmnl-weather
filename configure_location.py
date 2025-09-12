#!/usr/bin/env python3
"""
Script to configure the default weather location
"""

import os
import sys

def configure_location():
    """Configure the default weather location"""
    print("🌍 Weather Location Configuration")
    print("=" * 40)
    
    # Check if .secrets file exists
    if not os.path.exists('.secrets'):
        print("❌ .secrets file not found!")
        print("Please copy .secrets.example to .secrets first:")
        print("cp .secrets.example .secrets")
        return False
    
    # Read current .secrets file
    with open('.secrets', 'r') as f:
        lines = f.readlines()
    
    # Get new location from user
    current_location = "London"  # default
    for line in lines:
        if line.startswith('DEFAULT_LOCATION='):
            current_location = line.split('=')[1].strip()
            break
    
    print(f"Current default location: {current_location}")
    print("\nEnter new location (or press Enter to keep current):")
    new_location = input("Location: ").strip()
    
    if not new_location:
        new_location = current_location
        print(f"Keeping current location: {current_location}")
    else:
        print(f"Setting location to: {new_location}")
    
    # Update .secrets file
    updated_lines = []
    location_updated = False
    
    for line in lines:
        if line.startswith('DEFAULT_LOCATION='):
            updated_lines.append(f'DEFAULT_LOCATION={new_location}\n')
            location_updated = True
        else:
            updated_lines.append(line)
    
    # Add DEFAULT_LOCATION if it doesn't exist
    if not location_updated:
        updated_lines.append(f'DEFAULT_LOCATION={new_location}\n')
    
    # Write updated file
    with open('.secrets', 'w') as f:
        f.writelines(updated_lines)
    
    print(f"\n✅ Location configured successfully!")
    print(f"Default location is now: {new_location}")
    print("\nYou can also set it manually in .secrets file:")
    print(f"DEFAULT_LOCATION={new_location}")
    
    return True

def show_location_options():
    """Show different ways to configure location"""
    print("\n📍 Location Configuration Options:")
    print("=" * 40)
    print("1. Default Location (in .secrets file):")
    print("   DEFAULT_LOCATION=London")
    print("   DEFAULT_LOCATION=New York")
    print("   DEFAULT_LOCATION=Tokyo")
    print("   DEFAULT_LOCATION=Paris")
    print("   DEFAULT_LOCATION=Sydney")
    print()
    print("2. API Request (overrides default):")
    print("   curl -X POST 'http://localhost:8000/weather/trmnl-view' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"location\": \"Tokyo\", \"include_air_quality\": true}'")
    print()
    print("3. GET Request (uses default location):")
    print("   curl http://localhost:8000/weather/trmnl-view")
    print()
    print("4. Environment Variable:")
    print("   export DEFAULT_LOCATION=Tokyo")
    print("   python3 main.py")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_location_options()
    else:
        configure_location()
