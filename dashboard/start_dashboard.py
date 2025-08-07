#!/usr/bin/env python3
"""
TradingAgents Dashboard Launcher
Starts both backend and frontend servers
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class DashboardLauncher:
    def __init__(self):
        self.dashboard_dir = Path(__file__).parent
        self.backend_dir = self.dashboard_dir / "backend"
        self.frontend_dir = self.dashboard_dir / "frontend"
        self.backend_process = None
        self.frontend_process = None
        self.running = True

    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        # Check Python version
        if sys.version_info < (3, 10):
            print("❌ Python 3.10+ is required")
            return False
        print("✅ Python version OK")

        # Check if backend dependencies are installed
        try:
            import fastapi
            import uvicorn
            print("✅ Backend dependencies OK")
        except ImportError:
            print("❌ Backend dependencies missing. Run: pip install -r dashboard/backend/requirements.txt")
            return False

        # Check if Node.js is available
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Node.js not found")
                return False
            print("✅ Node.js OK")
        except FileNotFoundError:
            print("❌ Node.js not found. Please install Node.js 16+")
            return False

        # Check if npm is available
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ npm not found")
                return False
            print("✅ npm OK")
        except FileNotFoundError:
            print("❌ npm not found. Please install npm")
            return False

        return True

    def install_frontend_deps(self):
        """Install frontend dependencies if needed"""
        node_modules = self.frontend_dir / "node_modules"
        if not node_modules.exists():
            print("📦 Installing frontend dependencies...")
            try:
                subprocess.run(['npm', 'install'], cwd=self.frontend_dir, check=True)
                print("✅ Frontend dependencies installed")
            except subprocess.CalledProcessError:
                print("❌ Failed to install frontend dependencies")
                return False
        else:
            print("✅ Frontend dependencies already installed")
        return True

    def start_backend(self):
        """Start the FastAPI backend server"""
        print("🚀 Starting backend server...")
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "main.py"],
                cwd=self.backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor backend output in a separate thread
            def monitor_backend():
                while self.running and self.backend_process:
                    line = self.backend_process.stdout.readline()
                    if line:
                        print(f"[Backend] {line.strip()}")
                    elif self.backend_process.poll() is not None:
                        break
            
            threading.Thread(target=monitor_backend, daemon=True).start()
            
            # Wait a moment for backend to start
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ Backend server started on http://localhost:8000")
                return True
            else:
                print("❌ Backend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False

    def start_frontend(self):
        """Start the React frontend server"""
        print("🚀 Starting frontend server...")
        try:
            # Set environment variable to automatically open browser
            env = os.environ.copy()
            env['BROWSER'] = 'none'  # Prevent auto-opening browser
            
            self.frontend_process = subprocess.Popen(
                ['npm', 'start'],
                cwd=self.frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                env=env
            )
            
            # Monitor frontend output in a separate thread
            def monitor_frontend():
                while self.running and self.frontend_process:
                    line = self.frontend_process.stdout.readline()
                    if line:
                        print(f"[Frontend] {line.strip()}")
                        # Check if frontend is ready
                        if "Local:" in line and "localhost:3000" in line:
                            print("✅ Frontend server started on http://localhost:3000")
                    elif self.frontend_process.poll() is not None:
                        break
            
            threading.Thread(target=monitor_frontend, daemon=True).start()
            return True
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False

    def stop_servers(self):
        """Stop both servers"""
        print("\n🛑 Stopping servers...")
        self.running = False
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend server stopped")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("⚠️  Frontend server force killed")
            except Exception as e:
                print(f"❌ Error stopping frontend: {e}")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend server stopped")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("⚠️  Backend server force killed")
            except Exception as e:
                print(f"❌ Error stopping backend: {e}")

    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n📡 Received signal {signum}")
        self.stop_servers()
        sys.exit(0)

    def run(self):
        """Main run method"""
        print("🎯 TradingAgents Dashboard Launcher")
        print("=" * 50)
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed")
            return 1
        
        # Install frontend dependencies
        if not self.install_frontend_deps():
            print("❌ Frontend setup failed")
            return 1
        
        # Start backend
        if not self.start_backend():
            print("❌ Backend startup failed")
            return 1
        
        # Start frontend
        if not self.start_frontend():
            print("❌ Frontend startup failed")
            self.stop_servers()
            return 1
        
        print("\n" + "=" * 50)
        print("🎉 Dashboard is ready!")
        print("📱 Frontend: http://localhost:3000")
        print("🔧 Backend API: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop the dashboard")
        print("=" * 50)
        
        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
                
                # Check if processes are still running
                if self.backend_process and self.backend_process.poll() is not None:
                    print("❌ Backend process died unexpectedly")
                    break
                    
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("❌ Frontend process died unexpectedly")
                    break
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_servers()
        
        return 0

def main():
    launcher = DashboardLauncher()
    return launcher.run()

if __name__ == "__main__":
    sys.exit(main())