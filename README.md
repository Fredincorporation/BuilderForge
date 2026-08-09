# 🔨 BuilderForge — Agentic Service Provider (ASP) for OKX

<div align="center">
    <strong>Turn any Web3 idea into a launched project — autonomously.</strong>
    <br>
    <em>Proof of concept for automated OKX ASP launch workflows.</em>
</div>

---

## 🚀 Key Highlights & Winning Features

- **OKX ASP Marketplace Ready**: Provides compliant `asp_manifest.json` for OKX.AI marketplace directory integration (`GET /asp/manifest`, `POST /asp/validate`).
- **Simulated Mode**: Runs end-to-end without external API keys, generating market research, tokenomics, Solidity contract code, and OKX X Layer Testnet simulation output.
- **Live Mode**: Supports Anthropic Claude Sonnet and OpenAI GPT-4o when API credentials are available.
- **Multi-Agent Pipeline**:
  1. **Researcher Agent**: Generates market analysis, competitor intelligence, and grant opportunities.
  2. **Creator Agent**: Synthesizes tokenomics, pitch assets, and smart contract source code.
  3. **Executor Agent**: Simulates OKX X Layer Testnet deployment and transaction metadata.
  4. **Analyzer Agent**: Produces ASP readiness scoring, risk assessment, and next actions.
- **Demo workflow**: A one-click sample project can pre-populate the dashboard, stream agent logs, and export the generated launch package.

---

## 💻 Quick Start & Running Locally

### Prerequisites
- Node.js 18+ & npm/bun
- Python 3.10+

### 1. Start Backend Server (FastAPI)

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt
python main.py
```
> The API will start at `http://localhost:8000`. Test endpoint: `http://localhost:8000/health`

### 2. Start Frontend App (Vite React)

```bash
cd frontend
npm install
npm run dev
```
> Open `http://localhost:5173` (or `http://localhost:3000`) in your browser.

---

## 🌐 Deploying to Production

### Deploying Backend to Render / Railway
1. Set Root Directory to `backend`
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Set Environment Variable: `SIMULATION_MODE=true`

### Deploying Frontend to Vercel
1. Set Root Directory to `frontend`
2. Build Command: `npm run build`
3. Environment Variable: `VITE_API_URL=https://your-backend-url.com`

---

## 📄 License
MIT License. Built for the OKX AI Genesis Hackathon 2026.
