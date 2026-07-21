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

**BuilderForge** is a modern **Agentic Service Provider (ASP)** with a **React frontend** and **Python FastAPI backend**:
- **Frontend**: React + TanStack Start (Vite) with Tailwind CSS & Radix UI
- **Backend**: FastAPI + CrewAI with 5 specialized agents
- **Features**: DealFlow (market research), LaunchPad (idea-to-execution), OKX integration

5 specialized AI agents work together in a CrewAI pipeline to take a user from initial idea through research, creation, on-chain simulation, and analysis — exposed via a REST API.

### ✨ Live Deployment
- **Frontend**: http://localhost:3000 (or https://yourdomain.com)
- **Backend API**: http://localhost:8000 (or https://api.yourdomain.com)
- **API Docs**: http://localhost:8000/docs (Swagger UI)

**Runs in simulated mode with zero API keys** — perfect for hackathon judging.

---

## 🧠 Architecture

### System Diagram

```
┌─────────────────────────────────────────┐
│  FRONTEND (React/TanStack Start)        │
│  ├── Dashboard (projects)               │
│  ├── New Project Form                   │
│  ├── DealFlow (opportunities)           │
│  ├── LaunchPad (launches)               │
│  └── Wallet (simulation)                │
│                                         │
│  API Client: src/lib/api.ts             │
│  Hooks: src/hooks/useApi.ts             │
│  (React Query for state management)     │
└──────────────────┬──────────────────────┘
                   │
        REST API (JSON/HTTP)
                   │
┌──────────────────▼──────────────────────┐
│  BACKEND (FastAPI/Python)               │
│  ├── /api/projects (CRUD)               │
│  ├── /api/crew (CrewAI execution)       │
│  ├── /api/wallet (OKX simulation)       │
│  ├── /api/dealflow (opportunities)      │
│  └── /api/launchpad (launches)          │
│                                         │
│  Crew: crew/builderforge_crew.py        │
│  Agents: agents/*.py (5 specialized)    │
│  Tools: tools/*.py (research, content)  │
│  Memory: utils/memory.py (agent context)│
│  Models: utils/models.py (Pydantic)     │
└─────────────────────────────────────────┘
```

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
│ • Market search │    │ • Tokenomics     │     │ • OKX wallet    │
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
| **Frontend** | React + TanStack Start (Vite) | Modern SSR-capable React framework |
| **Styling** | Tailwind CSS + Radix UI | Component library + utility-first CSS |
| **State** | React Query (TanStack Query) | Server state management & caching |
| **Routing** | TanStack Router | File-based routing |
| **Backend API** | FastAPI | Async Python web framework |
| **Agent Framework** | CrewAI 1.15+ | Multi-agent orchestration |
| **AI Tools** | LangChain 0.3+ | Tool framework for agents |
| **LLM** | Anthropic Claude / OpenAI | Primary reasoning engines |
| **Async** | asyncio + ThreadPoolExecutor | Background job execution |
| **Blockchain** | Custom simulation | OKC testnet tx simulation |
| **Database** | Supabase (optional) | Project persistence |
| **Deployment** | Docker + nginx | Production containerization |

---

## 📁 Project Structure

```
BuilderForge/
│
├── frontend/                        # React + TanStack Start (Loveable export)
│   ├── src/
│   │   ├── routes/                  # File-based routes (TanStack Router)
│   │   │   ├── index.tsx            # Home page
│   │   │   ├── dashboard.tsx        # Projects dashboard
│   │   │   ├── new-project.tsx      # Create project form
│   │   │   ├── dealflow.tsx         # Opportunities
│   │   │   ├── launchpad.tsx        # Launches
│   │   │   └── __root.tsx           # Root layout
│   │   ├── components/
│   │   │   └── ui/                  # Radix UI components
│   │   ├── hooks/
│   │   │   └── useApi.ts            # React Query hooks for API calls
│   │   ├── lib/
│   │   │   └── api.ts               # Fetch-based API client
│   │   ├── server.ts                # Server middleware
│   │   └── styles.css               # Tailwind + custom styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── .env.example
│
├── backend/                         # FastAPI Python server
│   ├── app.py                       # FastAPI entry point
│   ├── config.py                    # Settings & configuration
│   ├── api/
│   │   ├── __init__.py
│   │   ├── projects.py              # POST/GET /api/projects
│   │   ├── crew.py                  # POST /api/crew/run
│   │   ├── wallet.py                # Wallet & simulation endpoints
│   │   ├── dealflow.py              # GET /api/dealflow
│   │   └── launchpad.py             # GET /api/launchpad
│   ├── agents/                      # AI Agent definitions
│   │   ├── __init__.py
│   │   ├── coordinator.py           # Main orchestrator
│   │   ├── researcher.py            # Market research
│   │   ├── creator.py               # Content generation
│   │   ├── executor.py              # On-chain execution
│   │   └── analyzer.py              # Metrics & analysis
│   ├── crew/
│   │   ├── __init__.py
│   │   └── builderforge_crew.py     # Task definitions & crew builder
│   ├── tools/                       # LangChain tools
│   │   ├── __init__.py
│   │   ├── research_tools.py        # Web search, grants
│   │   ├── content_tools.py         # Tokenomics, contracts
│   │   ├── blockchain_tools.py      # OKX wallet, deployment
│   │   └── analytics_tools.py       # Metrics, sentiment
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── state.py                 # Session state
│   │   ├── models.py                # Pydantic models
│   │   ├── memory.py                # Agent memory store
│   │   └── okx_integration.py       # OKX integration
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # Environment settings
│   ├── requirements.txt             # Python dependencies
│   ├── .env.example
│   ├── run.sh                       # Linux/Mac startup script
│   └── run.bat                      # Windows startup script
│
├── requirements.txt                 # Main dependencies (FastAPI + CrewAI)
├── .env.example                     # Environment template
├── README.md                        # This file
├── LICENSE
└── docker-compose.yml               # (Optional) Container setup
```

---

## 🚀 Quick Start

### Prerequisites
- **Node.js 18+** (for frontend)
- **Python 3.10+** (for backend)
- **npm or bun** (frontend package manager)
- **pip** (Python package manager)

### 1. Clone & Setup

```bash
git clone https://github.com/Fredincorporation/BuilderForge.git
cd BuilderForge

# Create Python virtual environment for backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

**Backend** (`.env` in root):
```bash
cp .env.example .env
# Edit with your API keys (optional for simulated mode)
# ANTHROPIC_API_KEY=
# OPENAI_API_KEY=
```

**Frontend** (`frontend/.env`):
```bash
cd frontend
cp .env.example .env
# Default: REACT_APP_API_URL=http://localhost:8000/api
cd ..
```

### 3. Install Frontend Dependencies

```bash
cd frontend
npm install  # or: bun install
cd ..
```

### 4. Run Both Services

**Terminal 1 — Backend (FastAPI)**:
```bash
cd backend
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Backend runs at: **http://localhost:8000**  
API Docs: **http://localhost:8000/docs**

**Terminal 2 — Frontend (React)**:
```bash
cd frontend
npm run dev  # or: bun dev
```

Frontend runs at: **http://localhost:3000** or **http://localhost:5173**

---

## 📡 API Endpoints

All endpoints return JSON. Base URL: `http://localhost:8000/api`

### Projects
```
POST   /api/projects                    # Create project
GET    /api/projects                    # List all projects
GET    /api/projects/{id}               # Get project by ID
PATCH  /api/projects/{id}               # Update project
DELETE /api/projects/{id}               # Delete project
```

### Crew Execution
```
POST   /api/crew/run                    # Start crew workflow (returns task_id)
GET    /api/crew/{task_id}              # Get execution status
GET    /api/crew/{task_id}/logs         # Get execution logs
POST   /api/crew/{task_id}/cancel       # Cancel execution
```

### Wallet & Blockchain
```
POST   /api/wallet/connect              # Connect wallet
GET    /api/wallet                      # Get current wallet
POST   /api/wallet/disconnect           # Disconnect wallet
POST   /api/wallet/simulate             # Simulate transaction
GET    /api/wallet/gas-estimate         # Estimate gas
```

### DealFlow & LaunchPad
```
GET    /api/dealflow                    # List opportunities
GET    /api/dealflow/{id}               # Get opportunity
GET    /api/launchpad                   # List launches
GET    /api/launchpad/{id}              # Get launch
```

### Health
```
GET    /health                          # Health check
GET    /                                # API info
```

See `backend/app.py` for full documentation and Swagger UI at `/docs`.

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
