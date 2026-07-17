"""BuilderForge Crew - CrewAI Pipeline Definition.

Defines the complete multi-agent workflow from idea to analysis.
Orchestrates 5 agents in a sequential pipeline with phase transitions.
"""

from __future__ import annotations

import json
import time
from typing import Any, Dict, List, Optional
from datetime import datetime

from crewai import Crew, Process, Task

from agents.coordinator import create_coordinator_agent, get_llm
from agents.researcher import create_researcher_agent
from agents.creator import create_creator_agent
from agents.executor import create_executor_agent
from agents.analyzer import create_analyzer_agent

from tools.research_tools import (
    search_web_for_opportunities,
    find_applicable_grants,
    analyze_competitors,
    find_target_audience,
)
from tools.content_tools import (
    generate_tokenomics,
    generate_pitch_sections,
    generate_social_copy,
    generate_website_copy,
    generate_contract_code,
)
from tools.blockchain_tools import (
    connect_okx_wallet,
    deploy_smart_contract,
    mint_tokens,
    estimate_gas,
    simulate_transaction_sequence,
)
from tools.analytics_tools import (
    calculate_project_metrics,
    analyze_sentiment,
    estimate_traction,
    suggest_next_steps,
)

from utils.state import ProjectData, ProjectPhase, add_crew_log


# ---------------------------------------------------------------------------
# Task Definitions
# ---------------------------------------------------------------------------

def create_research_tasks():
    """Create tasks for the Research phase."""
    return [
        Task(
            description=(
                "Research the market opportunity for the given project idea. "
                "Use the search tool to find market data, then analyse competitors, "
                "find applicable grants, and identify target audiences. "
                "Return a comprehensive JSON report with all findings."
            ),
            expected_output=(
                "A JSON object containing: market analysis, competitor analysis, "
                "applicable grants, target audiences, and market timing assessment."
            ),
            agent=create_researcher_agent(),
            tools=[
                search_web_for_opportunities,
                analyze_competitors,
                find_applicable_grants,
                find_target_audience,
            ],
        ),
    ]


def create_creation_tasks():
    """Create tasks for the Creation phase."""
    return [
        Task(
            description=(
                "Generate all launch assets for the project. Create tokenomics model, "
                "pitch deck sections, social media copy, website copy, and smart contract code. "
                "Use the content tools to generate each asset. "
                "Return all assets as a structured JSON object."
            ),
            expected_output=(
                "A JSON object containing: tokenomics model, pitch deck sections, "
                "social media copies, website copy, and smart contract code."
            ),
            agent=create_creator_agent(),
            tools=[
                generate_tokenomics,
                generate_pitch_sections,
                generate_social_copy,
                generate_website_copy,
                generate_contract_code,
            ],
        ),
    ]


def create_execution_tasks():
    """Create tasks for the Execution phase."""
    return [
        Task(
            description=(
                "Plan and simulate the on-chain deployment of the project. "
                "Connect to OKX wallet, simulate contract deployment, mint tokens, "
                "estimate gas costs, and produce a complete deployment sequence. "
                "Return a structured JSON deployment plan."
            ),
            expected_output=(
                "A JSON object containing: wallet connection, contract deployment "
                "simulation, token mint simulation, gas estimates, and deployment plan."
            ),
            agent=create_executor_agent(),
            tools=[
                connect_okx_wallet,
                deploy_smart_contract,
                mint_tokens,
                estimate_gas,
                simulate_transaction_sequence,
            ],
        ),
    ]


def create_analysis_tasks():
    """Create tasks for the Analysis phase."""
    return [
        Task(
            description=(
                "Analyse the complete project output. Calculate viability metrics, "
                "analyse market sentiment, estimate traction, and suggest next steps. "
                "Return a comprehensive analysis report as JSON."
            ),
            expected_output=(
                "A JSON object containing: project metrics score, sentiment analysis, "
                "traction estimates, next-step recommendations, and risk assessment."
            ),
            agent=create_analyzer_agent(),
            tools=[
                calculate_project_metrics,
                analyze_sentiment,
                estimate_traction,
                suggest_next_steps,
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# Crew Builders
# ---------------------------------------------------------------------------

def build_full_crew(verbose: bool = True) -> Crew:
    """Build the complete BuilderForge crew with all agents and sequential tasks."""
    coordinator = create_coordinator_agent()
    researcher = create_researcher_agent()
    creator = create_creator_agent()
    executor = create_executor_agent()
    analyzer = create_analyzer_agent()

    research_tasks = create_research_tasks()
    creation_tasks = create_creation_tasks()
    execution_tasks = create_execution_tasks()
    analysis_tasks = create_analysis_tasks()

    all_tasks = research_tasks + creation_tasks + execution_tasks + analysis_tasks

    return Crew(
        agents=[coordinator, researcher, creator, executor, analyzer],
        tasks=all_tasks,
        process=Process.sequential,
        verbose=verbose,
        max_rpm=10,
        memory=True,
        cache=True,
        output_log_file="data/crew_output.log",
    )


def build_phase_crew(phase: ProjectPhase, verbose: bool = True) -> Crew:
    """Build a crew for a single phase of the pipeline."""
    coordinator = create_coordinator_agent()

    if phase == ProjectPhase.RESEARCH:
        tasks = create_research_tasks()
        agents = [coordinator, create_researcher_agent()]
    elif phase == ProjectPhase.CREATION:
        tasks = create_creation_tasks()
        agents = [coordinator, create_creator_agent()]
    elif phase == ProjectPhase.EXECUTION:
        tasks = create_execution_tasks()
        agents = [coordinator, create_executor_agent()]
    elif phase == ProjectPhase.ANALYSIS:
        tasks = create_analysis_tasks()
        agents = [coordinator, create_analyzer_agent()]
    else:
        tasks = []
        agents = [coordinator]

    return Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose,
        max_rpm=10,
    )


# ---------------------------------------------------------------------------
# Pipeline Runner (Simulated - for demos without API keys)
# ---------------------------------------------------------------------------

def run_simulated_crew(project: ProjectData) -> ProjectData:
    """Run a simulated version of the entire pipeline.
    
    This bypasses the LLM API calls and uses pre-generated mock outputs.
    Useful for hackathon demos when API keys aren't available.
    """
    from tools.research_tools import search_web_for_opportunities
    from tools.content_tools import generate_tokenomics
    from tools.blockchain_tools import simulate_transaction_sequence
    from tools.analytics_tools import calculate_project_metrics

    description = project.description or project.title
    add_crew_log("Starting simulated crew execution...")
    time.sleep(0.5)

    # Phase 1: Research
    add_crew_log("🔍 Researcher agent analysing market...")
    project.progress = 0.2
    project.phase = ProjectPhase.RESEARCH.value

    research_data = json.loads(search_web_for_opportunities(description))
    grants_data = json.loads(TASK_DUMMY_GRANTS)
    competitors_data = json.loads(TASK_DUMMY_COMPETITORS)
    audience_data = json.loads(TASK_DUMMY_AUDIENCE)

    project.opportunity_report = {
        "market_research": research_data,
        "grants": grants_data,
        "competitors": competitors_data,
        "target_audience": audience_data,
    }
    project.research_output = json.dumps(project.opportunity_report, indent=2)
    add_crew_log("✅ Research complete — found grants, competitors, and audiences")

    # Phase 2: Creation
    add_crew_log("🎨 Creator agent generating assets...")
    project.progress = 0.4
    project.phase = ProjectPhase.CREATION.value

    tokenomics = json.loads(generate_tokenomics(project.title))
    pitch = json.loads(TASK_DUMMY_PITCH)
    social = json.loads(TASK_DUMMY_SOCIAL)
    website = json.loads(TASK_DUMMY_WEBSITE)
    contract = json.loads(TASK_DUMMY_CONTRACT)

    project.launch_assets = {
        "tokenomics": tokenomics,
        "pitch_deck": pitch,
        "social_copy": social,
        "website_copy": website,
        "smart_contract": contract,
    }
    project.creation_output = json.dumps(project.launch_assets, indent=2)
    add_crew_log("✅ Creation complete — tokenomics, content, and contracts generated")

    # Phase 3: Execution
    add_crew_log("⚡ Executor agent simulating on-chain deployment...")
    project.progress = 0.6
    project.phase = ProjectPhase.EXECUTION.value

    mock_wallet = {
        "address": "0x" + "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
        "balance": "12.45 OKT",
        "chain": "OKC Testnet",
    }
    deploy_plan = json.loads(simulate_transaction_sequence(project.title, mock_wallet["address"]))

    project.deployment_plan = {
        "wallet": mock_wallet,
        "deployment_sequence": deploy_plan,
    }
    project.execution_output = json.dumps(project.deployment_plan, indent=2)
    add_crew_log("✅ Execution complete — transactions simulated on OKC testnet")

    # Phase 4: Analysis
    add_crew_log("📊 Analyzer agent evaluating results...")
    project.progress = 0.8
    project.phase = ProjectPhase.ANALYSIS.value

    metrics = json.loads(calculate_project_metrics(project.title))
    next_steps = json.loads(TASK_DUMMY_NEXT_STEPS)

    project.metrics_report = {
        "viability_score": metrics,
        "recommendations": next_steps,
        "summary": f"Project {project.title} scores {metrics['overall_score']}/100 — "
                   f"rating: {metrics['rating']}",
    }
    project.analysis_output = json.dumps(project.metrics_report, indent=2)
    add_crew_log("✅ Analysis complete — metrics, recommendations, and next steps")

    # Final
    project.progress = 1.0
    project.phase = ProjectPhase.COMPLETE.value
    add_crew_log("🎉 BuilderForge pipeline complete! Ready for export and ASP listing.")

    return project


# ---------------------------------------------------------------------------
# Dummy data for simulated runs
# ---------------------------------------------------------------------------

TASK_DUMMY_GRANTS = json.dumps({
    "total_funding_available": 515000,
    "opportunities": [
        {"name": "OKX AI Genesis Hackathon Prize", "amount": "$30,000", "focus": "AI x Web3", "match_score": 10},
        {"name": "OKX Startup Lab Grant", "amount": "$50,000", "focus": "DeFi & AI", "match_score": 8},
        {"name": "Base Ecosystem Fund", "amount": "$75,000", "focus": "Onchain Apps", "match_score": 6},
    ]
})

TASK_DUMMY_COMPETITORS = json.dumps({
    "competitors": [
        {"name": "LaunchpadXYZ", "strengths": ["User base"], "weaknesses": ["No AI"], "market_share_pct": 28},
        {"name": "TokenMint Pro", "strengths": ["Easy tokens"], "weaknesses": ["No research"], "market_share_pct": 22},
    ],
    "opportunity": "Clear gap for AI-native end-to-end Agentic Service Provider",
})

TASK_DUMMY_AUDIENCE = json.dumps({
    "audiences": [
        {"segment": "Web3 Entrepreneurs", "size": "~500K"},
        {"segment": "Hackathon Participants", "size": "~100K"},
        {"segment": "DAO Tool Builders", "size": "~50K"},
    ]
})

TASK_DUMMY_PITCH = json.dumps({
    "problem": "Fragmented solutions, no AI automation",
    "solution": "Autonomous AI agents for end-to-end launch",
    "market_size": {"tam": "$4.8B", "sam": "$1.2B"},
})

TASK_DUMMY_SOCIAL = json.dumps({
    "twitter": "🚀 Launching the future of agentic service provision...",
    "linkedin": "Thrilled to announce our multi-agent system...",
})

TASK_DUMMY_WEBSITE = json.dumps({
    "hero": "Turn Ideas into Launched Products with AI Agents",
    "features": ["DealFlow", "LaunchPad Ally", "On-Chain Simulation", "ASP Ready"],
})

TASK_DUMMY_CONTRACT = json.dumps({
    "contract_name": "Token.sol",
    "language": "Solidity ^0.8.20",
    "code": "// SPDX-License-Identifier: MIT\npragma solidity ^0.8.20;\n...",
})

TASK_DUMMY_NEXT_STEPS = json.dumps({
    "steps": [
        {"priority": "HIGH", "action": "Review metrics and adjust strategy", "timeframe": "Day 7"},
        {"priority": "HIGH", "action": "Export complete project package", "timeframe": "Day 7"},
        {"priority": "MEDIUM", "action": "List as ASP on OKX.AI marketplace", "timeframe": "Week 3"},
    ]
})
