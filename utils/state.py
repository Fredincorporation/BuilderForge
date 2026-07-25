"""BuilderForge Session State Manager.

Centralised persistent state management backed by SQLite (utils/db.py).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime
from uuid import uuid4

from utils.models import ProjectData, ProjectPhase
from utils.db import (
    db_save_project,
    db_get_all_projects,
    db_get_project_by_id,
    db_delete_project,
)

# Runtime state store for transient flags
_state: Dict[str, Any] = {
    "current_project_id": None,
    "crew_running": False,
    "crew_log": [],
    "wallet_connected": False,
    "wallet_address": "",
    "okx_asp_listed": False,
    "onboarding_done": False,
    "agent_memory": {},
}


def init_session_state() -> None:
    """Initialise default state values if missing."""
    defaults: Dict[str, Any] = {
        "current_project_id": None,
        "crew_running": False,
        "crew_log": [],
        "wallet_connected": False,
        "wallet_address": "",
        "okx_asp_listed": False,
        "onboarding_done": False,
        "agent_memory": {},
    }
    for key, value in defaults.items():
        if key not in _state:
            _state[key] = value


def _dict_to_project(d: Dict[str, Any]) -> ProjectData:
    """Convert dict to ProjectData model."""
    p = ProjectData(
        id=d.get("id", ""),
        title=d.get("title", ""),
        description=d.get("description", ""),
        category=d.get("category", "General"),
        phase=d.get("phase", "IDEA_INPUT"),
        progress=float(d.get("progress", 0.0)),
        created_at=d.get("created_at"),
    )
    p.opportunity_report = d.get("opportunity_report")
    p.launch_assets = d.get("launch_assets")
    p.deployment_plan = d.get("deployment_plan")
    p.metrics_report = d.get("metrics_report")
    return p


def _project_to_dict(p: ProjectData) -> Dict[str, Any]:
    """Convert ProjectData model to dict."""
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "category": p.category,
        "phase": p.phase if isinstance(p.phase, str) else p.phase.value,
        "progress": p.progress,
        "created_at": p.created_at,
        "opportunity_report": p.opportunity_report,
        "launch_assets": p.launch_assets,
        "deployment_plan": p.deployment_plan,
        "metrics_report": p.metrics_report,
    }


def get_current_project() -> Optional[ProjectData]:
    """Get the currently active project from database."""
    pid = _state.get("current_project_id")
    if not pid:
        projects = db_get_all_projects()
        if projects:
            return _dict_to_project(projects[0])
        return None
    p_dict = db_get_project_by_id(pid)
    return _dict_to_project(p_dict) if p_dict else None


def get_all_projects() -> List[ProjectData]:
    """Get all stored projects from SQLite database."""
    p_dicts = db_get_all_projects()
    return [_dict_to_project(d) for d in p_dicts]


def get_project_by_id(project_id: str) -> Optional[ProjectData]:
    """Get project by ID from SQLite database."""
    p_dict = db_get_project_by_id(project_id)
    return _dict_to_project(p_dict) if p_dict else None


def save_project(project: ProjectData) -> None:
    """Save or update a project in SQLite database."""
    p_dict = _project_to_dict(project)
    saved = db_save_project(p_dict)
    _state["current_project_id"] = saved["id"]


def delete_project(project_id: str) -> bool:
    """Delete a project record."""
    return db_delete_project(project_id)


def add_crew_log(message: str) -> None:
    """Append a timestamped message to the crew execution log."""
    logs = _state.get("crew_log", [])
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs.append(f"[{timestamp}] {message}")
    _state["crew_log"] = logs


def get_crew_logs() -> List[str]:
    """Retrieve execution logs."""
    return _state.get("crew_log", [])


def clear_crew_log() -> None:
    """Reset the crew execution log."""
    _state["crew_log"] = []


def new_project_id() -> str:
    """Generate a short unique project ID."""
    return uuid4().hex[:8]
