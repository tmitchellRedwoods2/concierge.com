#!/usr/bin/env python3
"""
Concierge.com - Standalone Runner
Run this file to start the Concierge.com app
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies")
        return False
    return True

def run_app():
    """Run the Streamlit app"""
    try:
        print("🚀 Starting Concierge.com...")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", "--server.port=8501"])
    except KeyboardInterrupt:
        print("\n👋 Concierge.com stopped")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    print("🏆 Welcome to Concierge.com!")
    print("📦 Installing dependencies...")
    
    if install_requirements():
        print("🎯 Starting the app...")
        run_app()
    else:
        print("❌ Failed to install dependencies. Please run: pip install -r requirements.txt")
