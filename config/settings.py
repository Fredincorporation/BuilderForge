from __future__ import annotations

from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings  # type: ignore


class Settings(BaseSettings):
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    SUPABASE_URL: Optional[str] = None
    SUPABASE_KEY: Optional[str] = None
    OKX_API_KEY: Optional[str] = None
    OKX_SECRET_KEY: Optional[str] = None
    OKX_PASSPHRASE: Optional[str] = None
    OKX_PROJECT_ID: Optional[str] = None
    OKX_ENV: str = "testnet"
    OKX_RPC_URL: Optional[str] = "https://testrpc.xlayer.tech"
    OKX_USE_REAL_ASP: bool = False
    AGENT_TIMEOUT_SECONDS: int = 120
    AGENT_MAX_ITER: int = 10
    AGENT_MAX_RPM: int = 10
    NETWORK_NAME: str = "OKX X Layer Testnet"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
