"""BuilderForge Backend Data Schemas (Pydantic models)."""

from __future__ import annotations

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ProjectCreate(BaseModel):
    title: str = Field(..., description="Title of the Web3 project")
    description: str = Field(..., description="Detailed description of project concept & vision")
    category: Optional[str] = Field("General", description="Project category (e.g. DeFi, DeAI, Token Launch, NFT)")


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    phase: Optional[str] = None
    progress: Optional[float] = None
    opportunity_report: Optional[Dict[str, Any]] = None
    launch_assets: Optional[Dict[str, Any]] = None
    deployment_plan: Optional[Dict[str, Any]] = None
    metrics_report: Optional[Dict[str, Any]] = None


class PipelineRunRequest(BaseModel):
    project_id: str
    phase: Optional[str] = "ALL"
    mode: Optional[str] = "SIMULATED"  # "SIMULATED" or "LIVE"


class ResearcherResult(BaseModel):
    market_size: str
    target_sector: str
    competitors: List[Dict[str, str]]
    grant_opportunities: List[Dict[str, Any]]
    target_audience: List[str]
    timing_score: int
    summary: str


class CreatorResult(BaseModel):
    token_name: str
    token_symbol: str
    total_supply: str
    allocations: Dict[str, str]
    smart_contract_code: str
    pitch_tagline: str
    elevator_pitch: str
    key_features: List[str]
    marketing_hooks: List[str]


class ExecutorResult(BaseModel):
    chain_id: int = 195
    network_name: str = "OKX X Layer Testnet"
    contract_address: str
    tx_hash: str
    gas_used_okt: str
    deployment_status: str = "CONFIRMED"
    explorer_url: str
    rpc_logs: List[str]


class AnalyzerResult(BaseModel):
    launch_readiness_score: int  # 0-100
    asp_status: str  # e.g. "VERIFIED_ASP_READY"
    risk_factors: List[Dict[str, str]]
    growth_projections: Dict[str, str]
    recommended_next_steps: List[str]
    executive_summary: str


class ProjectResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str = "General"
    phase: str = "IDEA_INPUT"
    progress: float = 0.0
    created_at: str
    opportunity_report: Optional[Dict[str, Any]] = None
    launch_assets: Optional[Dict[str, Any]] = None
    deployment_plan: Optional[Dict[str, Any]] = None
    metrics_report: Optional[Dict[str, Any]] = None
    logs: List[str] = []


class ASPManifest(BaseModel):
    schema_version: str = "1.0.0"
    provider: Dict[str, Any]
    agents: List[Dict[str, Any]]
    pricing_models: List[Dict[str, Any]]
    service_slas: Dict[str, Any]
    marketplace_listing: Dict[str, Any]
