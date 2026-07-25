# 🔨 BuilderForge — Agentic Service Provider (ASP) for OKX

<div align="center">
    <strong>Turn any Web3 idea into a launched project — autonomously.</strong>
    <br>
    <em>Official Entry for the OKX AI Genesis Hackathon (July 2026)</em>
</div>

---

## 🚀 Key Highlights & Winning Features

- **OKX ASP Marketplace Ready**: Serves compliant `asp_manifest.json` for OKX.AI marketplace directory listing (`GET /asp/manifest`, `POST /asp/validate`).
- **Simulated Mode (Zero API Keys Required)**: Runs end-to-end out of the box generating realistic market research, tokenomics, Solidity smart contract code, and OKX X Layer Testnet transaction hashes.
- **Live Mode**: Supports Anthropic Claude Sonnet & OpenAI GPT-4o when API keys are configured.
- **Multi-Agent Pipeline (4 Agents + Coordinator)**:
  1. **Researcher Agent** (DealFlow market size, competitors, grant opportunities)
  2. **Creator Agent** (LaunchPad tokenomics distribution, Solidity contract, pitch deck)
  3. **Executor Agent** (OKX X Layer Testnet deployment, gas in OKT, EVM transaction hash)
  4. **Analyzer Agent** (ASP readiness score 0-100%, risk matrix, next actionable steps)
- **1-Click 60–90 Second Demo Flow**: One button on the homepage pre-populates a high-impact DeAI project, streams real-time agent execution logs, and displays the complete launch package.

---

## 🎬 60–90 Second Video Demo Script (For Hackathon Judges)

1. **0:00 - 0:15 | Intro & ASP Concept**:
   - *"Hi judges! Welcome to BuilderForge, an Agentic Service Provider (ASP) built for the OKX AI Ecosystem."*
   - *"BuilderForge turns a raw Web3 idea into market research, tokenomics, smart contracts, and OKX testnet deployment in under 60 seconds."*

2. **0:15 - 0:45 | One-Click Execution**:
   - Click **"Run Demo Project (1-Click)"** on the homepage.
   - Show the interactive 5-step modal: watch the Researcher Agent find TAM & eligible OKX Grants, the Creator Agent generate Solidity code, the Executor Agent simulate OKX X Layer deployment, and the Analyzer Agent compute the ASP score.

3. **0:45 - 1:15 | Dashboard & Artifact Inspection**:
   - Redirect to Dashboard: inspect the generated **Tokenomics Table**, **Solidity Smart Contract**, **OKX Tx Hash**, and click **"Export Launch Package (ZIP)"**.

4. **1:15 - 1:30 | OKX ASP Marketplace Listing**:
   - Navigate to `/asp-listing`: show the live `asp_manifest.json`, click **"Validate Spec"**, and test the interactive **"Agent-to-Agent Hiring Simulator"**.

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
3. Environment Variable: `VITE_API_URL=https://your-backend.up.railway.app/api`

---

## 📄 License
MIT License. Built for the OKX AI Genesis Hackathon 2026.
