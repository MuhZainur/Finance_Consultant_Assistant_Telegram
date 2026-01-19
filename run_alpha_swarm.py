import asyncio
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.stocks.manager import StockManager
from agents.crypto.manager import CryptoManager
from agents.commodities.manager import CommodityManager

async def run_swarm():
    print("=" * 60)
    print("🚀 INITIALIZING ALPHA SWARM PROTOCOL (TRI-SQUAD)")
    print("=" * 60)
    
    # ------------------------------------------------------------------
    # PHASE 1: Wall Street Squad (Top 5 US Stocks)
    # ------------------------------------------------------------------
    try:
        print("\n🦅 [PHASE 1] Wall Street Squad Initializing...")
        stock_mgr = StockManager()
        await stock_mgr.run_daily_cycle()
        print("✅ Wall Street Squad Complete.")
    except Exception as e:
        print(f"❌ Phase 1 Error: {e}")
        
    # ANTI-SPAM DELAY (20s)
    print("\n⏳ Cooldown: Waiting 20 seconds (Anti-Spam)...")
    await asyncio.sleep(20)
    
    # ------------------------------------------------------------------
    # PHASE 2: Crypto Squad (BTC + ETH + 3 Dynamic)
    # ------------------------------------------------------------------
    try:
        print("\n🪙 [PHASE 2] Crypto Squad Initializing...")
        crypto_mgr = CryptoManager()
        await crypto_mgr.run_daily_cycle()
        print("✅ Crypto Squad Complete.")
    except Exception as e:
        print(f"❌ Phase 2 Error: {e}")
        
    # ANTI-SPAM DELAY (20s)
    print("\n⏳ Cooldown: Waiting 20 seconds (Anti-Spam)...")
    await asyncio.sleep(20)

    # ------------------------------------------------------------------
    # PHASE 3: Commodity Squad (Gold, Silver, Oil)
    # ------------------------------------------------------------------
    try:
        print("\n🛢️ [PHASE 3] Commodity Squad Initializing...")
        comm_mgr = CommodityManager()
        await comm_mgr.run_daily_cycle()
        print("✅ Commodity Squad Complete.")
    except Exception as e:
        print(f"❌ Phase 3 Error: {e}")

    print("\n" + "=" * 60)
    print("🏁 MISSION ACCOMPLISHED. SYSTEM SLEEP.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_swarm())
