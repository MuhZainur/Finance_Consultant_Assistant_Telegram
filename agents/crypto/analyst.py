import pandas as pd
import numpy as np
from typing import Dict, Any

class CryptoTechnicalAnalyst:
    """
    Handles Technical Analysis calculations for Crypto Assets.
    Includes advanced metrics: MA Cross, MACD, Bollinger, Support/Resistance.
    """
    
    def calculate_ma(self, series: pd.Series) -> Dict[str, Any]:
        """Moving Averages & Cross Detection"""
        ma20 = series.rolling(window=20).mean()
        ma50 = series.rolling(window=50).mean()
        ma200 = series.rolling(window=200).mean()
        
        curr_ma20 = ma20.iloc[-1]
        curr_ma50 = ma50.iloc[-1]
        curr_ma200 = ma200.iloc[-1]
        
        # Cross Detection (Golden/Death Cross)
        signal = "Neutral"
        if curr_ma50 > curr_ma200 and ma50.iloc[-2] <= ma200.iloc[-2]:
            signal = "GOLDEN CROSS (Bullish)"
        elif curr_ma50 < curr_ma200 and ma50.iloc[-2] >= ma200.iloc[-2]:
            signal = "DEATH CROSS (Bearish)"
            
        trend = "Bullish" if series.iloc[-1] > curr_ma50 else "Bearish"

        return {
            "ma20": float(curr_ma20),
            "ma50": float(curr_ma50),
            "ma200": float(curr_ma200) if not pd.isna(curr_ma200) else 0,
            "trend": trend,
            "signal": signal
        }

    def calculate_macd(self, series: pd.Series) -> Dict[str, Any]:
        """MACD (12, 26, 9)"""
        exp1 = series.ewm(span=12, adjust=False).mean()
        exp2 = series.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal_line
        
        curr_hist = histogram.iloc[-1]
        prev_hist = histogram.iloc[-2]
        
        signal = "Neutral"
        if curr_hist > 0 and prev_hist <= 0:
            signal = "Bullish Crossover"
        elif curr_hist < 0 and prev_hist >= 0:
            signal = "Bearish Crossover"
            
        return {
            "macd": float(macd.iloc[-1]),
            "signal_line": float(signal_line.iloc[-1]),
            "histogram": float(curr_hist),
            "signal": signal
        }

    def calculate_bollinger(self, series: pd.Series, window=20) -> Dict[str, Any]:
        """Bollinger Bands & Squeeze"""
        sma = series.rolling(window=window).mean()
        std = series.rolling(window=window).std()
        upper = sma + (std * 2)
        lower = sma - (std * 2)
        
        curr_price = series.iloc[-1]
        bandwidth = (upper.iloc[-1] - lower.iloc[-1]) / sma.iloc[-1] * 100
        
        position = "Neutral"
        if curr_price >= upper.iloc[-1]: position = "Upper Band (Potential Rejection)"
        elif curr_price <= lower.iloc[-1]: position = "Lower Band (Potential Bounce)"
            
        return {
            "upper": float(upper.iloc[-1]),
            "middle": float(sma.iloc[-1]),
            "lower": float(lower.iloc[-1]),
            "bandwidth": float(bandwidth), # Low bandwidth = Squeeze
            "position": position
        }

    def find_support_resistance(self, series: pd.Series) -> Dict[str, float]:
        """Simple Local Min/Max for Support/Resistance"""
        # Look back 30 days
        recent = series.tail(30)
        resistance = recent.max()
        support = recent.min()
        return {"resistance": float(resistance), "support": float(support)}

    def calculate_rsi(self, series: pd.Series, period: int = 14) -> Dict[str, Any]:
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        current = rsi.iloc[-1]
        
        signal = "Neutral"
        if current > 70: signal = "Overbought (>70)"
        elif current < 30: signal = "Oversold (<30)"
            
        return {"current": float(current), "signal": signal}

    def calculate_drawdown(self, series: pd.Series) -> Dict[str, float]:
        """Calculates Max Drawdown from Peak"""
        running_max = series.cummax()
        drawdown = ((series - running_max) / running_max) * 100
        return {"max_drawdown": float(drawdown.min()), "current_drawdown": float(drawdown.iloc[-1])}

    def calculate_roi(self, series: pd.Series) -> Dict[str, str]:
        """Cumulative Returns"""
        curr = series.iloc[-1]
        
        def pct_change(n):
            if len(series) < n: return "N/A"
            prev = series.iloc[-n]
            return f"{((curr - prev) / prev) * 100:+.2f}%"

        return {
            "7d": pct_change(7),
            "30d": pct_change(30),
            "ytd": pct_change(len(series)) 
        }

    def analyze_ticker(self, ticker: str, ohlcv_df: pd.DataFrame) -> Dict[str, Any]:
        """
        Main entry point. Takes raw OHLCV DataFrame and returns
        TOKEN-EFFICIENT metrics summary for the LLM.
        """
        if ohlcv_df.empty:
            return {"error": "No data"}

        close = ohlcv_df['close']
        volume = ohlcv_df['volume']
        
        # Calculate Indicators
        rsi = self.calculate_rsi(close)
        ma = self.calculate_ma(close)
        macd = self.calculate_macd(close)
        bb = self.calculate_bollinger(close)
        sr = self.find_support_resistance(close)
        dd = self.calculate_drawdown(close)
        roi = self.calculate_roi(close)
        
        # Volume Spike
        avg_vol = volume.rolling(window=20).mean().iloc[-1]
        curr_vol = volume.iloc[-1]
        vol_spike = "Detected" if curr_vol > (avg_vol * 1.5) else "Normal"
        
        # Volatility
        log_ret = np.log(close / close.shift(1))
        volatility = log_ret.std() * np.sqrt(365) * 100

        # Flattened Summary for LLM & Notifier Consumption
        summary = {
            "symbol": ticker, # Ensure 'symbol' key exists
            "ticker": ticker,
            "price": float(close.iloc[-1]),
            
            # Trend
            "trend_status": ma['trend'],
            "ma_cross": ma['signal'],
            "ma20": f"{ma['ma20']:.2f}",
            "ma50": f"{ma['ma50']:.2f}",
            "ma200": f"{ma['ma200']:.2f}",
            
            # Momentum
            "rsi": f"{rsi['current']:.1f}",
            "rsi_signal": rsi['signal'],
            "macd_signal": macd['signal'],
            
            # Volatility
            "bb_width": f"{bb['bandwidth']:.2f}%" if bb['bandwidth'] < 5 else "Normal",
            "volume_spike": f"{float(curr_vol/avg_vol):.1f}x" if avg_vol > 0 else "N/A",
            
            # Levels
            "support": sr['support'],
            "resistance": sr['resistance'],
            
            # Risk
            "max_drawdown": f"{dd['max_drawdown']:.2f}%",
            "volatility_annual": f"{volatility:.1f}%",
            
            # Performance
            "perf_7d": roi['7d'],
            "perf_30d": roi['30d']
        }
        
        return summary
