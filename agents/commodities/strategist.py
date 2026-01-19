import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

class CommodityStrategist:
    """
    Generates investment strategies for Commodities (Gold, Silver, Oil) 
    using DeepSeek R1 with Online Search.
    """
    def __init__(self):
        load_dotenv()
        
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        self.model = "deepseek/deepseek-r1:online"

    async def generate_strategy(self, technical_summary: dict) -> dict:
        symbol = technical_summary.get('symbol', 'UNKNOWN')
        print(f"🧠 [Strategist] Thinking about {symbol} (Searching Web)...")
        
        system_prompt = """
        Anda adalah Chief Commodity Strategist dari AlphaSwarm (Global Maco Division). 
        Pengalaman 25 tahun di pasar Komoditas Berjangka (Futures).
        
        Tugas Anda: 
        1. Cari berita GEO-POLITIK & MAKRO EKONOMI terbaru (Perang, Inflasi, The Fed, OPEC) via Web Search.
        2. Analisa data teknikal aset komoditas ini.
        3. Berikan STRATEGI TRADING PROFESIONAL.
        
        Gunakan BAHASA INDONESIA yang tajam.
        
        --- 57 MARKET CONCEPTS (COMMODITY EDITION) ---
        1. SUPPLY & DEMAND:
           - Oil: Kebijakan OPEC+, Perang Timteng (Supply Shock).
           - Gold: Safe Haven (Ketakutan Global), Inflasi Hedge.
           - Silver: Industri (EV/Solar) demand.
           
        2. INTERMARKET ANALYSIS:
           - DXY (US Dollar): Musuh utama komoditas. DXY Naik = Gold Turun (biasanya).
           - Yields (US10Y): Bunga obligasi naik = Musuh Emas (karena Emas gak ada dividen).
           
        3. TECHNICALS:
           - Support/Resist klasik sangat kuat di komoditas.
           - Breakout biasanya memicu trend panjang (Trending Market).
           
        --- OUTPUT FORMAT (JSON) ---
        {
            "headline": "Judul bombastis/clickbait max 5 kata (Contoh: EMAS SIAP JEBOL ATH BARU!)",
            "market_phase": "Accumulation | Markup (Bull) | Distribution | Markdown (Bear)",
            "psychology": "Neutral | Fear | Greed | Inflation Panic | War Fear",
            "analysis_summary": "Paragraf lengkap (5-7 kalimat). Wajib bahas: DXY, geopolitik/makro, dan teknikal. Jelaskan KENAPA harga bergerak.",
            "news": [
                {"title": "Judul Berita 1", "source": "Sumber", "url": "URL"},
                {"title": "Judul Berita 2", "source": "Sumber", "url": "URL"}
            ],
            "action_plan": {
                "signal": "BUY | SELL | WAIT",
                "entry_zone": "Range Harga",
                "stop_loss": "Harga",
                "take_profit": "Harga"
            }
        }
        """
        
        user_prompt = f"""
        Asset: {symbol}
        Price: ${technical_summary.get('price', 'N/A')}
        
        TECHNICAL DATA:
        - Trend: {technical_summary.get('trend_status', 'N/A')}
        - MA20: {technical_summary.get('ma20', 'N/A')}, MA50: {technical_summary.get('ma50', 'N/A')}
        - RSI: {technical_summary.get('rsi', 'N/A')}
        - Support: {technical_summary.get('support', 'N/A')}, Resistance: {technical_summary.get('resistance', 'N/A')}
        - 52W High: {technical_summary.get('high_52w', 'N/A')}, Low: {technical_summary.get('low_52w', 'N/A')}
        - Volume Spike: {technical_summary.get('volume_spike', 'N/A')}
        
        INSTRUCTIONS:
        1. SEARCH web for latext news on {symbol} (Gold/Silver/Oil) + Macro (DXY/Fed).
        2. Analyze correlation with US Dollar/Geopolitics.
        3. Fill 'news' array.
        """
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            # Clean possible markdown wrapping
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            return json.loads(content.strip())
            
        except Exception as e:
            print(f"❌ Strategy Error: {e}")
            return {
                "headline": f"{symbol} Analysis Error",
                "analysis_summary": "Gagal mengambil analisa mental.",
                "news": [],
                "action_plan": {"signal": "WAIT"}
            }
