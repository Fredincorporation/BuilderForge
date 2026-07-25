"""BuilderForge Coordinator Agent (Master Orchestrator)."""

from __future__ import annotations

import logging
import time
from typing import Dict, Any, Callable, Optional

from .researcher import ResearcherAgent
from .creator import CreatorAgent
from .executor import ExecutorAgent
from .analyzer import AnalyzerAgent

logger = logging.getLogger(__name__)


class CoordinatorAgent:
    """Master Orchestrator Agent for BuilderForge."""

    def __init__(self, mode: str = "SIMULATED"):
        self.mode = mode
        self.researcher = ResearcherAgent(mode=mode)
        self.creator = CreatorAgent(mode=mode)
        self.executor = ExecutorAgent(mode=mode)
        self.analyzer = AnalyzerAgent(mode=mode)

    def execute_pipeline(
        self,
        project_id: str,
        project_title: str,
        description: str,
        category: str = "General",
        log_callback: Optional[Callable[[str, float], None]] = None
    ) -> Dict[str, Any]:
        """
        Execute full multi-agent pipeline:
        Phase 1: Researcher Agent (0-25%)
        Phase 2: Creator Agent (25-50%)
        Phase 3: Executor Agent (50-75%)
        Phase 4: Analyzer Agent (75-100%)
        """
        def emit_log(msg: str, progress: float):
            logger.info(f"[{progress*100:.0f}%] {msg}")
            if log_callback:
                log_callback(msg, progress)

        emit_log(f"Coordinator initializing BuilderForge multi-agent pipeline for '{project_title}'...", 0.05)
        
        # ----------------------------------------------------
        # Phase 1: Research (Researcher Agent)
        # ----------------------------------------------------
        emit_log("Phase 1/4: [Researcher Agent] Analyzing market landscape, competitors & grant opportunities...", 0.15)
        time.sleep(0.3)
        opportunity_report = self.researcher.run(project_title, description, category)
        emit_log(f"Phase 1 Complete: Found TAM {opportunity_report['market_size']}, {len(opportunity_report['grant_opportunities'])} grants eligible.", 0.25)
        
        # ----------------------------------------------------
        # Phase 2: Creation (Creator Agent)
        # ----------------------------------------------------
        emit_log("Phase 2/4: [Creator Agent] Synthesizing tokenomics model & compiling Solidity smart contract...", 0.35)
        time.sleep(0.3)
        launch_assets = self.creator.run(project_title, description, category)
        emit_log(f"Phase 2 Complete: Tokenomics generated ({launch_assets['token_symbol']} - {launch_assets['total_supply']} supply), ERC-20 contract compiled.", 0.50)
        
        # ----------------------------------------------------
        # Phase 3: Execution (Executor Agent)
        # ----------------------------------------------------
        emit_log("Phase 3/4: [Executor Agent] Initiating smart contract deployment on OKX X Layer Testnet (Chain ID 195)...", 0.60)
        time.sleep(0.3)
        deployment_plan = self.executor.run(project_title, launch_assets["smart_contract_code"])
        emit_log(f"Phase 3 Complete: Contract deployed on OKX X Layer! Address: {deployment_plan['contract_address']} (Tx: {deployment_plan['tx_hash'][:14]}...)", 0.75)
        
        # ----------------------------------------------------
        # Phase 4: Analysis (Analyzer Agent)
        # ----------------------------------------------------
        emit_log("Phase 4/4: [Analyzer Agent] Evaluating ASP readiness score & generating OKX.AI manifest...", 0.85)
        time.sleep(0.3)
        metrics_report = self.analyzer.run(
            project_id=project_id,
            project_title=project_title,
            description=description,
            opportunity_report=opportunity_report,
            launch_assets=launch_assets,
            deployment_plan=deployment_plan
        )
        emit_log(f"Phase 4 Complete: Launch Readiness Score: {metrics_report['launch_readiness_score']}/100. Status: VERIFIED_ASP_READY!", 1.00)

        return {
            "opportunity_report": opportunity_report,
            "launch_assets": launch_assets,
            "deployment_plan": deployment_plan,
            "metrics_report": metrics_report,
            "status": "COMPLETE",
            "progress": 1.0,
        }
