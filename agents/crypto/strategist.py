import os
import json
from openai import AsyncOpenAI

class CryptoStrategist:
    """
    The 'Brain' of the Crypto Squad. 🧠
    Interprets Hard Metrics (Layer 1) into Strategic Advice (Layer 2).
    """
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        self.model = "deepseek/deepseek-r1:online"

    async def generate_strategy(self, technical_summary: dict) -> dict:
        """
        Uses DeepSeek R1 with Online Search to generate sophisticated crypto strategy.
        """
        symbol = technical_summary.get('symbol', technical_summary.get('ticker', 'UNKNOWN'))
        print(f"🧠 [Strategist] Thinking about {symbol} (Searching Web)...")
        
        system_prompt = """
        Anda adalah Chief Crypto Strategist dari AlphaSwarm. Pengalaman 20 tahun di pasar Saham & Crypto.
        
        Tugas Anda: 
        1. Cari berita AKTUAL/TERBARU tentang koin ini menggunakan Web Search (Hype, FUD, Development, Tokenomics).
        2. Analisa data teknikal yang diberikan.
        3. Berikan STRATEGI INVESTASI PROFESIONAL menggunakan '57 Market Concepts'.
        
        Gunakan BAHASA INDONESIA yang luwes, tajam, dan mudah dipahami.
        
        --- OUTPUT FORMAT (JSON) ---
        {
            "headline": "Judul bombastis/clickbait max 5 kata (Contoh: BTC SIAP MELEDAK KE 100K!)",
            "market_phase": "Accumulation | Markup (Bull) | Distribution | Markdown (Bear)",
            "psychology": "Neutral | Fear | Greed | FOMO | Panic",
            "analysis_summary": "Paragraf lengkap (5-7 kalimat) dalam BAHASA INDONESIA. Integrasikan berita dan data on-chain/teknikal. Jelaskan KENAPA harus Buy/Wait.",
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
        Analyze {symbol} based on this data:
        
        TECHNICALS:
        - Price: {technical_summary.get('price')}
        - Trend: {technical_summary.get('trend_status')} (MA20: {technical_summary.get('ma20')})
        - RSI: {technical_summary.get('rsi')}
        - Volatility: BB Width {technical_summary.get('bb_width')}
        - Volume Spike: {technical_summary.get('volume_spike')}
        - Support/Res: {technical_summary.get('support')} / {technical_summary.get('resistance')}
        
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
            return json.loads(content)
            
        except Exception as e:
            print(f"❌ Strategist Error: {e}")
            return {
                "headline": f"{symbol} Analysis Error",
                "analysis_summary": "Gagal mengambil analisa mental.",
                "news": [],
                "action_plan": {"signal": "WAIT"}
            }

if __name__ == "__main__":
    # Test stub
    import asyncio
    async def test():
        strat = CryptoStrategist()
        mock_data = {
            "ticker": "BTC-USD", 
            "technical_indicators": {"trend": {"status": "Bullish", "ma_cross_signal": "GOLDEN CROSS"}},
            "price": 95000
        }
        res = await strat.generate_strategy(mock_data, ["BTC hits ATH"])
        print(json.dumps(res, indent=2))
        
    asyncio.run(test())
