# 🔨 BuilderForge — Agentic Service Provider (ASP) MVP

<div align="center">
    <img src="assets/builderforge_logo.svg" alt="BuilderForge" width="400"/>
    <br>
    <strong>Turn any idea into a launched product — autonomously.</strong>
    <br>
    <em>Built for the OKX AI Genesis Hackathon</em>
</div>

---

## 🏗️ Overview

**BuilderForge** is a multi-agent **Agentic Service Provider (ASP)** combining:
- **DealFlow** — Opportunity discovery, market research, grant finding, competitor analysis
- **LaunchPad Ally** — Idea-to-execution pipeline with content generation, smart contracts, and deployment simulation

5 specialized AI agents work together in a CrewAI pipeline to take a user from initial idea through research, creation, on-chain simulation, and analysis — complete with export and OKX.AI ASP listing.

### ✨ Demo
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://localhost:8501)

**Runs in simulated mode with zero API keys** — perfect for hackathon judging.

---

## 🧠 Architecture

### Multi-Agent System

```
                         ┌──────────────────┐
                         │   Coordinator    │
                         │   (Orchestrator) │
                         └────────┬─────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌─────────────────┐    ┌──────────────────┐     ┌─────────────────┐
│   Researcher    │    │     Creator      │     │    Executor     │
│ • Market research│    │ • Tokenomics     │     │ • OKX wallet    │
│ • Competitors   │    │ • Pitch deck     │     │ • Deploy sim    │
│ • Grants        │    │ • Social copy    │     │ • Gas estimates │
│ • Audiences     │    │ • Contract code  │     │ • Tx sequences  │
└─────────────────┘    └──────────────────┘     └─────────────────┘
                                                    │
                                                    ▼
                                          ┌─────────────────┐
                                          │    Analyzer     │
                                          │ • Metrics       │
                                          │ • Sentiment     │
                                          │ • Next steps    │
                                          └─────────────────┘
```

### Pipeline Flow

```
Idea Input → Research Phase → Creation Phase → Execution Phase → Analysis Phase → Export
  [Step 1]     [Step 2]        [Step 3]          [Step 4]        [Step 5]       [Done]
```

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Agent Framework** | CrewAI 0.61.x | Multi-agent orchestration |
| **AI Tools** | LangChain 0.2.x | Tool framework for agents |
| **LLM** | Anthropic Claude (Claude Sonnet 4) | Primary reasoning engine |
| **UI** | Streamlit 1.36.x | Dashboard and user interface |
| **Blockchain** | Custom viem-style simulation | OKC testnet tx simulation |
| **ASP Integration** | Custom OKX API stubs | OKX.AI marketplace listing |
| **Auth/Data** | Supabase (optional) | User auth + project persistence |
| **Styling** | Custom CSS | Cartoon brutalist design |

---

## 📁 Project Structure

```
BuilderForge/
│
├── app.py                          # Main entry point (Streamlit)
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── README.md                       # This file
│
├── agents/                         # AI Agent definitions
│   ├── __init__.py
│   ├── coordinator.py              # Main orchestrator agent
│   ├── researcher.py               # Market research agent
│   ├── creator.py                  # Content generation agent
│   ├── executor.py                 # On-chain execution agent
│   └── analyzer.py                 # Metrics & analysis agent
│
├── crew/                           # CrewAI pipeline
│   ├── __init__.py
│   └── builderforge_crew.py        # Task definitions & crew builder
│
├── tools/                          # LangChain tool definitions
│   ├── __init__.py
│   ├── research_tools.py           # Web search, grants, competitors
│   ├── content_tools.py            # Tokenomics, contracts, copy
│   ├── blockchain_tools.py         # OKX wallet, deploy, mint
│   └── analytics_tools.py          # Metrics, sentiment, traction
│
├── ui/                             # Streamlit UI components
│   ├── __init__.py
│   ├── styles.py                   # Brutalist CSS theme
│   └── components.py               # Reusable UI widgets
│
├── utils/                          # Shared utilities
│   ├── __init__.py
│   ├── state.py                    # Session state management
│   ├── supabase_client.py          # Supabase integration (optional)
│   └── okx_integration.py          # OKX wallet + ASP integration
│
├── pages/                          # Streamlit multi-pages
│   ├── __init__.py
│   ├── 1_New_Project.py            # Idea input & pipeline trigger
│   ├── 2_Dashboard.py              # Full results dashboard
│   ├── 3_DealFlow.py               # Opportunity discovery deep-dive
│   ├── 4_LaunchPad.py              # Content & deployment tools
│   └── 5_OKX_ASP_Listing.py        # ASP manifest & submission
│
├── assets/
│   └── builderforge_logo.svg       # App logo
│
└── data/                           # Runtime data (gitignored)
    └── .gitkeep
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or uv package manager

### 1. Clone & Install

```bash
git clone https://github.com/Fredincorporation/BuilderForge.git
cd BuilderForge

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup (Optional)

```bash
cp .env.example .env
# Edit .env with your keys if using real LLM mode
# For demo/simulated mode, leave as-is
```

### 3. Run the App

```bash
streamlit run app.py
```

The app opens at **http://localhost:8501** 🎉

---

## 🎮 How to Demo (For Judges)

### Simulated Mode (No API Keys — 30 Second Demo)

| Step | Action | What Judges See |
|------|--------|-----------------|
| 1 | Open `http://localhost:8501` | Home page with brutalist design, pipeline overview |
| 2 | Click **"START A NEW PROJECT"** | Navigate to New Project page |
| 3 | Enter project title + description + goals | Form with validation |
| 4 | Ensure **"Use Simulated Mode"** toggle is ON | Badge showing simulated mode |
| 5 | Click **"LAUNCH BUILDERFORGE"** | ⚡ **The magic happens:** progress bars, agent logs appear in real-time showing each phase |
| 6 | View results in **Dashboard** | 5 tabs showing Research, Creation, Execution, Analysis |
| 7 | Navigate to **DealFlow** | Market research, grants, competitors |
| 8 | Navigate to **LaunchPad** | Tokenomics, smart contract code, deployment simulation |
| 9 | Navigate to **OKX ASP Listing** | Build manifest, submit, see status dashboard |
| 10 | **Export** project as JSON from Dashboard | Download button |

**Total demo time: ~30 seconds** ⚡

### Real LLM Mode (With API Key)

1. Set `ANTHROPIC_API_KEY` in `.env`
2. Toggle **"Use Simulated Mode"** OFF on New Project page
3. Submit project — the real CrewAI pipeline executes
4. All agents use Claude to generate outputs

---

## 🔗 OKX ASP Integration

### What's Implemented

| Feature | Status | Description |
|---------|--------|-------------|
| ✅ Wallet Connection | Simulated | Connect OKX Web3 wallet on OKC testnet |
| ✅ Contract Deployment | Simulated | ERC-20 token deploy on OKC testnet |
| ✅ Token Minting | Simulated | Mint initial supply simulation |
| ✅ Transaction Sequence | Simulated | Full launch workflow simulation |
| ✅ Gas Estimates | Simulated | Cost estimates for all operations |
| ✅ ASP Manifest Builder | ✓ | Structured manifest for OKX.AI |
| ✅ ASP Submission | Simulated | Submit to OKX.AI marketplace |
| ✅ Production Guide | ✓ | Steps to go from sim to real |

### ASP Manifest Structure

The manifest follows OKX.AI's expected format:
```json
{
  "asp_version": "1.0.0",
  "name": "BuilderForge",
  "capabilities": ["market_research", "tokenomics_design", "smart_contract_creation", ...],
  "pricing": {
    "model": "freemium",
    "details": [
      {"tier": "free", "requests_per_day": 10, "price": 0},
      {"tier": "pro", "requests_per_day": 100, "price": 29}
    ]
  },
  "blockchain": {
    "supported_chains": ["OKC", "Ethereum", "Polygon", "Arbitrum"],
    "testnet": true
  }
}
```

### Production Deployment Roadmap

To move from simulation to production:
1. Create OKX Developer account → Get API credentials
2. Deploy contract verification on OKLink explorer
3. Connect to real OKC mainnet via OKX RPC endpoints
4. Implement OKX DEX liquidity provision
5. Submit real ASP listing to OKX.AI marketplace

---

## 🎨 Design: Cartoon Brutalist

The UI follows **cartoon brutalist** principles:
- **Bold black outlines** on all elements (3px borders)
- **Flat solid colors** — deep navy (#1a1a2e), orange accent (#ff6b35)
- **Chunky drop shadows** — 4-8px offset without blur
- **Expressive typography** — Space Grotesk, bold weights
- **Zero gradients** — every color is a flat hex value
- **Interactive feedback** — buttons press down on click (translate + smaller shadow)

---

## 🏆 Hackathon Submission Tips

### What Makes BuilderForge Stand Out

1. **Complete Multi-Agent System** — 5 agents with defined roles, goals, and tools
2. **CrewAI + LangChain Architecture** — Industry-standard frameworks
3. **OKX-Native Integration** — Wallet, testnet, ASP listing workflow
4. **Works Without API Keys** — Simulated mode for instant demos
5. **Beautiful UI** — Cartoon brutalist design that's visually distinctive
6. **Export Capabilities** — JSON download of complete project
7. **Clear ASP Path** — Manifest builder + submission + production guide

### Submission Checklist

- [x] Multi-agent orchestration (CrewAI)
- [x] LangChain tool integration
- [x] Streamlit UI with brutalist design
- [x] OKX wallet + testnet simulation
- [x] ASP listing workflow
- [x] Export functionality
- [x] Works without API keys
- [x] Comprehensive README
- [x] Project runs with `pip install -r requirements.txt && streamlit run app.py`

---

## 🛠️ Development

### Extending BuilderForge

```python
# 1. Add a new tool in tools/
@tool("my_new_tool")
def my_new_tool(param: str) -> str:
    """Description of what this tool does."""
    return json.dumps({"result": "data"})

# 2. Add a new agent in agents/
def create_my_agent() -> Agent:
    return Agent(role="...", goal="...", backstory="...", tools=[my_new_tool])

# 3. Add tasks in crew/builderforge_crew.py
def create_my_tasks():
    return [Task(description="...", agent=create_my_agent(), tools=[my_new_tool])]

# 4. Add a new page in pages/
# pages/6_My_Feature.py → automatically appears in sidebar
```

### Testing

```bash
# Run syntax check
python -c "import py_compile; py_compile.compile('app.py', doraise=True)"

# Try importing modules
python -c "from utils.state import init_session_state; print('OK')"
python -c "from crew.builderforge_crew import build_full_crew; print('OK')"
```

---

## 📄 License

MIT — Built for the OKX AI Genesis Hackathon

---

<div align="center">
    <strong>BuilderForge</strong> — <em>From idea to launched product, autonomously.</em>
    <br>
    <a href="https://github.com/Fredincorporation/BuilderForge">GitHub</a>
    · <a href="https://www.okx.com/ai">OKX.AI</a>
    · <a href="https://docs.crewai.com">CrewAI Docs</a>
</div>
