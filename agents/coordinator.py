"""BuilderForge Coordinator Agent (Root Module Wrapper)."""

from __future__ import annotations

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from backend.agents.coordinator import CoordinatorAgent

__all__ = ["CoordinatorAgent"]
