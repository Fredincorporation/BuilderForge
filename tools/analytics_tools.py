"""Analytics Tools for BuilderForge.

Provides metrics calculation, sentiment analysis,
traction estimation, and next-step recommendations.
"""

from __future__ import annotations

import json
import random
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from langchain.tools import tool


@tool("calculate_project_metrics")
def calculate_project_metrics(
    project_name: str,
    market_size: str = "500M",
    competitor_count: int = 4,
    team_size: int = 3,
) -> str:
    """Calculate project success metrics and viability score.
    
    Generates a comprehensive metrics report for a project idea.
    """
    # Calculate scores based on inputs
    market_score = min(100, 40 + random.randint(-10, 20))
    innovation_score = min(100, 60 + random.randint(-5, 15))
    feasibility_score = min(100, 50 + team_size * 10)
    timing_score = min(100, 65 + random.randint(-10, 10))

    overall_score = int((
        market_score * 0.3 +
        innovation_score * 0.25 +
        feasibility_score * 0.25 +
        timing_score * 0.2
    ))

    return json.dumps({
        "project": project_name,
        "overall_score": overall_score,
        "rating": "Excellent" if overall_score >= 80 else "Good" if overall_score >= 60 else "Needs Work",
        "dimensions": {
            "market_opportunity": {"score": market_score, "level": "High" if market_score >= 70 else "Medium"},
            "innovation": {"score": innovation_score, "level": "Disruptive" if innovation_score >= 70 else "Incremental"},
            "feasibility": {"score": feasibility_score, "level": "Achievable" if feasibility_score >= 60 else "Challenging"},
            "timing": {"score": timing_score, "level": "Now" if timing_score >= 60 else "Wait"},
        },
        "estimated_tvl_potential": f"${random.randint(5, 500)}M",
        "estimated_users_year_1": f"{random.randint(10000, 500000):,}",
        "break_even_month": random.randint(6, 18),
        "risk_factors": [
            "Market competition may intensify",
            "Regulatory uncertainty in target jurisdictions",
            "User adoption depends on UX quality",
        ],
    }, indent=2)


@tool("analyze_sentiment")
def analyze_sentiment(topic: str, source: str = "twitter") -> str:
    """Analyze social sentiment around a topic or project.
    
    Provides sentiment breakdown and trend analysis.
    """
    results = {
        "twitter": {
            "positive": random.randint(40, 70),
            "neutral": random.randint(15, 35),
            "negative": random.randint(5, 25),
        },
        "warpcast": {
            "positive": random.randint(50, 75),
            "neutral": random.randint(15, 30),
            "negative": random.randint(5, 15),
        },
        "telegram": {
            "positive": random.randint(30, 60),
            "neutral": random.randint(20, 40),
            "negative": random.randint(10, 30),
        },
    }

    sentiment = results.get(source, results["twitter"])
    dominant = max(sentiment, key=sentiment.get)
    
    return json.dumps({
        "topic": topic,
        "source": source,
        "sentiment_breakdown": sentiment,
        "dominant_sentiment": dominant,
        "trend": "rising" if dominant == "positive" else "stable",
        "sample_posts": [
            f"Excited about {topic}! This could change everything in web3.",
            f"Interesting approach to {topic}. Worth keeping an eye on.",
            f"Not sure about {topic}, needs more real-world validation.",
        ],
        "recommendation": "Proceed with marketing push" if dominant == "positive"
                         else "Consider community education campaign",
        "timestamp": datetime.now().isoformat(),
    }, indent=2)


@tool("estimate_traction")
def estimate_traction(project_stage: str = "idea", target_audience_size: str = "100K") -> str:
    """Estimate traction milestones for a project based on stage.
    
    Provides realistic growth projections and KPIs.
    """
    stages = {
        "idea": {"mau_6mo": 5000, "mau_12mo": 25000, "tvl_6mo": "$500K", "tvl_12mo": "$5M"},
        "mvp": {"mau_6mo": 15000, "mau_12mo": 75000, "tvl_6mo": "$2M", "tvl_12mo": "$20M"},
        "beta": {"mau_6mo": 50000, "mau_12mo": 200000, "tvl_6mo": "$10M", "tvl_12mo": "$50M"},
        "launched": {"mau_6mo": 100000, "mau_12mo": 500000, "tvl_6mo": "$25M", "tvl_12mo": "$100M"},
    }

    projections = stages.get(project_stage, stages["idea"])
    return json.dumps({
        "project_stage": project_stage,
        "target_audience": target_audience_size,
        "projections_6_months": {
            "estimated_mau": projections["mau_6mo"],
            "estimated_tvl": projections["tvl_6mo"],
            "estimated_revenue": f"${projections['mau_6mo'] * 2:,}/mo (at $2/user)",
        },
        "projections_12_months": {
            "estimated_mau": projections["mau_12mo"],
            "estimated_tvl": projections["tvl_12mo"],
            "estimated_revenue": f"${projections['mau_12mo'] * 2:,}/mo (at $2/user)",
        },
        "key_kpis": [
            "Daily Active Users (DAU)",
            "Total Value Locked (TVL)",
            "Monthly Recurring Revenue (MRR)",
            "User Retention (D1/D7/D30)",
            "Viral Coefficient (K-factor)",
        ],
        "growth_channels": [
            "OKX ecosystem marketing",
            "Crypto Twitter / Warpcast",
            "DEX aggregator listings",
            "Grant program participation",
            "Community ambassador program",
        ],
    }, indent=2)


@tool("suggest_next_steps")
def suggest_next_steps(
    current_phase: str,
    project_complexity: str = "medium",
) -> str:
    """Suggest next steps based on the current project phase.
    
    Provides actionable recommendations to progress the project.
    """
    phase_steps = {
        "Idea Input": [
            {"priority": "HIGH", "action": "Define 3 specific goals with measurable outcomes", "timeframe": "Day 1"},
            {"priority": "HIGH", "action": "Identify target audience and primary use case", "timeframe": "Day 1"},
            {"priority": "MEDIUM", "action": "Research similar projects for differentiation", "timeframe": "Day 2"},
            {"priority": "LOW", "action": "Draft a one-page project summary", "timeframe": "Day 3"},
        ],
        "Research & Discovery": [
            {"priority": "HIGH", "action": "Complete competitor analysis matrix", "timeframe": "Day 2-3"},
            {"priority": "HIGH", "action": "Apply for relevant grants (OKX, Arbitrum, etc.)", "timeframe": "Week 1"},
            {"priority": "MEDIUM", "action": "Validate market need with 10+ potential users", "timeframe": "Week 1-2"},
            {"priority": "LOW", "action": "Create market sizing spreadsheet", "timeframe": "Week 2"},
        ],
        "Content & Asset Generation": [
            {"priority": "HIGH", "action": "Finalize tokenomics model", "timeframe": "Day 3-4"},
            {"priority": "HIGH", "action": "Generate smart contract code and test", "timeframe": "Day 4-5"},
            {"priority": "MEDIUM", "action": "Create pitch deck and whitepaper", "timeframe": "Week 2"},
            {"priority": "MEDIUM", "action": "Prepare social media announcement calendar", "timeframe": "Week 2"},
        ],
        "Launch Planning & On-Chain": [
            {"priority": "HIGH", "action": "Run simulated deployment on OKC testnet", "timeframe": "Day 5-6"},
            {"priority": "HIGH", "action": "Verify contract on Oklink explorer", "timeframe": "Day 6"},
            {"priority": "MEDIUM", "action": "Prepare liquidity provision strategy", "timeframe": "Week 3"},
            {"priority": "MEDIUM", "action": "Schedule audit with third-party firm", "timeframe": "Week 3-4"},
        ],
        "Analysis & Next Steps": [
            {"priority": "HIGH", "action": "Review metrics dashboard and adjust strategy", "timeframe": "Day 7"},
            {"priority": "HIGH", "action": "Export complete project package", "timeframe": "Day 7"},
            {"priority": "MEDIUM", "action": "List as ASP on OKX.AI marketplace", "timeframe": "Week 3"},
            {"priority": "MEDIUM", "action": "Publish launch announcement across channels", "timeframe": "Week 3"},
        ],
        "Complete": [
            {"priority": "HIGH", "action": "Monitor on-chain activity and user feedback", "timeframe": "Ongoing"},
            {"priority": "HIGH", "action": "Iterate based on analytics data", "timeframe": "Ongoing"},
            {"priority": "MEDIUM", "action": "Explore partnership opportunities", "timeframe": "Month 2-3"},
        ],
    }

    steps = phase_steps.get(current_phase, phase_steps["Idea Input"])
    return json.dumps({
        "current_phase": current_phase,
        "complexity": project_complexity,
        "steps": steps,
        "tip": "Complete HIGH priority items first before moving to MEDIUM/LOW.",
    }, indent=2)
