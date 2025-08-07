# TradingAgents Dashboard

A modern web-based dashboard for controlling, managing, and observing a multiagent autonomous stock trading system. Built with FastAPI backend and React frontend.

## Features

### 🎛️ System Control
- Start/Stop/Pause/Resume trading system
- Real-time system status monitoring
- WebSocket-based live updates

### 🤖 Agent Monitoring
- Real-time agent status visualization
- Individual agent activity tracking
- Agent pipeline visualization
- Performance metrics per agent

### 💼 Portfolio Management
- Portfolio overview with P&L tracking
- Position management and monitoring
- Performance charts and analytics
- Asset allocation visualization

### 📊 Risk Management
- Real-time risk metrics
- Risk alerts and notifications
- Drawdown monitoring
- Volatility tracking

### 🔧 Configuration
- Agent parameter adjustment
- System configuration management
- Trading strategy settings

## Architecture

```
dashboard/
├── backend/           # FastAPI backend server
│   ├── main.py       # Main FastAPI application
│   └── requirements.txt
├── frontend/         # React frontend application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── App.tsx       # Main application component
│   │   └── index.tsx     # Entry point
│   ├── public/
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd dashboard/backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Make sure the main TradingAgents system is accessible:
```bash
# The backend expects to import from the parent directory
# Ensure you have the TradingAgents system installed or accessible
```

5. Start the backend server:
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd dashboard/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

### Starting the System

1. Start both backend and frontend servers
2. Open your browser to `http://localhost:3000`
3. Click the "Start" button in the System Status card
4. Monitor agent status in the Agents tab

### Executing Trading Analysis

1. Ensure the system is running
2. Go to the Overview tab
3. Click "Execute Trading Analysis"
4. Enter a stock symbol (e.g., NVDA) and date
5. Monitor progress in the Agents tab

### Monitoring Portfolio

1. Navigate to the Portfolio tab
2. View current positions and P&L
3. Analyze performance charts
4. Check asset allocation

## API Endpoints

### System Control
- `POST /api/system/command` - Send system commands (start/stop/pause/resume)
- `GET /api/system/status` - Get current system status

### Trading
- `POST /api/trading/execute` - Execute trading analysis
- `GET /api/trading/history` - Get trading history

### Data
- `GET /api/portfolio` - Get portfolio data
- `GET /api/agents` - Get agent states
- `GET /api/risk/metrics` - Get risk metrics
- `GET /api/config` - Get configuration
- `POST /api/config` - Update configuration

### WebSocket
- `WS /ws` - Real-time updates and notifications

## WebSocket Messages

The dashboard uses WebSocket for real-time communication:

### Incoming Messages
- `initial_state` - Initial system state on connection
- `system_status` - System status changes
- `agent_states` - Agent state updates
- `trading_completed` - Trading analysis completion
- `trading_error` - Trading errors
- `config_updated` - Configuration updates

## Development

### Adding New Components

1. Create component in `frontend/src/components/`
2. Export from component file
3. Import and use in `App.tsx`

### Adding New API Endpoints

1. Add endpoint to `backend/main.py`
2. Update frontend API calls in components
3. Handle WebSocket messages if needed

### Styling

The dashboard uses Material-UI with a dark theme. Customize the theme in `App.tsx`:

```typescript
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    // ... theme configuration
  },
});
```

## Configuration

### Backend Configuration

The backend integrates with the TradingAgents system configuration. Key settings:

- `DEFAULT_CONFIG` - Imported from TradingAgents
- WebSocket connection management
- API rate limiting (if needed)

### Frontend Configuration

- Proxy configuration in `package.json` for development
- WebSocket connection settings in `useWebSocket.ts`
- Theme configuration in `App.tsx`

## Troubleshooting

### Common Issues

1. **Backend not starting**
   - Check Python version (3.10+)
   - Verify TradingAgents system is accessible
   - Check port 8000 is available

2. **Frontend not connecting**
   - Verify backend is running on port 8000
   - Check proxy configuration in package.json
   - Verify WebSocket connection in browser dev tools

3. **Trading execution fails**
   - Ensure system is started
   - Check API keys are configured
   - Verify symbol format (uppercase, valid ticker)

### Debug Mode

Enable debug mode by setting `debug=True` in the TradingAgentsGraph initialization:

```python
dashboard_state.trading_agents = TradingAgentsGraph(debug=True, config=config)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the TradingAgents framework. See the main project license for details.