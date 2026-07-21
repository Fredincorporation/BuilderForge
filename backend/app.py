"""BuilderForge FastAPI Backend.

Exposes CrewAI agents and tools via REST API.
Supports async project creation, crew execution, wallet management, and analytics.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.projects import router as projects_router
from api.crew import router as crew_router
from api.wallet import router as wallet_router
from api.dealflow import router as dealflow_router
from api.launchpad import router as launchpad_router

# ============================================================================
# Logging Setup
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ============================================================================
# Application Lifecycle
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown handlers."""
    logger.info("BuilderForge Backend Starting...")
    yield
    logger.info("BuilderForge Backend Shutting Down...")


# ============================================================================
# FastAPI App
# ============================================================================
app = FastAPI(
    title="BuilderForge API",
    description="Autonomous Idea-to-Launch Agent for OKX Ecosystem",
    version="1.0.0",
    lifespan=lifespan,
)

# ============================================================================
# Middleware
# ============================================================================

# CORS: Allow frontend requests from localhost and deployed URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://0.0.0.0:3000",
        "http://0.0.0.0:5173",
        # Add production domain here when deployed
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Routes
# ============================================================================
app.include_router(projects_router, prefix="/api", tags=["projects"])
app.include_router(crew_router, prefix="/api", tags=["crew"])
app.include_router(wallet_router, prefix="/api", tags=["wallet"])
app.include_router(dealflow_router, prefix="/api", tags=["dealflow"])
app.include_router(launchpad_router, prefix="/api", tags=["launchpad"])


# ============================================================================
# Health Check
# ============================================================================
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        {"status": "ok", "service": "BuilderForge API"},
        status_code=200
    )


@app.get("/")
async def root():
    """API info endpoint."""
    return JSONResponse({
        "service": "BuilderForge API",
        "version": "1.0.0",
        "documentation": "/docs",
    })


# ============================================================================
# Error Handlers
# ============================================================================
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    logger.error(f"ValueError: {exc}")
    return JSONResponse(
        {"error": "Invalid input", "detail": str(exc)},
        status_code=400
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        {"error": "Internal server error", "detail": str(exc)},
        status_code=500
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
