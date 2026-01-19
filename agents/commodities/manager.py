import yfinance as yf
import pandas as pd
import asyncio
from .analyst import CommodityTechnicalAnalyst
from .strategist import CommodityStrategist
from agents.notifier_agent import NotifierAgent

class CommodityManager:
    def __init__(self):
        self.analyst = CommodityTechnicalAnalyst()
        self.strategist = CommodityStrategist()
        self.notifier = NotifierAgent()
        
        # Core Commodities Universe
        self.universe = [
            "GC=F", # Gold Futures
            "SI=F", # Silver Futures
            "CL=F"  # Crude Oil WTI
        ]

    def fetch_ohlcv(self, symbol: str) -> pd.DataFrame:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1y")
            if df.empty: return pd.DataFrame()
            
            df = df.reset_index()
            df = df.rename(columns={
                "Date": "timestamp", "Open": "open", "High": "high", 
                "Low": "low", "Close": "close", "Volume": "volume"
            })
            return df
        except:
            return pd.DataFrame()

    async def run_daily_cycle(self):
        print("🛢️ [Commodity Squad] Starting Macro Cycle...")
        
        combined_report = {}
        
        # Analyze ALL 3 Assets (No filtering needed)
        for symbol in self.universe:
            df = self.fetch_ohlcv(symbol)
            if df.empty: 
                print(f"⚠️ Failed to fetch data for {symbol}")
                continue
            
            print(f"\n👉 Analyzing Commodity: {symbol}")
            
            # 1. Technical Analysis
            tech_summary = self.analyst.analyze_ticker(symbol, df)
            
            # 2. Strategy (LLM + Online Search)
            strategy = await self.strategist.generate_strategy(tech_summary)
            
            # Extract news
            news = strategy.get('news', [])
            
            combined_report[symbol] = {
                "technical": tech_summary,
                "strategy": strategy,
                "news": news
            }
            
        # 3. Send Notification
        if combined_report:
            self.notifier.send_telegram_alert_commodity(combined_report)
            
        return combined_report
