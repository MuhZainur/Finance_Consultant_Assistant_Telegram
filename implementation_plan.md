# AlphaSwarm: Autonomous Daily Investment Strategist 📈🤖
**Status**: Planning Phase
**Goal**: Create a fully autonomous AI system that wakes up daily, analyzes multi-market data (Stocks, Crypto, Gold), reasons about investment strategies, and delivers a comprehensive report to the user.

---

## 🏗️ Architecture Overview

The system is built as a **Multi-Agent Orchestration** using **LangGraph**, integrated with **MCP (Model Context Protocol)** for safe data access and **RAG** for real-time news analysis.

### Core Components:

1.  **The Brain (Orchestrator)**: LangGraph State Machine that manages the workflow.
2.  **The Swarm (Agents)**:
    *   🕵️ **Researcher Agents**: Scrape & Retrieve data (News, Prices, Technical Indicators).
    *   🧠 **Analyst Agent**: Deep reasoning (DeepSeek R1) to correlate data points.
    *   ⚖️ **Critic Agent**: Hallucination check & Risk assessment.
    *   📢 **Publisher Agent**: Formats and sends the report (Email/Telegram).
3.  **The Memory (RAG + SQL)**:
    *   **ChromaDB**: Vector store for news articles and reports.
    *   **SQLite (via MCP)**: User's Portfolio & Transaction History.
4.  **The Lab (Benchmarking)**:
    *   Compare performance/cost between OpenRouter (DeepSeek) vs Local (Qwen).

---

## 🔄 Workflow Diagram (The Daily Routine)

```mermaid
graph TD
    Start((⏰ Wake Up 06:00)) --> Researcher
    
    subgraph "Phase 1: Information Gathering"
        Researcher -->|Task: Get Stock Data| StockTool[yFinance/AlphaVantage]
        Researcher -->|Task: Get Pseudo-News| NewsRAG[News Aggregator (RAG)]
        Researcher -->|Task: Check Portfolio| MCP[MCP Server: Portfolio DB]
    end
    
    Researcher -->|Collected Data| Analyst
    
    subgraph "Phase 2: Reasoning & Strategy"
        Analyst -->|Reasoning Chain| DeepSeek[DeepSeek R1 (OpenRouter)]
        DeepSeek -->|Draft Strategy| Analyst
    end
    
    Analyst -->|Strategy Draft| Critic
    
    subgraph "Phase 3: Validation"
        Critic -->|Check Constraints| Rules{Hallucination / Risk Check}
        Rules -->|Pass| Publisher
        Rules -->|Fail| Analyst
    end
    
    subgraph "Phase 4: Optimization"
        Publisher -->|Log Metrics| Benchmark[Benchmark DB (Cost/Time)]
        Publisher -->|Send Report| User((📧 User Email))
    end
```

---

## 🛠️ Step-by-Step Implementation

### Phase 1: Foundation & Data (The "Eyes")
- [ ] **Setup Project Structure**: Poetry/Pipenv, Docker.
- [ ] **MCP Server**: Build a simple MCP server to expose `portfolio.db` (SQLite) to the Agent.
- [ ] **RAG Engine**: Implement `NewsRetriever` using ChromaDB + n-gram (BM25).
- [ ] **Visualization Module**: Port over `plotly` candlestick logic from `Stock_Forecasting` (Reuse existing robust code).

### Phase 2: The Swarm Squads (Hierarchical Teams)

Each "Squad" is an autonomous unit with a **Manager**, **Researcher**, and **Analyst**.

#### 1. 🦅 Stock Squad
- **Manager**: Orchestrates the workflow for Stocks.
- **Stock Researcher**: Scrapes specialized news (Earnings Call, Insider Trading).
- **Stock Analyst**: Technicals (Chart) + Fundamentals (P/E).
- **Target**: Core (NVDA) + Dynamic (Top Volume Leaders).

#### 2. 🪙 Crypto Squad
- **Manager**: Orchestrates Crypto workflow.
- **Crypto Researcher**: Scrapes Twitter/X Sentiment & Governance Proposals.
- **Crypto Analyst**: On-Chain Metrics + Cycle Theory.
- **Target**: **ALWAYS BTC** + Top 2 Dynamic Movers.

#### 3. 🌍 Macro Squad
- **Manager**: Global Context Provider.
- **Macro Researcher**: Fed Speeches, geopolitical news.
- **Macro Analyst**: Correlation Logic (DXY vs Gold).

### Phase 3: Reporting & Orchestration
- [x] **Smart Notifier (`notifier_agent.py`)**:
    *   **Role**: Aggregates JSON output from Manager.
    *   **Action**: Sends comprehensive HTML Text Alert via Telegram.
- [x] **Features**:
    *   **Rich Analysis**: 5-7 sentences covering Technicals, Fundamentals, Psychology.
    *   **Actionable**: Entry/Exit prices + Deep Links to TradingView.
- [ ] **Delivery Agent (`notifier_agent.py`)**:
    *   **Role**: Sends the PDF via Email/WhatsApp.

### Asset Filtering Strategy (The "Hybrid" Approach)
1.  **Core Watchlist (Always Analyzed)**:
    *   **Stocks**: NVDA, MSFT, AAPL, TSLA.
    *   **Crypto**: BTC, ETH, SOL.
    *   **Macro**: Gold (XAU), Oil (WTI), DXY.
2.  **Dynamic Hotlist (Opportunity Hunting)**:
    *   **Stocks**: Scan S&P 500 winners -> Pick Top 3 "Highest Relative Volume".
    *   **Crypto**: Scan Top 100 on Binance -> Pick Top 3 "Top Gainers".

### 📊 Data Points Context (Token-Efficient Input)
**We send these calculated metrics into the LLM context, NOT raw charts.**

### 📊 Data Points & Analysis Logic (The "57 Concepts" Integration)
*Refining the logic to cover the comprehensive User Glossary.*

#### 1. Category 1: Metrics & Indicators (Python Calculated)
*   **Technicals (Stock & Crypto)**:
    *   **Trend**: Moving Averages (MA20, MA50, MA200) -> Detect "Golden Cross" or "Death Cross".
    *   **Momentum**: RSI (Overbought >70 / Oversold <30), MACD Line & Histogram.
    *   **Levels**: Support & Resistance (Local Min/Max detection).
    *   **Volatility**: Bollinger Bands (Bandwidth).
    *   **Volume**: Volume Spike detection (Current Vol > 2x Avg Vol).
*   **Fundamentals (Stock Only via `yfinance`)**:
    *   **Valuation**: Market Cap, PER (Price/Earnings), PBV (Price/Book), EPS.
    *   **Income**: Dividends (Yield).
    *   **Corporate**: IPO Date context, Buyback info (if available).

#### 2. Category 2 & 3: Strategy, Psychology & Definitions (LLM Reasoning)
*   **System Prompt Instructions**:
    *   **Psychology**: Analyze Price + News to detect "FOMO" (Parabolic move + Hype news) or "Panic Selling" (Crash + FUD).
    *   **Strategic Advice**: ALWAYS provide actionable setup:
        *   *Entry*: "Limit Order at Support level X".
        *   *Protection*: "Stop Loss below support Y".
        *   *Target*: "Take Profit at Resistance Z".
    *   **Market Phase**: Classify as Bullish / Bearish / Sideways / Correction.
    *   **Asset Class**:
        *   Stock: "Blue Chip" vs "Second Liner" (based on Market Cap).
        *   Crypto: "Bitcoin" vs "Altcoin" vs "Meme/Gorengan".

### Phase 3: Reasoning & Verification (The "Wisdom")

### Phase 3: Reasoning & Verification (The "Wisdom")
- [ ] **DeepSeek Integration**: Connect OpenRouter API for the "Thinking" process.
- [ ] **Prompt Engineering**: "Act as a Hedge Fund Manager... Provide reasoning for Buying Gold..."
- [ ] **Critic Node**: Implement a self-correction loop (e.g., "Reasoning too vague, specificy support levels").

### Phase 4: Benchmarking & Optimization (The "Science")
- [ ] **Benchmark Suite**: Script to run the same analysis using:
    *   Model A: DeepSeek R1 (Reasoning) - Cost $0.05
    *   Model B: Qwen 2.5 7B (Local GGUF) - Cost $0.00
- [ ] **Comparison Report**: Generate table of Latency vs Quality vs Cost.

### Phase 5: Deployment
- [ ] **Dockerize**: Wrap everything in containers.
- [ ] **Scheduler**: Setup Cron job (or simple Python `schedule` loop).
- [ ] **Notification**: Connect SMTP (Email) or Telegram Bot API.

---

## 🔬 Tech Stack
| Component | Technology |
| :--- | :--- |
| **Orchestration** | LangGraph (Python) |
| **LLM Inference** | OpenRouter (DeepSeek R1) & Llama.cpp (Local Qwen) |
| **Data Access** | **MCP (Model Context Protocol)** Python SDK |
| **Vector DB** | ChromaDB (Local) |
| **Database** | SQLite (Portfolio) |
| **Tools** | yfinance, DuckDuckGo Search, BeautifulSoup |
| **Deployment** | Docker Receive |

---

## 🚨 Critical Engineering Challenges (Senior Level)
1.  **Hallucination Control**: Financial advice must be grounded. We use **Hybrid RAG** (Vector + Keyword) to ensure "News" is actually relevant.
2.  **Latency vs Cost**: We track token usage daily.
3.  **Structured Output**: The LLM must output JSON for the DB, but Markdown for the User Email.
