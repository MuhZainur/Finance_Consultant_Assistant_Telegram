import yfinance as yf
import pandas as pd
import asyncio
from .analyst import StockTechnicalAnalyst
from .strategist import StockStrategist
from agents.notifier_agent import NotifierAgent

class StockManager:
    def __init__(self):
        self.analyst = StockTechnicalAnalyst()
        self.strategist = StockStrategist()
        self.notifier = NotifierAgent()
        
        # S&P 500 Top Volume Universe (Blue Chips + High Activity)
        self.universe = [
            "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",
            "META", "TSLA", "BRK-B", "JPM", "V",
            "JNJ", "WMT", "UNH", "MA", "PG",
            "HD", "BAC", "DIS", "NFLX", "AMD"
        ]

    def fetch_ohlcv(self, symbol: str) -> pd.DataFrame:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1y")  # 1 year for MA200 calculation
            if df.empty: return pd.DataFrame()
            
            df = df.reset_index()
            df = df.rename(columns={
                "Date": "timestamp", "Open": "open", "High": "high", 
                "Low": "low", "Close": "close", "Volume": "volume"
            })
            return df
        except:
            return pd.DataFrame()

    async def get_top_candidates(self, limit=5):
        """
        Scans S&P 500 universe and returns top 'limit' stocks based on:
        1. Volume Spike (Today vs Avg)
        2. Trend (Price > MA50)
        3. RSI (Sweet spot: 30-70)
        """
        print(f"🔍 Scanning {len(self.universe)} stocks for Top {limit} Opportunities...")
        candidates = []
        
        for symbol in self.universe:
            df = self.fetch_ohlcv(symbol)
            if df.empty or len(df) < 50: continue
            
            # Quick Tech Check
            # 1. Volume Spike
            avg_vol = df['volume'].iloc[-21:-1].mean()
            curr_vol = df['volume'].iloc[-1]
            vol_spike = (curr_vol / avg_vol) if avg_vol > 0 else 0
            
            # 2. Trend
            close = df['close'].iloc[-1]
            ma50 = df['close'].rolling(50).mean().iloc[-1]
            trend_score = 1 if close > ma50 else 0
            
            # 3. RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # Score Calculation
            score = (vol_spike * 2) + (trend_score * 5)
            if 30 < rsi < 70: score += 2  # Sweet spot
            
            candidates.append({
                "symbol": symbol,
                "score": score,
                "data": df
            })
            
        # Sort by score descending
        sorted_candidates = sorted(candidates, key=lambda x: x['score'], reverse=True)
        top_picks = sorted_candidates[:limit]
        
        print(f"✅ Selected Top {limit}: {[c['symbol'] for c in top_picks]}")
        return top_picks

    async def run_daily_cycle(self):
        print("🦅 [Wall Street Squad] Starting Smart Alert Cycle...")
        
        # 1. Automatic Filtering - Get Top 5 Stocks
        top_candidates = await self.get_top_candidates(limit=5)
        
        combined_report = {}
        
        # 2. Deep Analysis
        for asset in top_candidates:
            symbol = asset['symbol']
            df = asset['data']
            
            if df.empty: continue
            
            print(f"\n👉 Analyzing Candidate: {symbol}")
            
            # Tech Analysis (Deep)
            tech_summary = self.analyst.analyze_ticker(symbol, df)
            
            # Strategy (LLM with Online Search)
            # News is now fetched internally by the Strategist
            strategy = await self.strategist.generate_strategy(tech_summary)
            
            # Extract retrieved news from strategy for the report
            news = strategy.get('news', [])
            
            combined_report[symbol] = {
                "technical": tech_summary,
                "strategy": strategy,
                "news": news
            }
            
        # 3. Send Notification (Separate from Crypto)
        if combined_report:
            self.notifier.send_telegram_alert_stock(combined_report)
            
        return combined_report
