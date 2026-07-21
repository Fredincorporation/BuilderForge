from __future__ import annotations

from enum import Enum
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, validator


class ProjectPhase(str, Enum):
    IDEA_INPUT = "Idea Input"
    RESEARCH = "Research & Discovery"
    CREATION = "Content & Asset Generation"
    EXECUTION = "Launch Planning & On-Chain"
    ANALYSIS = "Analysis & Next Steps"
    COMPLETE = "Complete"


class WalletConnection(BaseModel):
    connected: bool = False
    address: str = ""
    chain_id: int = 0
    chain_name: str = ""
    balance: str = "0"
    network: str = "testnet"
    error: Optional[str] = None
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class TransactionDetail(BaseModel):
    hash: str = ""
    from_address: str = ""
    to_address: str = ""
    status: str = "pending"
    block_number: Optional[int] = None
    timestamp: Optional[str] = None
    gas_used: Optional[int] = None
    gas_price_gwei: Optional[float] = None
    value: Optional[str] = "0"
    network: str = "OKC Testnet"
    note: Optional[str] = None


class AgentInput(BaseModel):
    project_id: str
    title: str
    description: str
    category: str
    goals: List[str]
    phase: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentOutput(BaseModel):
    summary: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    raw: Optional[str] = None
    success: bool = True
    errors: Optional[List[str]] = None


class ProjectData(BaseModel):
    id: str = ""
    title: str = ""
    description: str = ""
    goals: List[str] = Field(default_factory=list)
    category: str = "Other"
    created_at: str = ""
    phase: str = ProjectPhase.IDEA_INPUT.value
    progress: float = 0.0
    opportunity_report: Dict[str, Any] = Field(default_factory=dict)
    launch_assets: Dict[str, Any] = Field(default_factory=dict)
    deployment_plan: Dict[str, Any] = Field(default_factory=dict)
    metrics_report: Dict[str, Any] = Field(default_factory=dict)
    research_output: str = ""
    creation_output: str = ""
    execution_output: str = ""
    analysis_output: str = ""
    wallet_connected: bool = False
    wallet_address: str = ""
    wallet: WalletConnection = Field(default_factory=WalletConnection)
    transactions: List[TransactionDetail] = Field(default_factory=list)
    exported_formats: List[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
        extra = "ignore"

    @validator("progress")
    def progress_must_be_between_zero_and_one(cls, value: float) -> float:
        return max(0.0, min(value, 1.0))

    def add_transaction(self, tx: TransactionDetail) -> None:
        self.transactions.append(tx)


class AgentMemoryRecord(BaseModel):
    project_id: str
    source: str = "agent"
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
