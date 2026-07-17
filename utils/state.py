"""BuilderForge Session State Manager.

Centralised management of all Streamlit session state keys.
Ensures consistent state across multi-page navigation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field, asdict

# ---------------------------------------------------------------------------
# Graceful Streamlit import — works outside Streamlit runtime (e.g., tests)
# ---------------------------------------------------------------------------
try:
    import streamlit as st
    _has_streamlit = True
except (ImportError, ModuleNotFoundError, RuntimeError):
    import warnings
    warnings.warn("Streamlit not available — using fallback in-memory state")
    _has_streamlit = False

    # dummy module to avoid AttributeError on st.session_state
    class _FakeSt:
        class _SessionState(dict):
            def __getattr__(self, k):
                return self.get(k)
            def __setattr__(self, k, v):
                self[k] = v
            def get(self, k, default=None):
                return super().get(k, default)
        session_state = _SessionState()

    st = _FakeSt()


class ProjectPhase(Enum):
    """Phases of the BuilderForge pipeline."""
    IDEA_INPUT = "Idea Input"
    RESEARCH = "Research & Discovery"
    CREATION = "Content & Asset Generation"
    EXECUTION = "Launch Planning & On-Chain"
    ANALYSIS = "Analysis & Next Steps"
    COMPLETE = "Complete"


@dataclass
class ProjectData:
    """Represents a single project through the pipeline."""
    id: str = ""
    title: str = ""
    description: str = ""
    goals: List[str] = field(default_factory=list)
    category: str = "Other"
    created_at: str = ""
    phase: str = ProjectPhase.IDEA_INPUT.value
    progress: float = 0.0

    # Phase outputs
    opportunity_report: Dict[str, Any] = field(default_factory=dict)
    launch_assets: Dict[str, Any] = field(default_factory=dict)
    deployment_plan: Dict[str, Any] = field(default_factory=dict)
    metrics_report: Dict[str, Any] = field(default_factory=dict)

    # Raw outputs from agents
    research_output: str = ""
    creation_output: str = ""
    execution_output: str = ""
    analysis_output: str = ""

    # Blockchain
    wallet_connected: bool = False
    wallet_address: str = ""
    transactions: List[Dict[str, Any]] = field(default_factory=list)

    # Export
    exported_formats: List[str] = field(default_factory=list)


def init_session_state() -> None:
    """Initialise all session state variables."""
    defaults: Dict[str, Any] = {
        "page": "New Project",
        "projects": [],
        "current_project_id": None,
        "crew_running": False,
        "crew_log": [],
        "wallet_connected": False,
        "wallet_address": "",
        "okx_asp_listed": False,
        "onboarding_done": False,
        "dark_mode": True,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_current_project() -> Optional[ProjectData]:
    """Get the currently active project, if any."""
    pid = st.session_state.get("current_project_id")
    if not pid:
        return None
    projects: List[ProjectData] = st.session_state.get("projects", [])
    for p in projects:
        if p.id == pid:
            return p
    return None


def save_project(project: ProjectData) -> None:
    """Save or update a project in session state."""
    projects: List[ProjectData] = st.session_state.get("projects", [])
    for i, p in enumerate(projects):
        if p.id == project.id:
            projects[i] = project
            break
    else:
        projects.append(project)
    st.session_state["projects"] = projects
    st.session_state["current_project_id"] = project.id


def add_crew_log(message: str) -> None:
    """Append a timestamped message to the crew execution log."""
    logs = st.session_state.get("crew_log", [])
    timestamp = datetime.now().strftime("%H:%M:%S")
    logs.append(f"[{timestamp}] {message}")
    st.session_state["crew_log"] = logs


def clear_crew_log() -> None:
    """Reset the crew execution log."""
    st.session_state["crew_log"] = []


def new_project_id() -> str:
    """Generate a short unique project ID."""
    from uuid import uuid4
    return uuid4().hex[:8]


def get_phase_index(phase_name: str) -> int:
    """Map phase name to its numerical index for progress bars."""
    phases = [p.value for p in ProjectPhase]
    try:
        return phases.index(phase_name)
    except ValueError:
        return 0
