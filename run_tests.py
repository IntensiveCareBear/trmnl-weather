#!/usr/bin/env python3
"""
Test runner for TRMNL Weather Plugin
"""

import sys
import os
import subprocess

def run_test(test_file):
    """Run a specific test file"""
    test_path = os.path.join('tests', test_file)
    if os.path.exists(test_path):
        print(f"🧪 Running {test_file}...")
        try:
            result = subprocess.run([sys.executable, test_path], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {test_file} passed")
                return True
            else:
                print(f"❌ {test_file} failed")
                print(result.stdout)
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ Error running {test_file}: {e}")
            return False
    else:
        print(f"❌ Test file {test_file} not found")
        return False

def main():
    """Run tests based on command line arguments"""
    if len(sys.argv) > 1:
        # Run specific test
        test_file = sys.argv[1]
        if not test_file.endswith('.py'):
            test_file += '.py'
        success = run_test(test_file)
        sys.exit(0 if success else 1)
    else:
        # Run all tests
        print("🚀 Running TRMNL Weather Plugin Tests")
        print("=" * 50)
        
        # Core tests
        tests = [
            'test_local.py',
            'test_api.py',
            'test_docker.py',
            'test_scheduled_updates.py'
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if run_test(test):
                passed += 1
            print()
        
        print("=" * 50)
        print(f"📊 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed!")
        else:
            print("❌ Some tests failed!")
        
        sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()
