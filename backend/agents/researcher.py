"""BuilderForge Researcher Agent (DealFlow Intelligence)."""

from __future__ import annotations

import logging
from typing import Dict, Any

try:
    from tools.web_search import search_market_data
except ImportError:
    from ..tools.web_search import search_market_data

logger = logging.getLogger(__name__)


class ResearcherAgent:
    """Agent responsible for market intelligence, competitor analysis, and grant discovery."""

    def __init__(self, mode: str = "SIMULATED"):
        self.mode = mode

    def run(self, project_title: str, description: str, category: str = "General") -> Dict[str, Any]:
        """Run research pipeline and return structured result."""
        logger.info(f"[Researcher Agent] Executing research for '{project_title}'...")
        
        research_data = search_market_data(project_title, category)
        
        return {
            "market_size": research_data["market_size"],
            "target_sector": research_data["target_sector"],
            "competitors": research_data["competitors"],
            "grant_opportunities": research_data["grant_opportunities"],
            "target_audience": research_data["target_audience"],
            "timing_score": research_data["timing_score"],
            "summary": research_data["summary"],
        }
