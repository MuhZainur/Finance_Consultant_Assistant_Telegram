# 📝 AlphaSwarm Project Checklist

## 1. Project Initialization & Infrastructure
- [ ] Create project directory `AlphaSwarm`
- [ ] Initialize Python environment (venv/poetry)
- [ ] Install Core Dependencies: `langgraph`, `langchain`, `fastmcp`, `chromadb`, `yfinance`, `duckduckgo-search`
- [ ] Setup Environment Variables (.env) for OpenRouter API Key

## 2. Crypto Squad POC (The Pilot) 🪙
- [x] **Infrastructure**: Create `agents/crypto_squad/` with `manager.py`, `researcher.py`, `analyst.py`.
- [x] **Data Tools (Input)**:
    *   Implement `CCXT` logic for "BTC + Top 2 Gainers" (Dynamic Screening).
    *   Implement `NewsFetcher` (DuckDuckGo RSS) for "Crypto Sentiment".
- [x] **Agent Logic (Basic)**:
    *   **Researcher**: Summarize last 24h news for specific coin.
    *   **Analyst**: Combine Price Trend + 24h Volume + Sentiment Summary.
- [x] **Agent Logic (Advanced - 57 Concepts)**:
    *   **Trend**: MA20/50/200, Golden/Death Cross detected.
    *   **Momentum**: MACD Signal + Histogram, RSI Levels.
    *   **Levels**: Support/Resistance (30d Lookback).
    *   **Volatility**: Bollinger Bands Position + Width (Squeeze).
    *   **Volume**: Volume Spike detection vs 20d Avg.
- [x] **Smart Filtering Logic**:
    *   **Core Logic**: Always analyze `BTC-USD` & `ETH-USD` (The "Prophets").
    *   **Dynamic Logic**: Scan 20+ coins, Pick Top 3 "Movers" (Volume/Trend).
    *   **Total**: 5 Unique Assets per Daily Report.
- [x] **Rich Analysis (57 Concepts)**:
    *   Update `CryptoStrategist` system prompt with user's full dictionary.
    *   Map Stock terms (EPS, PER) to Crypto equivalents (NVT, Staking) where possible.
    *   Focus on Psychology (FOMO, Panic) and Actionable Strategy (Cut Loss, Avg Down).
- [x] **Notification System**:
    *   Implement `NotifierAgent` to format Text-based emails/Telegram messages.
    *   Include TradingView Links: `https://www.tradingview.com/chart/?symbol={EXCHANGE}:{SYMBOL}`.
    *   **Localization**: Full Indonesian Support + Catchy Headlines.
- [ ] **Stock Squad Expansion**:
    *   Adapt filtering logic for Stocks (S&P 500 volume scan).
    *   Test run: Ensure JSON output contains "Signal", "Confidence", and "Reasoning".
    *   **Deliverable**: `crypto_report_final.json`

## 3. Stock & Macro Squads (Expansion Phases)
- [ ] **Stock Squad**: Clone Crypto logic, swap CCXT with YFinance.
- [ ] **Macro Squad**: Clone logic, swap with FRED/Gold API.

## 4. Reporting & Orchestration
- [ ] **Report Generator**: Build PDF engine to consume Squad JSONs.
- [ ] **Notifier**: Email dispatch logic.

## 5. Benchmarking & Evaluation (The Science)
- [ ] Create `benchmark.py` script
- [ ] Implement `CostTracker` to log token usage per run
- [ ] Run comparison: OpenRouter (DeepSeek) vs Local GGUF (Llama/Qwen)
- [ ] Generate Performance Report (Markdown table)

## 6. Automation & Deployment
- [x] Create Main Orchestrator (`run_alpha_swarm.py`)
    - [x] Implement sequential logic (Stock -> Crypto)
    - [x] Add Anti-Spam Delay (20s)
- [x] Verification & Testing
    - [x] Test Stock Squad isolated
    - [x] Test Full Dual-Squad Cycle
    - [x] Optimize Message Length (Top 5 Support)
    - [x] Migrate to OpenRouter Online Search (Anti-Timeout)

## 7. Commodity Squad Expansion (New)
- [x] Create `agents/commodities` module
    - [x] Analyst (Technical)
    - [x] Strategist (OpenRouter Online)
    - [x] Manager (Gold, Silver, Oil)
- [x] Update Notifier for Commodities
- [x] Update Orchestrator (Add Phase 3)

## 8. Final Polish
- [x] Delete legacy files and test scripts (`main.py`, `debug_*.py`, `test_*.py`)
- [x] Verify directory structure

## 9. Deployment Readiness (FastAPI + Docker)
- [x] Create clean `requirements.txt`
- [x] Wrap logic in `app.py` (FastAPI)
- [x] Create `Dockerfile` (optimized python-slim)
- [x] Verify Local API Startup

## 10. Documentation
- [x] Create Professional `README.md`
- [x] Create `.gitignore`
- [x] Create Detailed Architecture Flowchart (`flowchart.md`)
