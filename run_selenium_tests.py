#!/usr/bin/env python3
"""
Selenium test runner script
"""
import subprocess
import sys
import os
import time


def install_dependencies():
    """Install Selenium test dependencies"""
    print("🔧 Installing Selenium test dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements-selenium.txt"
        ], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    return True


def run_selenium_tests(app_url="http://localhost:8501", headless=True):
    """Run Selenium tests"""
    print(f"🚀 Running Selenium tests against: {app_url}")
    
    # Set environment variables for tests
    env = os.environ.copy()
    env["APP_URL"] = app_url
    env["HEADLESS"] = str(headless).lower()
    
    # Run tests
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/selenium/",
        "-v",
        "--tb=short",
        "--html=reports/selenium_report.html",
        "--self-contained-html",
        "--junitxml=reports/selenium_junit.xml"
    ]
    
    try:
        result = subprocess.run(cmd, env=env, check=True)
        print("✅ All Selenium tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Selenium tests failed: {e}")
        return False


def run_smoke_tests(app_url="http://localhost:8501"):
    """Run smoke tests only"""
    print(f"🔥 Running smoke tests against: {app_url}")
    
    env = os.environ.copy()
    env["APP_URL"] = app_url
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/selenium/test_app_navigation.py::TestAppNavigation::test_login_functionality",
        "tests/selenium/test_app_navigation.py::TestAppNavigation::test_all_service_tabs_present",
        "-v",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, env=env, check=True)
        print("✅ Smoke tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Smoke tests failed: {e}")
        return False


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Selenium tests for Concierge.com")
    parser.add_argument("--url", default="http://localhost:8501", 
                       help="App URL to test against")
    parser.add_argument("--smoke-only", action="store_true",
                       help="Run only smoke tests")
    parser.add_argument("--no-headless", action="store_true",
                       help="Run browser in visible mode")
    parser.add_argument("--install-deps", action="store_true",
                       help="Install dependencies before running tests")
    
    args = parser.parse_args()
    
    print("🧪 Concierge.com Selenium Test Runner")
    print("=" * 50)
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            sys.exit(1)
    
    # Run tests
    if args.smoke_only:
        success = run_smoke_tests(args.url)
    else:
        success = run_selenium_tests(args.url, not args.no_headless)
    
    if success:
        print("\n🎉 Test execution completed successfully!")
        print("📊 Check reports/ directory for detailed results")
        sys.exit(0)
    else:
        print("\n💥 Test execution failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
