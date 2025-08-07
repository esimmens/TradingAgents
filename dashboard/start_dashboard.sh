#!/bin/bash

# TradingAgents Dashboard Launcher Script
# Starts both backend and frontend servers

set -e

DASHBOARD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$DASHBOARD_DIR/backend"
FRONTEND_DIR="$DASHBOARD_DIR/frontend"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Cleanup function
cleanup() {
    print_info "Stopping servers..."
    if [[ ! -z "$BACKEND_PID" ]]; then
        kill $BACKEND_PID 2>/dev/null || true
        print_status "Backend server stopped"
    fi
    if [[ ! -z "$FRONTEND_PID" ]]; then
        kill $FRONTEND_PID 2>/dev/null || true
        print_status "Frontend server stopped"
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo "🎯 TradingAgents Dashboard Launcher"
echo "=================================================="

# Check Python version
print_info "Checking Python version..."
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    print_error "Python 3.10+ is required"
    exit 1
fi
print_status "Python version OK"

# Check Node.js
print_info "Checking Node.js..."
if ! command -v node &> /dev/null; then
    print_error "Node.js not found. Please install Node.js 16+"
    exit 1
fi
print_status "Node.js OK"

# Check npm
print_info "Checking npm..."
if ! command -v npm &> /dev/null; then
    print_error "npm not found. Please install npm"
    exit 1
fi
print_status "npm OK"

# Install frontend dependencies
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    print_info "Installing frontend dependencies..."
    cd "$FRONTEND_DIR"
    npm install
    print_status "Frontend dependencies installed"
else
    print_status "Frontend dependencies already installed"
fi

# Start backend server
print_info "Starting backend server..."
cd "$BACKEND_DIR"
python3 main.py &
BACKEND_PID=$!
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    print_error "Backend server failed to start"
    exit 1
fi
print_status "Backend server started on http://localhost:8000"

# Start frontend server
print_info "Starting frontend server..."
cd "$FRONTEND_DIR"
BROWSER=none npm start &
FRONTEND_PID=$!
sleep 5

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    print_error "Frontend server failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi
print_status "Frontend server started on http://localhost:3000"

echo ""
echo "=================================================="
echo "🎉 Dashboard is ready!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo "=================================================="

# Wait for processes
wait