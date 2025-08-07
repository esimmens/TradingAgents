#!/usr/bin/env python3
"""
TradingAgents Dashboard Startup Script

This script starts both the backend server and frontend dashboard.
"""

import subprocess
import sys
import os
import time
import signal
import threading
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import fastapi
        import uvicorn
        print("✅ Backend dependencies found")
    except ImportError:
        print("❌ Backend dependencies missing. Run: pip install -r server/requirements.txt")
        return False
    
    # Check Node.js and npm
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm found: {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    return True

def install_frontend_dependencies():
    """Install frontend dependencies if needed."""
    dashboard_path = Path("dashboard")
    node_modules_path = dashboard_path / "node_modules"
    
    if not node_modules_path.exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(['npm', 'install'], cwd=dashboard_path, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            return False
    else:
        print("✅ Frontend dependencies already installed")
    
    return True

def start_backend():
    """Start the backend server."""
    print("🚀 Starting backend server...")
    try:
        subprocess.run([sys.executable, "server/app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend server failed to start: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")

def start_frontend():
    """Start the frontend development server."""
    print("🚀 Starting frontend server...")
    try:
        subprocess.run(['npm', 'start'], cwd="dashboard", check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Frontend server failed to start: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")

def main():
    """Main function to start the dashboard."""
    print("🎯 TradingAgents Dashboard Startup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("dashboard").exists() or not Path("server").exists():
        print("❌ Please run this script from the project root directory")
        print("   (where 'dashboard' and 'server' folders are located)")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Dependencies check failed. Please install required dependencies.")
        sys.exit(1)
    
    # Install frontend dependencies
    if not install_frontend_dependencies():
        print("\n❌ Frontend dependency installation failed.")
        sys.exit(1)
    
    print("\n✅ All dependencies ready!")
    print("\n🌐 Starting TradingAgents Dashboard...")
    print("   Backend:  http://localhost:8000")
    print("   Frontend: http://localhost:3000")
    print("   Press Ctrl+C to stop all servers")
    print("-" * 40)
    
    # Start both servers in separate threads
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    
    try:
        # Start backend first
        backend_thread.start()
        time.sleep(3)  # Give backend time to start
        
        # Start frontend
        frontend_thread.start()
        
        # Keep main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down TradingAgents Dashboard...")
        print("   Thank you for using TradingAgents!")
        sys.exit(0)

if __name__ == "__main__":
    main()