"""BuilderForge FastAPI Backend Application.

Main entrypoint for running the OKX Agentic Service Provider (ASP) backend.
Exposes multi-agent pipeline routes, OKX testnet integration, and ASP listing APIs.
"""

from __future__ import annotations

import os
import sys
import logging
from contextlib import asynccontextmanager

# Set backend directory as primary sys.path entry
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

if BASE_DIR in sys.path:
    sys.path.remove(BASE_DIR)
sys.path.insert(0, BASE_DIR)

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import settings
from api.projects import router as projects_router
from api.crew import router as crew_router
from api.wallet import router as wallet_router
from api.dealflow import router as dealflow_router
from api.launchpad import router as launchpad_router
from api.asp import router as asp_router

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle handler."""
    # Detect and remove a seeded runtime DB (only if it contains known demo IDs)
    try:
        import sqlite3
        db_file = os.path.join(ROOT_DIR, "data", "builderforge.db")
        seeded_ids = {"f97b8957", "08e3177f", "de51c18b"}
        if os.path.exists(db_file):
            try:
                conn = sqlite3.connect(db_file)
                cur = conn.cursor()
                cur.execute("SELECT id FROM projects LIMIT 10")
                rows = cur.fetchall()
                conn.close()
                present = {r[0] for r in rows if r and r[0]}
                # If any known seeded id is present, remove the DB to start clean
                if seeded_ids & present:
                    logger.warning("Seeded demo projects detected in runtime DB — removing local DB to start clean.")
                    try:
                        os.remove(db_file)
                    except Exception as e:
                        logger.error(f"Failed to remove seeded DB file: {e}")
            except Exception as e:
                logger.warning(f"Unable to inspect runtime DB: {e}")
    except Exception:
        # Non-fatal: continue startup even if DB cleanup check fails
        pass

    logger.info("=" * 60)
    logger.info("🚀 BuilderForge OKX ASP Backend Initializing...")
    logger.info(f"⚡ Mode: {'SIMULATED (No API keys required)' if settings.SIMULATION_MODE else 'LIVE'}")
    logger.info(f"🔗 OKX Network: OKX X Layer Testnet (Chain ID {settings.OKX_CHAIN_ID})")
    logger.info("=" * 60)
    yield
    logger.info("BuilderForge Backend Shutting Down...")


app = FastAPI(
    title="BuilderForge ASP API",
    description="Autonomous Multi-Agent Idea-to-Launch ASP for OKX Ecosystem",
    version="1.2.0",
    lifespan=lifespan,
)

# Enable CORS for local dev and production deploy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers under both /api and root prefixes for max compatibility
app.include_router(projects_router, prefix="/api", tags=["projects"])
app.include_router(projects_router, tags=["projects_direct"])

app.include_router(crew_router, prefix="/api", tags=["crew"])
app.include_router(crew_router, tags=["crew_direct"])

app.include_router(wallet_router, prefix="/api", tags=["wallet"])
app.include_router(wallet_router, tags=["wallet_direct"])

app.include_router(dealflow_router, prefix="/api", tags=["dealflow"])
app.include_router(launchpad_router, prefix="/api", tags=["launchpad"])

app.include_router(asp_router, prefix="/api", tags=["asp"])
app.include_router(asp_router, tags=["asp_direct"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        {
            "status": "ok",
            "service": "BuilderForge ASP API",
            "simulation_mode": settings.SIMULATION_MODE,
            "chain_id": settings.OKX_CHAIN_ID,
        },
        status_code=200
    )


@app.get("/")
async def root():
    """Root info endpoint."""
    return JSONResponse({
        "service": "BuilderForge OKX ASP API",
        "version": "1.2.0",
        "docs": "/docs",
        "health": "/health",
        "asp_manifest": "/asp/manifest",
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
