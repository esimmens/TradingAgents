from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import uuid
from datetime import datetime, timedelta
import random
import time
from contextlib import asynccontextmanager

# Mock data for demonstration
class MockTradingSystem:
    def __init__(self):
        self.agents = [
            {
                "id": "1",
                "name": "Fundamental Analyst",
                "type": "analyst",
                "status": "active",
                "currentTask": "Analyzing NVDA financial statements",
                "performance": {"accuracy": 85, "tradesExecuted": 12, "profitLoss": 2500},
                "lastActivity": datetime.now(),
            },
            {
                "id": "2",
                "name": "Technical Analyst",
                "type": "analyst",
                "status": "idle",
                "currentTask": None,
                "performance": {"accuracy": 78, "tradesExecuted": 15, "profitLoss": 1800},
                "lastActivity": datetime.now() - timedelta(minutes=5),
            },
            {
                "id": "3",
                "name": "Sentiment Analyst",
                "type": "analyst",
                "status": "active",
                "currentTask": "Processing social media sentiment for AAPL",
                "performance": {"accuracy": 82, "tradesExecuted": 8, "profitLoss": 1200},
                "lastActivity": datetime.now(),
            },
            {
                "id": "4",
                "name": "Bullish Researcher",
                "type": "researcher",
                "status": "active",
                "currentTask": "Evaluating bullish case for TSLA",
                "performance": {"accuracy": 75, "tradesExecuted": 10, "profitLoss": 2100},
                "lastActivity": datetime.now(),
            },
            {
                "id": "5",
                "name": "Bearish Researcher",
                "type": "researcher",
                "status": "idle",
                "currentTask": None,
                "performance": {"accuracy": 80, "tradesExecuted": 6, "profitLoss": -800},
                "lastActivity": datetime.now() - timedelta(minutes=10),
            },
            {
                "id": "6",
                "name": "Trader Agent",
                "type": "trader",
                "status": "active",
                "currentTask": "Executing buy order for MSFT",
                "performance": {"accuracy": 88, "tradesExecuted": 25, "profitLoss": 4200},
                "lastActivity": datetime.now(),
            },
            {
                "id": "7",
                "name": "Risk Manager",
                "type": "risk_manager",
                "status": "active",
                "currentTask": "Monitoring portfolio risk metrics",
                "performance": {"accuracy": 90, "tradesExecuted": 20, "profitLoss": 1500},
                "lastActivity": datetime.now(),
            },
            {
                "id": "8",
                "name": "Portfolio Manager",
                "type": "portfolio_manager",
                "status": "active",
                "currentTask": "Rebalancing portfolio allocations",
                "performance": {"accuracy": 92, "tradesExecuted": 30, "profitLoss": 6800},
                "lastActivity": datetime.now(),
            },
        ]
        
        self.trades = []
        self.portfolio = {
            "totalValue": 105800,
            "cash": 25000,
            "positions": [
                {"symbol": "NVDA", "quantity": 50, "avgPrice": 450, "currentPrice": 485.50, "profitLoss": 1775},
                {"symbol": "AAPL", "quantity": 100, "avgPrice": 170, "currentPrice": 175.20, "profitLoss": 520},
                {"symbol": "MSFT", "quantity": 75, "avgPrice": 315, "currentPrice": 320.45, "profitLoss": 408.75},
            ],
            "dailyPnL": 1250,
            "totalPnL": 5800,
        }
        
        self.marketData = [
            {"symbol": "NVDA", "price": 485.50, "change": 12.30, "changePercent": 2.6, "volume": 45000000, "timestamp": datetime.now()},
            {"symbol": "AAPL", "price": 175.20, "change": -2.10, "changePercent": -1.2, "volume": 38000000, "timestamp": datetime.now()},
            {"symbol": "TSLA", "price": 245.80, "change": 8.50, "changePercent": 3.6, "volume": 52000000, "timestamp": datetime.now()},
            {"symbol": "MSFT", "price": 320.45, "change": 5.20, "changePercent": 1.7, "volume": 28000000, "timestamp": datetime.now()},
            {"symbol": "GOOGL", "price": 142.30, "change": -1.80, "changePercent": -1.3, "volume": 22000000, "timestamp": datetime.now()},
        ]
        
        self.systemStatus = "stopped"
        self.activeSymbols = ["NVDA", "AAPL", "TSLA", "MSFT", "GOOGL"]
        self.connected_clients = []

    def generate_mock_trade(self):
        symbols = ["NVDA", "AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NFLX"]
        trade_types = ["buy", "sell"]
        agents = [agent["name"] for agent in self.agents if agent["type"] == "trader"]
        
        trade = {
            "id": str(uuid.uuid4()),
            "symbol": random.choice(symbols),
            "type": random.choice(trade_types),
            "quantity": random.randint(10, 100),
            "price": round(random.uniform(50, 500), 2),
            "timestamp": datetime.now(),
            "status": "executed",
            "agent": random.choice(agents),
            "reasoning": f"Technical analysis indicates {random.choice(['bullish', 'bearish'])} momentum for {random.choice(symbols)}",
        }
        
        self.trades.append(trade)
        return trade

    def update_market_data(self):
        for data in self.marketData:
            # Simulate price changes
            change = random.uniform(-5, 5)
            data["price"] = round(data["price"] + change, 2)
            data["change"] = round(change, 2)
            data["changePercent"] = round((change / (data["price"] - change)) * 100, 1)
            data["timestamp"] = datetime.now()

    def update_portfolio(self):
        # Simulate portfolio value changes
        change = random.uniform(-500, 1000)
        self.portfolio["totalValue"] = round(self.portfolio["totalValue"] + change, 2)
        self.portfolio["dailyPnL"] = round(change, 2)
        self.portfolio["totalPnL"] = round(self.portfolio["totalPnL"] + change, 2)

    def update_agents(self):
        for agent in self.agents:
            if agent["status"] == "active":
                # Simulate agent activity
                if random.random() < 0.3:  # 30% chance to complete task
                    agent["status"] = "idle"
                    agent["currentTask"] = None
                else:
                    # Update performance metrics
                    agent["performance"]["accuracy"] = min(100, agent["performance"]["accuracy"] + random.uniform(-2, 2))
                    agent["lastActivity"] = datetime.now()

trading_system = MockTradingSystem()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting TradingAgents Dashboard Server...")
    yield
    # Shutdown
    print("Shutting down TradingAgents Dashboard Server...")

app = FastAPI(title="TradingAgents Dashboard API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Trade(BaseModel):
    id: str
    symbol: str
    type: str
    quantity: int
    price: float
    timestamp: datetime
    status: str
    agent: str
    reasoning: Optional[str] = None

class Agent(BaseModel):
    id: str
    name: str
    type: str
    status: str
    currentTask: Optional[str] = None
    performance: Dict[str, Any]
    lastActivity: datetime

class Portfolio(BaseModel):
    totalValue: float
    cash: float
    positions: List[Dict[str, Any]]
    dailyPnL: float
    totalPnL: float

class MarketData(BaseModel):
    symbol: str
    price: float
    change: float
    changePercent: float
    volume: int
    timestamp: datetime

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        trading_system.connected_clients.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in trading_system.connected_clients:
            trading_system.connected_clients.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove disconnected clients
                self.active_connections.remove(connection)

manager = ConnectionManager()

# REST API endpoints
@app.get("/")
async def root():
    return {"message": "TradingAgents Dashboard API"}

@app.get("/api/agents")
async def get_agents():
    return trading_system.agents

@app.get("/api/trades")
async def get_trades():
    return trading_system.trades

@app.get("/api/portfolio")
async def get_portfolio():
    return trading_system.portfolio

@app.get("/api/market-data")
async def get_market_data():
    return trading_system.marketData

@app.get("/api/system-status")
async def get_system_status():
    return {
        "status": trading_system.systemStatus,
        "activeSymbols": trading_system.activeSymbols,
        "connectedClients": len(trading_system.connected_clients)
    }

@app.post("/api/system/start")
async def start_system():
    trading_system.systemStatus = "running"
    await manager.broadcast(json.dumps({
        "type": "system_status_update",
        "status": "running"
    }))
    return {"status": "started"}

@app.post("/api/system/stop")
async def stop_system():
    trading_system.systemStatus = "stopped"
    await manager.broadcast(json.dumps({
        "type": "system_status_update",
        "status": "stopped"
    }))
    return {"status": "stopped"}

@app.post("/api/system/pause")
async def pause_system():
    trading_system.systemStatus = "paused"
    await manager.broadcast(json.dumps({
        "type": "system_status_update",
        "status": "paused"
    }))
    return {"status": "paused"}

@app.post("/api/symbols/add")
async def add_symbol(symbol: str):
    if symbol not in trading_system.activeSymbols:
        trading_system.activeSymbols.append(symbol.upper())
    return {"symbols": trading_system.activeSymbols}

@app.post("/api/symbols/remove")
async def remove_symbol(symbol: str):
    if symbol in trading_system.activeSymbols:
        trading_system.activeSymbols.remove(symbol)
    return {"symbols": trading_system.activeSymbols}

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Send initial data
            await websocket.send_text(json.dumps({
                "type": "initial_data",
                "agents": trading_system.agents,
                "portfolio": trading_system.portfolio,
                "marketData": trading_system.marketData,
                "systemStatus": trading_system.systemStatus
            }))
            
            # Keep connection alive and send periodic updates
            while True:
                await asyncio.sleep(5)  # Update every 5 seconds
                
                if trading_system.systemStatus == "running":
                    # Generate mock trade occasionally
                    if random.random() < 0.1:  # 10% chance
                        trade = trading_system.generate_mock_trade()
                        await websocket.send_text(json.dumps({
                            "type": "trade_executed",
                            "trade": trade
                        }))
                    
                    # Update market data
                    trading_system.update_market_data()
                    await websocket.send_text(json.dumps({
                        "type": "market_data_update",
                        "marketData": trading_system.marketData
                    }))
                    
                    # Update portfolio
                    trading_system.update_portfolio()
                    await websocket.send_text(json.dumps({
                        "type": "portfolio_update",
                        "portfolio": trading_system.portfolio
                    }))
                    
                    # Update agents
                    trading_system.update_agents()
                    for agent in trading_system.agents:
                        if agent["status"] == "active":
                            await websocket.send_text(json.dumps({
                                "type": "agent_update",
                                "agent": agent
                            }))
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)