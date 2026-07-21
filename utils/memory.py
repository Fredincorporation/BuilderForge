from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from utils.supabase_client import get_supabase_client, is_configured
from utils.models import AgentMemoryRecord


class MemoryStore:
    """Short-term and long-term memory store for agent workflows."""

    def __init__(self) -> None:
        self.short_term: Dict[str, List[AgentMemoryRecord]] = {}
        self.supabase = get_supabase_client() if is_configured() else None

    def remember(
        self,
        project_id: str,
        content: str,
        source: str = "agent",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AgentMemoryRecord:
        record = AgentMemoryRecord(
            project_id=project_id,
            source=source,
            content=content,
            metadata=metadata or {},
        )
        self.short_term.setdefault(project_id, []).append(record)
        self._save_long_term(record)
        return record

    def retrieve(self, project_id: str, limit: int = 10) -> List[str]:
        records = self.short_term.get(project_id, [])
        if self.supabase:
            try:
                response = (
                    self.supabase.table("agent_memory")
                    .select("content")
                    .eq("project_id", project_id)
                    .order("created_at", desc=True)
                    .limit(limit)
                    .execute()
                )
                if response.data:
                    records = [AgentMemoryRecord(**{"project_id": project_id, **row}) for row in response.data]
            except Exception:
                pass
        return [record.content for record in records[-limit:]]

    def _save_long_term(self, record: AgentMemoryRecord) -> None:
        if not self.supabase:
            return
        try:
            self.supabase.table("agent_memory").insert(
                {
                    "project_id": record.project_id,
                    "source": record.source,
                    "content": record.content,
                    "metadata": record.metadata,
                    "created_at": record.timestamp,
                }
            ).execute()
        except Exception:
            pass


class MemoryQuery(BaseModel):
    project_id: str
    query_text: str
    results: List[str] = Field(default_factory=list)

    def summary(self) -> str:
        if not self.results:
            return "No memory found for this project yet."
        return "\n".join([f"- {item}" for item in self.results])
