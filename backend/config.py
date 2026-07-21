"""FastAPI Backend Configuration.

Settings for the BuilderForge API server.
"""

from __future__ import annotations

import os
from typing import Optional
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # API Settings
    api_title: str = "BuilderForge API"
    api_version: str = "1.0.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server Settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    reload: bool = debug
    
    # CORS Settings
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Database Settings (optional)
    database_url: Optional[str] = os.getenv("DATABASE_URL")
    
    # Supabase Settings
    supabase_url: Optional[str] = os.getenv("SUPABASE_URL")
    supabase_key: Optional[str] = os.getenv("SUPABASE_KEY")
    
    # CrewAI / LLM Settings
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # OKX Settings
    okx_testnet_url: str = os.getenv("OKX_TESTNET_URL", "https://okc-testnet-rpc.okdogechain.com")
    okx_chain_id: int = int(os.getenv("OKX_CHAIN_ID", "195"))  # OKC testnet
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()


if __name__ == "__main__":
    settings = get_settings()
    print(f"API: {settings.api_title} v{settings.api_version}")
    print(f"Debug: {settings.debug}")
    print(f"Server: {settings.host}:{settings.port}")
