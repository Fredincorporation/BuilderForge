"""Research Tools for BuilderForge.

Provides market research, competitor analysis, grant discovery,
and opportunity identification capabilities.
"""

from __future__ import annotations

import json
import random
from typing import Any, Dict, List, Optional
from datetime import datetime

from langchain.tools import tool


# ---------------------------------------------------------------------------
# In-memory mock databases for hackathon demo
# ---------------------------------------------------------------------------

GRANT_DATABASE = [
    {"name": "OKX Startup Lab Grant", "amount": "$50,000", "chain": "OKC", "deadline": "2026-08-15", "focus": "DeFi & AI"},
    {"name": "Arbitrum Foundation Grant", "amount": "$25,000", "chain": "Arbitrum", "deadline": "2026-09-01", "focus": "Layer 2"},
    {"name": "Polygon Village Grant", "amount": "$10,000", "chain": "Polygon", "deadline": "2026-07-30", "focus": "Consumer dApps"},
    {"name": "Solana Superteam Grant", "amount": "$100,000", "chain": "Solana", "deadline": "2026-10-01", "focus": "Infrastructure"},
    {"name": "Celo Web3 Social Impact", "amount": "$15,000", "chain": "Celo", "deadline": "2026-08-20", "focus": "Social Impact"},
    {"name": "Base Ecosystem Fund", "amount": "$75,000", "chain": "Base", "deadline": "2026-09-15", "focus": "Onchain Apps"},
    {"name": "OKX AI Genesis Hackathon Prize", "amount": "$30,000", "chain": "OKC", "deadline": "2026-07-31", "focus": "AI x Web3"},
    {"name": "Optimism RetroPGF Round 6", "amount": "$200,000", "chain": "Optimism", "deadline": "2026-11-01", "focus": "Public Goods"},
]

TREND_TOPICS = [
    "AI Agent Launchpads on L2s",
    "Intent-based DeFi protocols",
    "Token-bound accounts for DAOs",
    "Decentralized compute for AI training",
    "SocialFi with on-chain reputation",
    "Liquidity aggregation across chains",
    "Zero-knowledge identity solutions",
    "Real-world asset tokenization",
    "Autonomous AI trading agents",
    "Gamified DeFi rewards mechanisms",
]


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool("search_web_for_opportunities")
def search_web_for_opportunities(query: str) -> str:
    """Search the web for market opportunities, trends, and competitors.
    
    Use this to research a project idea or market space.
    Returns structured opportunity data.
    """
    # Simulate web search results for the demo
    results = [
        {
            "source": "OKX Research",
            "title": f"Market Analysis: {query}",
            "snippet": f"The {query} market is experiencing rapid growth with 3.2x YoY increase in active wallets. "
                       f"Key competitors include established players but a gap exists in AI-powered onboarding.",
            "relevance": 0.92,
        },
        {
            "source": "CoinGecko Trends",
            "title": f"Top Gainers in {query} Sector",
            "snippet": f"Projects in {query} space have seen average TVL growth of 45% in Q2 2026. "
                       f"New entrants focusing on UX and AI integration are outperforming.",
            "relevance": 0.88,
        },
        {
            "source": "Dune Analytics",
            "title": f"On-Chain Activity: {query}",
            "snippet": f"Daily active users in {query} category up 67% month-over-month. "
                       f"Average transaction value: $245. Top protocols: Uniswap, Aave, Compound.",
            "relevance": 0.85,
        },
    ]
    return json.dumps({"query": query, "results": results, "timestamp": datetime.now().isoformat()}, indent=2)


@tool("find_applicable_grants")
def find_applicable_grants(project_description: str, category: str = "") -> str:
    """Find grants and funding opportunities applicable to a project.
    
    Use this to identify grants, subsidies, and hackathon prizes.
    """
    # Filter grant database based on project description keywords
    keywords = project_description.lower().split()
    matching_grants = []

    for grant in GRANT_DATABASE:
        score = 0
        for kw in keywords:
            if kw in grant["focus"].lower():
                score += 1
            if kw in grant["chain"].lower():
                score += 1
            if kw in grant["name"].lower():
                score += 2

        if score > 0 or not keywords:
            matching_grants.append({**grant, "match_score": score})

    # Sort by relevance and return top 5
    matching_grants.sort(key=lambda x: x["match_score"], reverse=True)
    top_grants = matching_grants[:5]

    return json.dumps({
        "total_funding_available": sum(int(g["amount"].replace("$", "").replace(",", "")) for g in top_grants),
        "opportunities": top_grants,
        "recommendation": f"Based on your project, the best fit is '{top_grants[0]['name']}' "
                         f"({top_grants[0]['amount']}) if applicable."
    }, indent=2) if top_grants else json.dumps({"message": "No matching grants found."})


@tool("analyze_competitors")
def analyze_competitors(market_segment: str) -> str:
    """Analyze competitors in a given market segment.
    
    Use this to identify competing projects and their strengths/weaknesses.
    """
    competitors = [
        {
            "name": "LaunchpadXYZ",
            "type": "Direct Competitor",
            "strengths": ["Established user base", "Multi-chain support"],
            "weaknesses": ["No AI features", "Manual curation", "High fees"],
            "market_share_pct": 28,
        },
        {
            "name": "AgentForge",
            "type": "Direct Competitor",
            "strengths": ["Good agent framework", "Active community"],
            "weaknesses": ["No launchpad integration", "No blockchain features", "Steep learning curve"],
            "market_share_pct": 15,
        },
        {
            "name": "TokenMint Pro",
            "type": "Indirect Competitor",
            "strengths": ["Easy token creation", "Audited contracts"],
            "weaknesses": ["No AI research", "No opportunity discovery", "Static templates"],
            "market_share_pct": 22,
        },
        {
            "name": "DeployBot",
            "type": "Potential Partner",
            "strengths": ["Automated deployments", "Multi-chain support"],
            "weaknesses": ["No idea generation", "No content creation"],
            "market_share_pct": 10,
        },
    ]

    gap_analysis = [
        f"Gap: No existing product combines AI-powered research with automated launchpad deployment in {market_segment}",
        f"Gap: Competitors lack multi-agent orchestration for end-to-end product creation",
        f"Gap: Zero competitors offer integrated OKX ASP listing workflow",
    ]

    return json.dumps({
        "segment": market_segment,
        "competitors": competitors,
        "total_addressable_market": "$2.4B",
        "your_opportunity": f"There is a clear gap for an AI-native, end-to-end Agentic Service Provider in {market_segment}",
        "gaps": gap_analysis,
        "entry_strategy": "Differentiate with autonomous multi-agent workflow + OKX testnet integration + ASP readiness."
    }, indent=2)


@tool("find_target_audience")
def find_target_audience(project_idea: str) -> str:
    """Find and profile target audiences for a project idea.
    
    Use this to identify who would use the product and how to reach them.
    """
    audiences = [
        {
            "segment": "Web3 Entrepreneurs",
            "size": "~500K globally",
            "pain_point": "Need to rapidly prototype and launch token projects without dev teams",
            "channels": ["Twitter/X", "Warpcast", "Telegram dev groups"],
        },
        {
            "segment": "Hackathon Participants",
            "size": "~100K per major event",
            "pain_point": "Need tools to move from idea to MVP within 48 hours",
            "channels": ["Devpost", "ETHGlobal", "OKX Hackathons"],
        },
        {
            "segment": "DAO Tool Builders",
            "size": "~50K active builders",
            "pain_point": "Need to research governance models and deploy PoCs quickly",
            "channels": ["Discord DAO communities", "Governance forums"],
        },
        {
            "segment": "AI x Crypto Researchers",
            "size": "~200K early adopters",
            "pain_point": "Need to bridge AI capabilities with on-chain automation",
            "channels": ["ResearchGate", "arXiv", "AI x Crypto Twitter"],
        },
    ]
    return json.dumps({
        "project": project_idea,
        "audiences": audiences,
        "go_to_market": "Launch on Product Hunt + OKX ecosystem + crypto Twitter with demo videos",
    }, indent=2)
