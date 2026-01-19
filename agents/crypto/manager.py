import yfinance as yf
import pandas as pd
import asyncio
from .analyst import CryptoTechnicalAnalyst
from .strategist import CryptoStrategist
from agents.notifier_agent import NotifierAgent

class CryptoManager:
    def __init__(self):
        self.analyst = CryptoTechnicalAnalyst()
        self.strategist = CryptoStrategist()
        self.notifier = NotifierAgent()
        
        # Expanded Universe (Top Volume/Cap Coins)
        self.universe = [
            "BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "BNB-USD",
            "DOGE-USD", "ADA-USD", "AVAX-USD", "TRX-USD", "LINK-USD",
            "DOT-USD", "MATIC-USD", "LTC-USD", "SHIB-USD", "UNI7083-USD"
        ]

    def fetch_ohlcv(self, symbol: str) -> pd.DataFrame:
        try:
            # print(f"📉 Fetching {symbol}...")
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="1y") # 1y to effectively calculate MA200
            if df.empty: return pd.DataFrame()
            
            df = df.reset_index()
            df = df.rename(columns={
                "Date": "timestamp", "Open": "open", "High": "high", 
                "Low": "low", "Close": "close", "Volume": "volume"
            })
            return df
        except:
            return pd.DataFrame()

    async def get_top_candidates(self, limit=3):
        """
        Scans the universe and returns top 'limit' assets based on:
        1. Volume Spike (Today vs Avg)
        2. Trend (Price > MA50)
        3. Volatility (BB Width)
        """
        print(f"🔍 Scanning {len(self.universe)} assets for Top {limit} Opportunities...")
        candidates = []
        
        for symbol in self.universe:
            df = self.fetch_ohlcv(symbol)
            if df.empty or len(df) < 50: continue
            
            # Quick Tech Check (Lightweight)
            # 1. Volume Spike
            avg_vol = df['volume'].iloc[-21:-1].mean()
            curr_vol = df['volume'].iloc[-1]
            vol_spike = (curr_vol / avg_vol) if avg_vol > 0 else 0
            
            # 2. Trend
            close = df['close'].iloc[-1]
            ma50 = df['close'].rolling(50).mean().iloc[-1]
            trend_score = 1 if close > ma50 else 0
            
            # 3. RSI (Simple calc for filter)
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
            
            # Score Calculation
            # Prioritize: High Volume Spike + Bullish Trend + RSI not overbought (>70)
            score = (vol_spike * 2) + (trend_score * 5)
            if 30 < rsi < 70: score += 2 # Sweet spot
            
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
        print("🪙 [Crypto Squad] Starting Smart Alert Cycle...")
        
        # 1. Automatic Filtering (Get ample candidates to ensure we fill 5 slots)
        # Fetch Top 10 first, then filter down
        top_candidates = await self.get_top_candidates(limit=10)
        
        # 2. Add Core Assets (The "Prophets")
        # Ensure BTC and ETH are always analyzed
        core_assets = ["BTC-USD", "ETH-USD"]
        
        final_list = []
        seen = set()
        
        # Add Core First
        for symbol in core_assets:
            final_list.append({"symbol": symbol, "data": self.fetch_ohlcv(symbol)})
            seen.add(symbol)
            
        # Add Dynamic Assets (fill until we have 5 total)
        for cand in top_candidates:
            if len(final_list) >= 5:
                break
            
            if cand['symbol'] not in seen:
                final_list.append(cand)
                seen.add(cand['symbol'])
        
        combined_report = {}
        
        # 3. Deep Analysis
        for asset in final_list:
            symbol = asset['symbol']
            df = asset['data']
            
            if df.empty: continue
            
            print(f"\n👉 Analyzing Candidate: {symbol}")
            
            # Tech Analysis (Deep)
            tech_summary = self.analyst.analyze_ticker(symbol, df)
            
            # Strategy (LLM with Online Search)
            # News is now fetched internally by the Strategist
            strategy = await self.strategist.generate_strategy(tech_summary)
            
            # Extract news
            news = strategy.get('news', [])
            
            combined_report[symbol] = {
                "technical": tech_summary,
                "strategy": strategy,
                "news": news # Added raw news for Notifier
            }
            
        # 4. Send Notification
        if combined_report:
            self.notifier.send_telegram_alert(combined_report)
            
        return combined_report

if __name__ == "__main__":
    mgr = CryptoManager()
    import json
    print(json.dumps(asyncio.run(mgr.run_daily_cycle()), indent=2))
