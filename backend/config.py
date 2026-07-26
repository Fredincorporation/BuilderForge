"""BuilderForge Configuration Manager."""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load root & backend .env
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Settings(BaseSettings):
    """Application configuration settings backed by environment variables."""

    # Server settings
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Execution Mode
    SIMULATION_MODE: bool = os.getenv("SIMULATION_MODE", "true").lower() == "true"

    # LLM API Keys (optional for Live Mode)
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", "")

    # OKX API Credentials & Flags
    OKX_API_KEY: Optional[str] = os.getenv("OKX_API_KEY", "")
    OKX_SECRET_KEY: Optional[str] = os.getenv("OKX_SECRET_KEY", "")
    OKX_PASSPHRASE: Optional[str] = os.getenv("OKX_PASSPHRASE", "")
    OKX_PROJECT_ID: Optional[str] = os.getenv("OKX_PROJECT_ID", "")
    OKX_ENV: str = os.getenv("OKX_ENV", "testnet")
    OKX_USE_REAL_ASP: bool = os.getenv("OKX_USE_REAL_ASP", "false").lower() == "true"

    # OKX Blockchain Config
    OKX_RPC_URL: str = os.getenv("OKX_RPC_URL", os.getenv("OKX_TESTNET_RPC", "https://testrpc.xlayer.tech"))
    OKX_TESTNET_RPC: str = os.getenv("OKX_TESTNET_RPC", "https://testrpc.xlayer.tech")
    OKX_CHAIN_ID: int = int(os.getenv("OKX_CHAIN_ID", "195"))
    OKX_EXPLORER_BASE: str = os.getenv("OKX_EXPLORER_BASE", "https://www.okx.com/explorer/xlayer-test")

    # Agent Limits
    AGENT_MAX_ITER: int = int(os.getenv("AGENT_MAX_ITER", "10"))
    AGENT_MAX_RPM: int = int(os.getenv("AGENT_MAX_RPM", "20"))

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
