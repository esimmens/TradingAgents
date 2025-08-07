# TradingAgents Dashboard

A comprehensive web-based dashboard for monitoring and controlling the TradingAgents multiagent autonomous stock trading system.

## Features

### 🎯 **Real-time Monitoring**
- Live portfolio tracking with P&L updates
- Real-time market data visualization
- Agent status and performance monitoring
- Trade execution tracking

### 🤖 **Agent Management**
- View all trading agents (Analysts, Researchers, Traders, Risk Managers)
- Monitor agent performance metrics
- Configure agent parameters
- Real-time agent status updates

### 📊 **Trading Interface**
- Market overview with live price feeds
- Portfolio positions tracking
- Pending and executed trades management
- Price charts and technical analysis

### 📈 **Analytics & Performance**
- Portfolio performance vs benchmark
- Risk metrics (Sharpe ratio, drawdown, volatility)
- Sector allocation visualization
- Trading activity analysis
- Top performing positions

### ⚙️ **System Configuration**
- API key management (OpenAI, Finnhub)
- Trading parameters configuration
- Risk management settings
- Agent configuration
- Notification settings

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │ TradingAgents   │
│   (Dashboard)   │◄──►│   (WebSocket)   │◄──►│   (Trading      │
│                 │    │                 │    │    System)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- TradingAgents system (optional for full integration)

### 1. Install Dependencies

#### Frontend (Dashboard)
```bash
cd dashboard
npm install
```

#### Backend (Server)
```bash
cd server
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
cd server
python app.py
```
The server will start on `http://localhost:8000`

### 3. Start the Dashboard
```bash
cd dashboard
npm start
```
The dashboard will open on `http://localhost:3000`

## Dashboard Pages

### 📊 **Dashboard (Home)**
- Portfolio overview with key metrics
- Real-time charts and performance indicators
- Agent status overview
- Recent trading activity

### 🤖 **Agents**
- Detailed agent management interface
- Performance metrics for each agent
- Agent configuration and settings
- Real-time agent status monitoring

### 📈 **Trading**
- Live market data display
- Portfolio positions tracking
- Order management (pending/executed)
- Price charts and technical analysis

### 📊 **Analytics**
- Comprehensive performance analysis
- Risk metrics and portfolio statistics
- Sector allocation visualization
- Trading activity breakdown

### ⚙️ **Settings**
- System configuration
- API key management
- Trading parameters
- Risk management settings
- Notification preferences

## Real-time Features

### WebSocket Integration
- Live portfolio updates
- Real-time trade notifications
- Agent status changes
- Market data streaming

### System Control
- Start/Stop/Pause trading system
- Add/remove watchlist symbols
- Real-time system status monitoring

## Configuration

### API Keys
Configure your API keys in the Settings page:
- **OpenAI API Key**: For agent LLM interactions
- **Finnhub API Key**: For market data

### Trading Parameters
- Max position size
- Risk per trade
- Stop loss and take profit levels
- Daily loss limits

### Agent Configuration
- Max concurrent agents
- Agent timeout settings
- Debug and logging options

## Development

### Frontend Structure
```
dashboard/
├── src/
│   ├── components/     # Reusable UI components
│   ├── contexts/       # React context providers
│   ├── pages/          # Main dashboard pages
│   └── App.tsx         # Main application
```

### Backend Structure
```
server/
├── app.py              # FastAPI application
├── requirements.txt    # Python dependencies
└── README.md          # Backend documentation
```

### Key Technologies

#### Frontend
- **React 18** with TypeScript
- **Material-UI** for UI components
- **Recharts** for data visualization
- **Socket.io** for real-time communication
- **React Query** for data fetching
- **Zustand** for state management

#### Backend
- **FastAPI** for REST API
- **WebSockets** for real-time communication
- **Pydantic** for data validation
- **Uvicorn** for ASGI server

## Integration with TradingAgents

The dashboard is designed to integrate with the TradingAgents system:

1. **Agent Monitoring**: Real-time status of all trading agents
2. **Trade Tracking**: Monitor executed trades and their reasoning
3. **Portfolio Management**: Track positions and performance
4. **System Control**: Start/stop the trading system

## Customization

### Adding New Agents
1. Update the agent types in `TradingContext.tsx`
2. Add agent icons and configurations
3. Update the backend mock data

### Custom Metrics
1. Add new metrics to the analytics page
2. Create custom charts and visualizations
3. Update the data models as needed

### Styling
The dashboard uses Material-UI theming. Customize the theme in `src/index.tsx`:

```typescript
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#00d4aa' },
    secondary: { main: '#ff6b35' },
    // ... custom colors
  },
});
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Ensure the backend server is running on port 8000
   - Check CORS settings in the backend

2. **API Key Errors**
   - Verify API keys in the Settings page
   - Check network connectivity

3. **Real-time Updates Not Working**
   - Check WebSocket connection status
   - Verify backend is sending updates

### Debug Mode
Enable debug mode in the Settings page to see detailed logs and agent activity.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This dashboard is part of the TradingAgents project and follows the same license terms.

## Support

For issues and questions:
- Check the TradingAgents documentation
- Open an issue on GitHub
- Join the Discord community

---

**Note**: This dashboard is designed for research and educational purposes. Trading performance may vary based on many factors. It is not intended as financial, investment, or trading advice.