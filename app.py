import asyncio
import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from contextlib import asynccontextmanager
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

# Import Swarm Logic
from agents.stocks.manager import StockManager
from agents.crypto.manager import CryptoManager
from agents.commodities.manager import CommodityManager

# Define Lifecycle (Optional, for startup checks)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Check keys
    if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("TELEGRAM_BOT_TOKEN"):
        print("⚠️ COMPONENT CHECK: Some API Keys are missing!")
    else:
        print("✅ COMPONENT CHECK: Systems Green.")
    yield
    # Shutdown logic if needed

app = FastAPI(
    title="AlphaSwarm API",
    description="AI Agent Swarm for Financial Analysis (Stocks, Crypto, Commodities)",
    version="1.2.0",
    lifespan=lifespan
)

async def run_swarm_task():
    """
    The main logic from run_alpha_swarm.py, adapted for background execution.
    """
    print("🚀 [API TRIGGER] INITIALIZING ALPHA SWARM PROTOCOL...")
    
    try:
        # Phase 1: Stocks
        print("🦅 [PHASE 1] Wall Street Squad...")
        stock_mgr = StockManager()
        await stock_mgr.run_daily_cycle()
        
        await asyncio.sleep(20) # Anti-Spam
        
        # Phase 2: Crypto
        print("🪙 [PHASE 2] Crypto Squad...")
        crypto_mgr = CryptoManager()
        await crypto_mgr.run_daily_cycle()
        
        await asyncio.sleep(20) # Anti-Spam
        
        # Phase 3: Commodities
        print("🛢️ [PHASE 3] Commodity Squad...")
        comm_mgr = CommodityManager()
        await comm_mgr.run_daily_cycle()
        
        print("🏁 [API TRIGGER] MISSION ACCOMPLISHED.")
        
    except Exception as e:
        print(f"❌ [API TRIGGER] CRITICAL ERROR: {str(e)}")

@app.get("/")
def home():
    return {"status": "AlphaSwarm System Online 🦅", "version": "1.2.0"}

@app.get("/health")
def health_check():
    """
    Used by Cloud Run / Docker to check container health.
    """
    return {"health": "ok"}

@app.post("/trigger")
async def trigger_swarm(background_tasks: BackgroundTasks):
    """
    Manually triggers the full analysis cycle in the background.
    Returns immediately so the HTTP request doesn't time out.
    """
    background_tasks.add_task(run_swarm_task)
    return {"message": "AlphaSwarm Protocol Initiated 🚀", "status": "Running in background"}

if __name__ == "__main__":
    import uvicorn
    # Allow running directly via python app.py
    uvicorn.run(app, host="0.0.0.0", port=8080)
