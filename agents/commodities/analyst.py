import pandas as pd
import numpy as np

class CommodityTechnicalAnalyst:
    """
    Technical Analysis specifically tuned for Commoidities (Futures).
    Ticker examples: GC=F (Gold), SI=F (Silver), CL=F (Crude Oil).
    """
    
    def analyze_ticker(self, ticker: str, df: pd.DataFrame) -> dict:
        if df.empty: return {}
        
        # 1. Trend Analysis (MA Cross)
        close = df['close']
        ma20 = close.rolling(20).mean()
        ma50 = close.rolling(50).mean()
        ma200 = close.rolling(200).mean()
        
        current_price = close.iloc[-1]
        
        # Determine Trend Status
        if current_price > ma50.iloc[-1] and ma50.iloc[-1] > ma200.iloc[-1]:
            trend_status = "Bullish (Strong)"
        elif current_price < ma50.iloc[-1] and ma50.iloc[-1] < ma200.iloc[-1]:
            trend_status = "Bearish (Strong)"
        elif current_price > ma200.iloc[-1]:
             trend_status = "Bullish (Correction)"
        else:
            trend_status = "Sideways / Choppy"
            
        # MA Cross Signal
        ma_cross = "Neutral"
        if ma20.iloc[-1] > ma50.iloc[-1] and ma20.iloc[-2] <= ma50.iloc[-2]:
            ma_cross = "GOLDEN CROSS (Bullish)"
        elif ma20.iloc[-1] < ma50.iloc[-1] and ma20.iloc[-2] >= ma50.iloc[-2]:
            ma_cross = "DEATH CROSS (Bearish)"
            
        # 2. RSI (Momentum)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        rsi_signal = "Neutral"
        if rsi > 70: rsi_signal = "Overbought (Hati-hati)"
        elif rsi < 30: rsi_signal = "Oversold (Potensi Rebound)"
        
        # 3. MACD
        exp12 = close.ewm(span=12, adjust=False).mean()
        exp26 = close.ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal_line = macd.ewm(span=9, adjust=False).mean()
        
        macd_hist = macd.iloc[-1] - signal_line.iloc[-1]
        macd_signal = "Bullish" if macd_hist > 0 else "Bearish"
        
        # 4. Support & Resistance (Simple Pivot)
        recent_high = df['high'].iloc[-20:].max()
        recent_low = df['low'].iloc[-20:].min()
        
        # 5. Volatility (Annualized) - Commodities can be volatile
        log_ret = np.log(close / close.shift(1))
        volatility = log_ret.std() * np.sqrt(252) * 100
        
        # 6. Volume Spike
        avg_vol = df['volume'].iloc[-21:-1].mean()
        curr_vol = df['volume'].iloc[-1]
        vol_spike = "Normal"
        if avg_vol > 0:
            ratio = curr_vol / avg_vol
            if ratio > 2.0: vol_spike = "EXTREME (Bandar Masuk?)"
            elif ratio > 1.5: vol_spike = "High"
            
        # 7. 52-Week High/Low
        high_52w = df['high'].iloc[-252:].max()
        low_52w = df['low'].iloc[-252:].min()

        return {
            "symbol": ticker,
            "price": current_price,
            "trend_status": trend_status,
            "ma_cross": ma_cross,
            "ma20": round(ma20.iloc[-1], 2),
            "ma50": round(ma50.iloc[-1], 2),
            "ma200": round(ma200.iloc[-1], 2),
            "rsi": round(rsi, 2),
            "rsi_signal": rsi_signal,
            "macd_signal": macd_signal,
            "support": recent_low,
            "resistance": recent_high,
            "volatility_annual": f"{volatility:.1f}%",
            "volume_spike": vol_spike,
            "high_52w": high_52w,
            "low_52w": low_52w
        }
