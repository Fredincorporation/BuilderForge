"""BuilderForge Session State Manager.

Centralised management of all Streamlit session state keys.
Ensures consistent state across multi-page navigation.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime

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

from utils.models import ProjectData, ProjectPhase


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
        "agent_memory": {},
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
