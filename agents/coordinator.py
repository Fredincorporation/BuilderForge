"""BuilderForge Coordinator Agent (Root Module Wrapper)."""

from __future__ import annotations

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

BACKEND_DIR = os.path.join(BASE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from backend.agents.coordinator import CoordinatorAgent
from crewai import Agent


def get_llm(temperature: float = 0.7):
    """Return an LLM instance or model string for CrewAI agents."""
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if openai_key:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)
        except Exception:
            return "gpt-4o-mini"
    elif anthropic_key:
        try:
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=temperature)
        except Exception:
            return "anthropic/claude-3-5-sonnet-20241022"
    return "gpt-4o-mini"


COORDINATOR_ROLE = """You are the Chief Coordinator Agent of BuilderForge.
You orchestrate the entire multi-agent workflow from project inception to execution and analysis.
You ensure seamless alignment across research, content creation, blockchain execution, and analytics."""

COORDINATOR_GOAL = """Coordinate and manage all sub-agents to transform product ideas into fully deployed Web3 & AI applications."""

COORDINATOR_BACKSTORY = """You are a master Web3 product architect with deep knowledge of decentralized systems, AI automation, and project leadership."""


def create_coordinator_agent() -> Agent:
    """Create and return the Coordinator Agent instance."""
    return Agent(
        role=COORDINATOR_ROLE,
        goal=COORDINATOR_GOAL,
        backstory=COORDINATOR_BACKSTORY,
        verbose=True,
        allow_delegation=True,
        llm=get_llm(0.2),
        max_iter=15,
        max_rpm=10,
    )


__all__ = ["CoordinatorAgent", "create_coordinator_agent", "get_llm"]

