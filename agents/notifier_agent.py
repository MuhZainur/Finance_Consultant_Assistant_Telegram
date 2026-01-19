import os
import requests
import json
from datetime import datetime
import html

class NotifierAgent:
    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_telegram_alert(self, report_data: dict):
        """
        Formats and sends a Telegram alert for the Top Candidates.
        """
        if not self.bot_token or not self.chat_id:
            print("⚠️ Telegram credentials missing. Skipping notification.")
            return

        print("📢 [Notifier] Sending Telegram Alert...")
        
        # 1. Header
        date_str = datetime.now().strftime("%d %b %Y")
        message = f"🔥 <b>ALPHASWARM: INTEL PASAR CRYPTO</b> ({date_str})\n\n"
        
        # 2. Iterate Top Assets
        for ticker, data in report_data.items():
            strat = data.get('strategy', {})
            plan = strat.get('action_plan', {})
            tech = data.get('technical', {})
            
            signal = plan.get('signal', 'WAIT')
            icon = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
            
            # TradingView Link
            clean_ticker = ticker.split('-')[0] + "USDT" 
            tv_link = f"https://www.tradingview.com/chart/?symbol=BINANCE:{clean_ticker}"
            
            # Dynamic Headline (Hook)
            headline = html.escape(strat.get('headline', f"Analisa Harian {ticker}"))
            
            # Asset Block
            message += f"💎 <b>{ticker}</b> {icon} <b>{headline}</b>\n"
            message += f"💵 Harga: ${tech.get('price', 0):,.2f}\n\n"
            
            # 1. Rich Analysis (The "Why")
            raw_analysis = strat.get('analysis_summary', 'Belum ada analisa.')
            if len(raw_analysis) > 280: raw_analysis = raw_analysis[:277] + "..."
            analysis_text = html.escape(raw_analysis)
            message += f"🧠 <b>Analisa Bandar &amp; Teknikal:</b>\n<i>{analysis_text}</i>\n\n"
            
            # 2. Key Metrics (Uniform for ALL assets)
            message += f"🛡️ <b>Data Kunci:</b>\n"
            message += f"• Fase: {strat.get('market_phase', 'Unknown')}\n"
            message += f"• Psikologis: {strat.get('psychology', 'Neutral')}\n"
            message += f"• Support: {tech.get('support', 'N/A')} | Res: {tech.get('resistance', 'N/A')}\n"
            message += f"• RSI: {tech.get('rsi', 'N/A')} | Vol: {tech.get('volume_spike', 'N/A')}\n"
            
            # 3. Trade Setup (Only if Signal is Actionable)
            entry = plan.get('entry_zone')
            if signal in ["BUY", "SELL"] and entry and entry != "N/A":
                 message += f"\n🎯 <b>Rencana Trade ({signal}):</b>\n" 
                 message += f"• Masuk: {entry}\n"
                 message += f"• Target: {plan.get('take_profit')}\n"
                 message += f"• Stop: {plan.get('stop_loss')}"

            # 4. News Section (Hybrid Option A+B)
            news_items = data.get('news', [])
            if news_items:
                message += f"\n📰 <b>Berita Terkini:</b>\n"
                # Limit to 1 news item if analyzing 5 assets
                limit_news = 1 if len(report_data) >= 5 else 2
                for item in news_items[:limit_news]:
                    title = html.escape(item.get('title', 'No Title'))
                    source = html.escape(item.get('source', 'Web'))
                    url = item.get('url', '')
                    if len(title) > 60: title = title[:57] + "..."
                    message += f"• <a href='{url}'>{title}</a> ({source})\n"
            
            message += f"\n🔗 <a href='{tv_link}'>Lihat Chart</a>\n\n"
            
        message += "<i>🤖 Disusun oleh AlphaSwarm AI</i>"

        # 3. Send Request
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        try:
            r = requests.post(f"{self.base_url}/sendMessage", json=payload)
            if r.status_code == 200:
                print("✅ Telegram Sent Successfully!")
            else:
                print(f"❌ Telegram Error: {r.text}")
        except Exception as e:
            print(f"❌ Network Error: {e}")

    def send_telegram_alert_stock(self, report_data: dict):
        """
        Formats and sends Telegram alert for TOP US STOCKS.
        Separate from Crypto to avoid character limit issues.
        """
        if not self.bot_token or not self.chat_id:
            print("⚠️ Telegram credentials missing. Skipping notification.")
            return

        print("📢 [Notifier] Sending Wall Street Alert...")
        
        # 1. Header
        date_str = datetime.now().strftime("%d %b %Y")
        message = f"🦅 <b>ALPHASWARM: INTEL WALL STREET</b> ({date_str})\n\n"
        
        # 2. Iterate Top Stocks
        for ticker, data in report_data.items():
            strat = data.get('strategy', {})
            plan = strat.get('action_plan', {})
            tech = data.get('technical', {})
            
            signal = plan.get('signal', 'WAIT')
            icon = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
            
            # TradingView Link (Stock format)
            tv_link = f"https://www.tradingview.com/chart/?symbol=NASDAQ:{ticker}"
            
            # Dynamic Headline (Hook)
            headline = html.escape(strat.get('headline', f"Analisa Harian {ticker}"))
            
            # Asset Block
            message += f"📊 <b>{ticker}</b> {icon} <b>{headline}</b>\n"
            message += f"💵 Harga: ${tech.get('price', 0):,.2f}\n\n"
            
            # 1. Rich Analysis
            raw_analysis = strat.get('analysis_summary', 'Belum ada analisa.')
            if len(raw_analysis) > 280: raw_analysis = raw_analysis[:277] + "..."
            analysis_text = html.escape(raw_analysis)
            message += f"🧠 <b>Analisa Institusi &amp; Teknikal:</b>\n<i>{analysis_text}</i>\n\n"
            
            # 2. Key Metrics (Uniform)
            message += f"🛡️ <b>Data Kunci:</b>\n"
            message += f"• Fase: {strat.get('market_phase', 'Unknown')}\n"
            message += f"• Psikologis: {strat.get('psychology', 'Neutral')}\n"
            message += f"• Support: ${tech.get('support', 'N/A')} | Res: ${tech.get('resistance', 'N/A')}\n"
            message += f"• RSI: {tech.get('rsi', 'N/A')} | Vol: {tech.get('volume_spike', 'N/A')}\n"
            message += f"• 52W High: ${tech.get('high_52w', 'N/A')} | Low: ${tech.get('low_52w', 'N/A')}\n"
            
            # 3. Trade Setup (Conditional)
            entry = plan.get('entry_zone')
            if signal in ["BUY", "SELL"] and entry and entry != "N/A":
                 message += f"\n🎯 <b>Rencana Trade ({signal}):</b>\n" 
                 message += f"• Masuk: {entry}\n"
                 message += f"• Target: {plan.get('take_profit')}\n"
                 message += f"• Stop: {plan.get('stop_loss')}"

            # 4. News Section
            news_items = data.get('news', [])
            if news_items:
                message += f"\n📰 <b>Berita Terkini:</b>\n"
                # Limit to 1 news item if analyzing 5 stocks to save space
                limit_news = 1 if len(report_data) >= 5 else 2
                for item in news_items[:limit_news]:
                    title = html.escape(item.get('title', 'No Title'))
                    source = html.escape(item.get('source', 'Web'))
                    url = item.get('url', '')
                    if len(title) > 60: title = title[:57] + "..."
                    message += f"• <a href='{url}'>{title}</a> ({source})\n"
            
            message += f"\n🔗 <a href='{tv_link}'>Lihat Chart</a>\n\n"
            
        message += "<i>🤖 Disusun oleh AlphaSwarm AI</i>"

        # 3. Send Request
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        try:
            r = requests.post(f"{self.base_url}/sendMessage", json=payload)
            if r.status_code == 200:
                print("✅ Wall Street Alert Sent Successfully!")
            else:
                print(f"❌ Telegram Error: {r.text}")
        except Exception as e:
            print(f"❌ Network Error: {e}")

    def send_telegram_alert_commodity(self, report_data: dict):
        """
        Formats and sends Telegram alert for COMMODITIES (Gold, Silver, Oil).
        """
        if not self.bot_token or not self.chat_id:
            print("⚠️ Telegram credentials missing. Skipping notification.")
            return

        print("📢 [Notifier] Sending Commodity Alert...")
        
        # 1. Header
        date_str = datetime.now().strftime("%d %b %Y")
        message = f"🛢️ <b>ALPHASWARM: INTEL KOMODITAS & MACRO</b> ({date_str})\n\n"
        
        # 2. Iterate Assets
        for ticker, data in report_data.items():
            strat = data.get('strategy', {})
            plan = strat.get('action_plan', {})
            tech = data.get('technical', {})
            
            signal = plan.get('signal', 'WAIT')
            icon = "🟢" if "BUY" in signal else "🔴" if "SELL" in signal else "🟡"
            
            # Custom Names
            clean_name = ticker
            if "GC=F" in ticker: clean_name = "GOLD (XAU/USD)"
            elif "SI=F" in ticker: clean_name = "SILVER (XAG/USD)"
            elif "CL=F" in ticker: clean_name = "WTI CRUDE OIL"
            
            # TradingView Link (Futures)
            tv_link = "https://www.tradingview.com/symbols/XAUUSD/" if "GC" in ticker else "https://www.tradingview.com/chart"
            
            # Dynamic Headline
            headline = html.escape(strat.get('headline', f"Analisa {clean_name}"))
            
            # Asset Block
            message += f"🌍 <b>{clean_name}</b> {icon} <b>{headline}</b>\n"
            message += f"💵 Harga: ${tech.get('price', 0):,.2f}\n\n"
            
            # 1. Rich Analysis
            raw_analysis = strat.get('analysis_summary', 'Belum ada analisa.')
            if len(raw_analysis) > 280: raw_analysis = raw_analysis[:277] + "..."
            analysis_text = html.escape(raw_analysis)
            message += f"🧠 <b>Analisa Macro &amp; Supply:</b>\n<i>{analysis_text}</i>\n\n"
            
            # 2. Key Metrics
            message += f"🛡️ <b>Data Kunci:</b>\n"
            message += f"• Fase: {strat.get('market_phase', 'Unknown')}\n"
            message += f"• Psikologis: {strat.get('psychology', 'Neutral')}\n"
            message += f"• RSI: {tech.get('rsi', 'N/A')} | MA Trend: {tech.get('trend_status', 'N/A')}\n"
            message += f"• Support: ${tech.get('support', 'N/A')} | Res: ${tech.get('resistance', 'N/A')}\n"
            
            # 3. Trade Setup
            entry = plan.get('entry_zone')
            if signal in ["BUY", "SELL"] and entry and entry != "N/A":
                 message += f"\n🎯 <b>Rencana Trade ({signal}):</b>\n" 
                 message += f"• Masuk: {entry}\n"
                 message += f"• Target: {plan.get('take_profit')}\n"
                 message += f"• Stop: {plan.get('stop_loss')}"

            # 4. News Section
            news_items = data.get('news', [])
            if news_items:
                message += f"\n📰 <b>Berita &amp; Geopolitik:</b>\n"
                # Always show 1 relevant news item
                for item in news_items[:1]:
                    title = html.escape(item.get('title', 'No Title'))
                    source = html.escape(item.get('source', 'Web'))
                    url = item.get('url', '')
                    if len(title) > 60: title = title[:57] + "..."
                    message += f"• <a href='{url}'>{title}</a> ({source})\n"
            
            message += f"\n🔗 <a href='{tv_link}'>Lihat Chart</a>\n\n"
            
        message += "<i>🤖 Disusun oleh AlphaSwarm AI (Commodity Squad)</i>"

        # 3. Send Request
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        
        try:
            r = requests.post(f"{self.base_url}/sendMessage", json=payload)
            if r.status_code == 200:
                print("✅ Commodity Alert Sent Successfully!")
            else:
                print(f"❌ Telegram Error: {r.text}")
        except Exception as e:
            print(f"❌ Network Error: {e}")

if __name__ == "__main__":
    # Test
    from dotenv import load_dotenv
    load_dotenv()
    agent = NotifierAgent()
    mock_data = {
        "BTC-USD": {
            "strategy": {
                "headline": "BTC SIAP JEBOL 100K! 🚀",
                "analysis_summary": "Bitcoin membentuk pola Golden Cross yang sangat bullish di time frame 4 jam. Akumulasi bandar terlihat jelas dari lonjakan volume di area support $92k. RSI memang agak jenuh beli (68), tapi sentimen pasar 'Greed' yang kuat karena arus masuk ETF kemungkinan akan mendorong harga menembus resisten tanpa koreksi dalam. Siap-siap serok jika ada dip.",
                "market_phase": "Markup (Bull)",
                "psychology": "Greed",
                "action_plan": {"signal": "BUY", "entry_zone": "$92k-$93k", "take_profit": "$100k", "stop_loss": "$89k"}
            },
            "technical": {"price": 95200, "support": 92000, "resistance": 98000, "rsi": 68, "volume_spike": 2.5},
            "news": [
                {"title": "BlackRock ETF Inflows Break Record", "source": "Bloomberg", "url": "https://bloomberg.com/btc"},
                {"title": "Bitcoin Golden Cross Confirmed on 4H Chart", "source": "CoinDesk", "url": "https://coindesk.com/btc"}
            ]
        },
        "ETH-USD": {
            "strategy": {
                "headline": "ETH Masih Galau, Wait & See 😴",
                "analysis_summary": "Berbeda dengan BTC, Ethereum masih terjebak sideways membosankan di $3,000 - $3,400. Bollinger Bands menyempit menandakan akan ada ledakan volatilitas sebentar lagi (Squeeze). Karena volume belum valid, sebaiknya jangan FOMO dulu. Tunggu konfirmasi breakout di atas $3,500 baru kita masuk posisi agresif.",
                "market_phase": "Accumulation",
                "psychology": "Neutral",
                "action_plan": {"signal": "WAIT", "entry_zone": "N/A"}
            },
            "technical": {"price": 3250, "support": 3000, "resistance": 3500, "rsi": 45, "volume_spike": 0.8},
            "news": [
                {"title": "Ethereum Gas Fees Drop to 5 Gwei", "source": "Etherscan", "url": "https://etherscan.io"}
            ]
        },
        "BNB-USD": {
            "strategy": {
                "headline": "BNB Mulai Bangun dari Tidur 🐂",
                "analysis_summary": "Binance Coin menunjukkan tanda-tanda pemulihan dengan volume beli yang meningkat signifikan. Resistance di $600 mulai diuji. Jika tembus, potensi lari ke ATH baru sangat terbuka. Fundamental Launchpool baru menjadi katalis positif.",
                "market_phase": "Markup (Early)",
                "psychology": "Optimism",
                "action_plan": {"signal": "BUY", "entry_zone": "$590-$600", "take_profit": "$650", "stop_loss": "$575"}
            },
            "technical": {"price": 595, "support": 580, "resistance": 620, "rsi": 55, "volume_spike": 1.2}
        },
        "SOL-USD": {
            "strategy": {
                "headline": "Solana Koreksi Wajar, Waktunya Serok? 📉",
                "analysis_summary": "Setelah rally panjang, SOL mengalami koreksi sehat ke area Fib 0.5. RSI sudah masuk area oversold (28), indikasi potensi pantulan teknikal (Technical Rebound). Volume jual mulai menipis, menandakan seller exhaustion.",
                "market_phase": "Correction",
                "psychology": "Fear",
                "action_plan": {"signal": "BUY", "entry_zone": "$130-$135", "take_profit": "$150", "stop_loss": "$125"}
            },
            "technical": {"price": 132, "support": 130, "resistance": 145, "rsi": 28, "volume_spike": 1.5}
        },
        "DOT-USD": {
            "strategy": {
                "headline": "Polkadot Masih Tidur Panjang 💤",
                "analysis_summary": "Secara teknikal DOT masih dalam tren bearish jangka panjang (Downtrend). Belum ada tanda-tanda reversal maupun volume spike. MA50 dan MA200 masih death cross. Sebaiknya hindari dulu sampai ada struktur market yang lebih jelas.",
                "market_phase": "Markdown (Bear)",
                "psychology": "Depression",
                "action_plan": {"signal": "WAIT", "entry_zone": "N/A"}
            },
            "technical": {"price": 6.5, "support": 6.0, "resistance": 7.2, "rsi": 35, "volume_spike": 0.5}
        }
    }
    agent.send_telegram_alert(mock_data)
