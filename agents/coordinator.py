"""BuilderForge Coordinator Agent.

Main orchestrator that manages the project pipeline,
tracks phase transitions, and delegates to specialised agents.
"""

from __future__ import annotations

import json
from typing import Any

from crewai import Agent
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from config.settings import settings
from utils.models import ProjectData
from utils.state import add_crew_log


# ---------------------------------------------------------------------------
# LLM Configuration
# ---------------------------------------------------------------------------

def get_llm(temperature: float = 0.3) -> Any:
    """Get the configured LLM using environment-backed settings."""
    if settings.ANTHROPIC_API_KEY:
        return ChatAnthropic(
            model="claude-sonnet-4-20250514",
            temperature=temperature,
            max_tokens=4096,
        )
    if settings.OPENAI_API_KEY:
        return ChatOpenAI(
            model="gpt-4o",
            temperature=temperature,
        )
    raise RuntimeError("No LLM configured. Set ANTHROPIC_API_KEY or OPENAI_API_KEY.")


# ---------------------------------------------------------------------------
# Agent Definition
# ---------------------------------------------------------------------------

COORDINATOR_ROLE = """You are the Coordinator Agent, the central orchestrator of BuilderForge.
You manage the entire project lifecycle from idea to launch planning.

Your responsibilities:
1. Receive and structure user ideas into actionable project plans
2. Determine which phase the project is in and what needs to happen next
3. Delegate tasks to the Researcher, Creator, Executor, and Analyzer agents
4. Collect results and prepare them for the user dashboard
5. Track overall progress and ensure nothing falls through the cracks

You are strategic, organised, and communicate clearly with both users and agents."""

COORDINATOR_GOAL = """Orchestrate the complete BuilderForge pipeline:
1. Project Setup: Structure the user's idea into a clear brief
2. Phase Management: Track and transition between phases smoothly
3. Agent Coordination: Delegate to the right agent at the right time
4. Quality Control: Verify outputs before presenting to user
5. Progress Tracking: Maintain accurate progress metrics

Output a comprehensive project report at the end."""

COORDINATOR_BACKSTORY = """You were built to be the ultimate project conductor, 
able to see the full picture while managing every detail. You've coordinated 
hundreds of successful launches and understand what it takes to go from 
zero to shipped. Your multi-agent orchestration skills are legendary."""


def create_coordinator_agent() -> Agent:
    """Create and return the Coordinator Agent instance."""
    return Agent(
        role=COORDINATOR_ROLE,
        goal=COORDINATOR_GOAL,
        backstory=COORDINATOR_BACKSTORY,
        verbose=True,
        allow_delegation=True,
        llm=get_llm(),
        max_iter=settings.AGENT_MAX_ITER,
        max_rpm=settings.AGENT_MAX_RPM,
    )
