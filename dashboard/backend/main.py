from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging
from datetime import datetime
import uvicorn
import sys
import os

# Add the parent directory to the path to import tradingagents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TradingAgents Dashboard", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state management
class DashboardState:
    def __init__(self):
        self.trading_agents: Optional[TradingAgentsGraph] = None
        self.active_sessions: Dict[str, Any] = {}
        self.connected_clients: List[WebSocket] = []
        self.system_status = "stopped"
        self.current_config = DEFAULT_CONFIG.copy()
        self.portfolio_data = {
            "positions": [],
            "total_value": 0.0,
            "cash": 100000.0,
            "pnl": 0.0,
            "daily_pnl": 0.0
        }
        self.agent_states = {
            "fundamental_analyst": {"status": "idle", "last_update": None, "current_task": None},
            "sentiment_analyst": {"status": "idle", "last_update": None, "current_task": None},
            "news_analyst": {"status": "idle", "last_update": None, "current_task": None},
            "technical_analyst": {"status": "idle", "last_update": None, "current_task": None},
            "bull_researcher": {"status": "idle", "last_update": None, "current_task": None},
            "bear_researcher": {"status": "idle", "last_update": None, "current_task": None},
            "trader": {"status": "idle", "last_update": None, "current_task": None},
            "risk_manager": {"status": "idle", "last_update": None, "current_task": None},
            "portfolio_manager": {"status": "idle", "last_update": None, "current_task": None}
        }
        self.trading_history = []
        self.risk_metrics = {
            "var": 0.0,
            "max_drawdown": 0.0,
            "sharpe_ratio": 0.0,
            "volatility": 0.0,
            "beta": 0.0
        }

dashboard_state = DashboardState()

# Pydantic models
class TradingRequest(BaseModel):
    symbol: str
    date: str
    config: Optional[Dict[str, Any]] = None

class ConfigUpdate(BaseModel):
    config: Dict[str, Any]

class SystemCommand(BaseModel):
    command: str  # start, stop, pause, resume
    params: Optional[Dict[str, Any]] = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        dashboard_state.connected_clients = self.active_connections

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        dashboard_state.connected_clients = self.active_connections

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                pass

manager = ConnectionManager()

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        # Send initial state
        await manager.send_personal_message(json.dumps({
            "type": "initial_state",
            "data": {
                "system_status": dashboard_state.system_status,
                "agent_states": dashboard_state.agent_states,
                "portfolio": dashboard_state.portfolio_data,
                "risk_metrics": dashboard_state.risk_metrics
            }
        }), websocket)
        
        while True:
            data = await websocket.receive_text()
            # Handle incoming WebSocket messages if needed
            logger.info(f"Received WebSocket message: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# API Endpoints

@app.get("/")
async def root():
    return {"message": "TradingAgents Dashboard API"}

@app.get("/api/system/status")
async def get_system_status():
    return {
        "status": dashboard_state.system_status,
        "agent_states": dashboard_state.agent_states,
        "active_sessions": len(dashboard_state.active_sessions),
        "connected_clients": len(dashboard_state.connected_clients)
    }

@app.post("/api/system/command")
async def system_command(command: SystemCommand):
    try:
        if command.command == "start":
            if dashboard_state.system_status == "running":
                raise HTTPException(status_code=400, detail="System is already running")
            
            dashboard_state.system_status = "starting"
            await manager.broadcast({
                "type": "system_status",
                "data": {"status": "starting"}
            })
            
            # Initialize trading agents
            config = command.params.get("config", dashboard_state.current_config) if command.params else dashboard_state.current_config
            dashboard_state.trading_agents = TradingAgentsGraph(debug=True, config=config)
            
            dashboard_state.system_status = "running"
            await manager.broadcast({
                "type": "system_status",
                "data": {"status": "running"}
            })
            
        elif command.command == "stop":
            dashboard_state.system_status = "stopping"
            await manager.broadcast({
                "type": "system_status",
                "data": {"status": "stopping"}
            })
            
            dashboard_state.trading_agents = None
            dashboard_state.active_sessions = {}
            
            dashboard_state.system_status = "stopped"
            await manager.broadcast({
                "type": "system_status",
                "data": {"status": "stopped"}
            })
            
        elif command.command == "pause":
            if dashboard_state.system_status != "running":
                raise HTTPException(status_code=400, detail="System is not running")
            dashboard_state.system_status = "paused"
            await manager.broadcast({
                "type": "system_status",
                "data": {"status": "paused"}
            })
            
        elif command.command == "resume":
            if dashboard_state.system_status != "paused":
                raise HTTPException(status_code=400, detail="System is not paused")
            dashboard_state.system_status = "running"
            await manager.broadcast({
                "type": "system_status",
                "data": {"status": "running"}
            })
        
        return {"message": f"Command '{command.command}' executed successfully"}
    
    except Exception as e:
        logger.error(f"Error executing command {command.command}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trading/execute")
async def execute_trading_decision(request: TradingRequest):
    try:
        if dashboard_state.system_status != "running":
            raise HTTPException(status_code=400, detail="System is not running")
        
        if not dashboard_state.trading_agents:
            raise HTTPException(status_code=400, detail="Trading agents not initialized")
        
        # Update agent states to show they're working
        for agent in dashboard_state.agent_states:
            dashboard_state.agent_states[agent]["status"] = "working"
            dashboard_state.agent_states[agent]["last_update"] = datetime.now().isoformat()
        
        await manager.broadcast({
            "type": "agent_states",
            "data": dashboard_state.agent_states
        })
        
        # Execute trading decision
        session_id = f"{request.symbol}_{request.date}_{datetime.now().timestamp()}"
        
        # Run the trading agents in background
        asyncio.create_task(run_trading_session(session_id, request.symbol, request.date))
        
        return {
            "message": "Trading execution started",
            "session_id": session_id,
            "symbol": request.symbol,
            "date": request.date
        }
    
    except Exception as e:
        logger.error(f"Error executing trading decision: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_trading_session(session_id: str, symbol: str, date: str):
    try:
        dashboard_state.active_sessions[session_id] = {
            "symbol": symbol,
            "date": date,
            "status": "running",
            "start_time": datetime.now().isoformat()
        }
        
        # Execute the trading agents
        _, decision = dashboard_state.trading_agents.propagate(symbol, date)
        
        # Update portfolio and trading history
        dashboard_state.trading_history.append({
            "session_id": session_id,
            "symbol": symbol,
            "date": date,
            "decision": decision,
            "timestamp": datetime.now().isoformat()
        })
        
        # Reset agent states
        for agent in dashboard_state.agent_states:
            dashboard_state.agent_states[agent]["status"] = "idle"
            dashboard_state.agent_states[agent]["last_update"] = datetime.now().isoformat()
        
        dashboard_state.active_sessions[session_id]["status"] = "completed"
        dashboard_state.active_sessions[session_id]["decision"] = decision
        
        await manager.broadcast({
            "type": "trading_completed",
            "data": {
                "session_id": session_id,
                "decision": decision,
                "agent_states": dashboard_state.agent_states
            }
        })
        
    except Exception as e:
        logger.error(f"Error in trading session {session_id}: {str(e)}")
        dashboard_state.active_sessions[session_id]["status"] = "error"
        dashboard_state.active_sessions[session_id]["error"] = str(e)
        
        await manager.broadcast({
            "type": "trading_error",
            "data": {
                "session_id": session_id,
                "error": str(e)
            }
        })

@app.get("/api/portfolio")
async def get_portfolio():
    return dashboard_state.portfolio_data

@app.get("/api/agents")
async def get_agent_states():
    return dashboard_state.agent_states

@app.get("/api/trading/history")
async def get_trading_history():
    return dashboard_state.trading_history

@app.get("/api/risk/metrics")
async def get_risk_metrics():
    return dashboard_state.risk_metrics

@app.get("/api/config")
async def get_config():
    return dashboard_state.current_config

@app.post("/api/config")
async def update_config(config_update: ConfigUpdate):
    try:
        dashboard_state.current_config.update(config_update.config)
        
        await manager.broadcast({
            "type": "config_updated",
            "data": dashboard_state.current_config
        })
        
        return {"message": "Configuration updated successfully"}
    
    except Exception as e:
        logger.error(f"Error updating configuration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
async def get_active_sessions():
    return dashboard_state.active_sessions

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)