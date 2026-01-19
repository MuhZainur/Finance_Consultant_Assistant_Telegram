# AlphaSwarm: Autonomous Financial Intelligence Swarm 🦅

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)]()
[![Docker](https://img.shields.io/badge/Deployment-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)]()
[![OpenRouter](https://img.shields.io/badge/AI-OpenRouter-7F52FF?style=flat-square&logo=openai&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)]()

**AlphaSwarm** is a production-grade AI Agentic System designed to automate financial market analysis. It deploys a "Special Forces" swarm of agents to scout, analyze, and report on **Stocks (Wall St)**, **Crypto**, and **Commodities** in real-time.

It leverages **DeepSeek R1 (via OpenRouter)** for reasoning and online news fetching, ensuring analysis is grounded in live market events (Geopolitics, Fed Policy, Supply Shocks).

---

## 🏗️ The "Tri-Squad" Architecture

The system operates in a strictly orchestrated sequence to maximize efficiency and avoid API rate limits:

### 1. Wall Street Squad 🦅
*   **Target:** Top 5 US Stocks (Dynamic Filter: S&P 500 Leaders).
*   **Focus:** Earnings, Institutional Volume, Technical Breakouts.
*   **Output:** Telegram Alert with "Smart Compression" (Analysis + News).

### 2. Crypto Squad 🪙
*   **Target:** Bitcoin, Ethereum + 3 Dynamic Altcoins.
*   **Focus:** On-Chain Metrics, Sentiment, Bitcoin Dominance.
*   **Output:** "INTEL PASAR CRYPTO" Alert.

### 3. Commodity Squad 🛢️
*   **Target:** Gold (XAU), Silver (XAG), Crude Oil (WTI).
*   **Focus:** Macro Economics, Inflation, War/Geopolitics.
*   **Output:** "INTEL KOMODITAS" Alert.

---

## 💻 Tech Stack

| Component | Technologies |
| :--- | :--- |
| **Orchestrator** | Python 3.10, AsyncIO, BackgroundTasks |
| **AI Brain** | **DeepSeek R1 Online** (via OpenRouter) |
| **Data Layer** | `yfinance` (Market Data), OpenRouter Plugin (News) |
| **API Layer** | **FastAPI**, Uvicorn |
| **Notifications** | Telegram Bot API (HTML Parse Mode) |
| **Infrastructure** | Docker, Docker Compose (Ready) |

---

## 🚀 Installation & Usage

### 1. Prerequisites
*   Docker Desktop installed.
*   OpenRouter API Key.
*   Telegram Bot Token & Chat ID.

### 2. Setup Variables
Create a `.env` file in the root directory:
```bash
OPENROUTER_API_KEY=sk-or-your-key
TELEGRAM_BOT_TOKEN=123456:ABC-your-token
TELEGRAM_CHAT_ID=-100123456789
```

### 3. Run with Docker (Recommended)
```bash
# Build Image
docker build -t alphaswarm .

# Run Container
docker run -p 8080:8080 --env-file .env alphaswarm
```

### 4. API Endpoints
Once running, the system exposes a REST API:
*   `GET /health`: Check system status.
*   `POST /trigger`: Manually trigger the full swarm cycle (useful for Cron Jobs).

Example Trigger:
```bash
curl -X POST http://localhost:8080/trigger
```

---

## 📂 Project Structure

```
├── agents/                   # The AI Squads
│   ├── stocks/               # Wall St Logic
│   ├── crypto/               # Crypto Logic
│   ├── commodities/          # Commodity Logic
│   └── notifier_agent.py     # Telegram Handler
├── app.py                    # FastAPI Wrapper
├── run_alpha_swarm.py        # Core Logic (Orchestrator)
├── Dockerfile                # Deployment Config
├── requirements.txt          # Production Depedencies
└── README.md                 # You are here
```

---

*Created by **[MuhZainur]** - AI Engineer*
