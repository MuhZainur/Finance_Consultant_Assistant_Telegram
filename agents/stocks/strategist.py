import os
import json
from openai import AsyncOpenAI
from dotenv import load_dotenv

class StockStrategist:
    """
    Generates investment strategies for US Stocks using DeepSeek R1 with Online Search.
    Standardized to use AsyncOpenAI for non-blocking I/O.
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
        symbol = technical_summary.get('symbol', technical_summary.get('ticker', 'UNKNOWN'))
        print(f"🧠 [Strategist] Thinking about {symbol} (Searching Web)...")
        
        system_prompt = """
        Anda adalah Chief Stock Strategist dari AlphaSwarm Wall Street Division. Pengalaman 20 tahun di pasar Saham Global.
        
        Tugas Anda: 
        1. Cari berita AKTUAL/TERBARU tentang saham ini menggunakan Web Search (Earnings, Price Action, Analyst Ratings).
        2. Analisa data teknikal yang diberikan.
        3. Berikan STRATEGI INVESTASI PROFESIONAL menggunakan '57 Market Concepts'.
        
        Gunakan BAHASA INDONESIA yang luwes, tajam, dan mudah dipahami.
        
        --- OUTPUT FORMAT (JSON) ---
        {
            "headline": "Judul bombastis/clickbait max 5 kata (Contoh: NVIDIA SIAP MELESAT 20%!)",
            "market_phase": "Accumulation | Markup (Bull) | Distribution | Markdown (Bear)",
            "psychology": "Neutral | Fear | Greed | FOMO | Panic",
            "analysis_summary": "Paragraf lengkap (5-7 kalimat) dalam BAHASA INDONESIA. Integrasikan berita terbaru yang Anda temukan dengan data teknikal. Jelaskan KENAPA harus Buy/Wait.",
            "news": [
                {"title": "Judul Berita 1", "source": "Sumber", "url": "URL"},
                {"title": "Judul Berita 2", "source": "Sumber", "url": "URL"}
            ],
            "action_plan": {
                "signal": "BUY | SELL | WAIT | CUT LOSS",
                "entry_zone": "Range Harga",
                "stop_loss": "Harga",
                "take_profit": "Harga"
            }
        }
        """
        
        user_prompt = f"""
        Ticker: {symbol}
        Price: ${technical_summary.get('price', 'N/A')}
        
        TECHNICAL DATA:
        - Trend: {technical_summary.get('trend_status', 'N/A')}
        - MA20: {technical_summary.get('ma20', 'N/A')}, MA50: {technical_summary.get('ma50', 'N/A')}
        - RSI: {technical_summary.get('rsi', 'N/A')}
        - Support: {technical_summary.get('support', 'N/A')}, Resistance: {technical_summary.get('resistance', 'N/A')}
        - 52W High: {technical_summary.get('high_52w', 'N/A')}, Low: {technical_summary.get('low_52w', 'N/A')}
        - Volume Spike: {technical_summary.get('volume_spike', 'N/A')}
        
        INSTRUCTIONS:
        1. SEARCH the web for the latest news (last 24-48 hours) regarding {symbol}.
        2. Combine technicals + news to form a strategy.
        3. Fill the 'news' array in JSON with valid URLs found.
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
