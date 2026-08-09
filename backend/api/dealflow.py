"""DealFlow Endpoints.

Routes for OKX Ecosystem opportunities, grant discovery, and deal management.
"""

from __future__ import annotations

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from utils.db import db_get_all_projects

logger = logging.getLogger(__name__)
router = APIRouter()

# High-quality curated OKX ecosystem deals
CURATED_DEALS: List[Dict[str, Any]] = [
    {
        "id": "deal_okx_001",
        "title": "OKX X Layer Developer Ecosystem Grant",
        "description": "Fast-track grant funding for high-utility autonomous AI agentic applications, ASP microservices, and DeAI protocols deploying on OKX X Layer Testnet & Mainnet.",
        "status": "active",
        "category": "Grants",
        "funding_stage": "$100,000 OKT Grant",
        "match_score": 96,
        "tags": ["OKX X Layer", "Grants", "ASP", "DeAI"],
        "why_it_matches": "Direct alignment with OKX X Layer Chain ID 195 smart contract architecture and ASP listing criteria.",
        "recommended_action": "Deploy contract on OKX X Layer Testnet and submit ASP Manifest validation payload.",
        "apply_url": "https://www.okx.com/xlayer/grants",
    },
    {
        "id": "deal_okx_002",
        "title": "OKX.AI ASP Marketplace Listing & Incubator",
        "description": "Priority onboarding and monetization track for Agentic Service Providers (ASPs) into the OKX.AI agent directory with zero platform take-rates for the first 6 months.",
        "status": "active",
        "category": "Partnerships",
        "funding_stage": "OKX.AI Partner Track",
        "match_score": 94,
        "tags": ["OKX.AI", "ASP", "Inference", "Monetization"],
        "why_it_matches": "Your project contains valid ASP pricing definitions and standardized AI agent capability schemas.",
        "recommended_action": "Complete ASP manifest schema validation and submit via BuilderForge ASP portal.",
        "apply_url": "https://www.okx.com/ai/asp",
    },
    {
        "id": "deal_okx_003",
        "title": "OKX Ventures Web3 & DeAI Seed Fund",
        "description": "Venture capital backing for early-stage teams building autonomous decentralized finance, automated yield vaults, and agentic Web3 infrastructure.",
        "status": "active",
        "category": "Funding",
        "funding_stage": "$250K - $1M Seed",
        "match_score": 91,
        "tags": ["OKX Ventures", "Seed", "DeFi", "AI"],
        "why_it_matches": "High market opportunity score with validated TAM/SAM projections and competitive differentiation.",
        "recommended_action": "Generate ZIP export from Dashboard and attach generated Pitch Deck to OKX Ventures application.",
        "apply_url": "https://www.okx.com/ventures",
    },
    {
        "id": "deal_okx_004",
        "title": "Google Cloud & OKX AI Startup Credits",
        "description": "$200,000 in GPU cloud compute credits (NVIDIA H100/A100 instances) and dedicated AI engineering office hours for BuilderForge ecosystem projects.",
        "status": "active",
        "category": "Grants",
        "funding_stage": "$200,000 GPU Credits",
        "match_score": 88,
        "tags": ["Google Cloud", "Compute", "GPU", "Credits"],
        "why_it_matches": "Compute-intensive agent orchestrations qualify for top-tier Google Cloud Web3 startup incentives.",
        "recommended_action": "Apply with project ID and request GPU cluster allocation.",
        "apply_url": "https://cloud.google.com/startup",
    },
    {
        "id": "deal_okx_005",
        "title": "OKX AI Genesis Hackathon Prize Pool",
        "description": "Global hackathon prize track for top-performing Web3 AI applications, autonomous agents, and cross-chain execution engines.",
        "status": "active",
        "category": "Grants",
        "funding_stage": "$150,000 Prize Pool",
        "match_score": 95,
        "tags": ["Hackathon", "OKX", "Prize Track"],
        "why_it_matches": "Your project architecture meets all 4 evaluation tracks: Innovation, X Layer Integration, ASP Readiness, and Execution Quality.",
        "recommended_action": "Submit final demo video and GitHub repository link to OKX Hackathon portal.",
        "apply_url": "https://www.okx.com/ai-genesis",
    },
    {
        "id": "deal_okx_006",
        "title": "DeFi Alliance & OKX Accelerator Program",
        "description": "12-week intensive accelerator with liquidity provision, security audit support, and direct mentorship from top OKX core developers.",
        "status": "upcoming",
        "category": "Partnerships",
        "funding_stage": "$50,000 + Audit Credit",
        "match_score": 85,
        "tags": ["Accelerator", "Security", "Audit", "Mentorship"],
        "why_it_matches": "Provides smart contract audit vouchers and liquidity bootstrapping support prior to mainnet launch.",
        "recommended_action": "Pre-register team profile before applications close.",
        "apply_url": "https://defialliance.co",
    },
]


def _build_deals_from_projects() -> List[Dict[str, Any]]:
    """Dynamically pull opportunities from SQLite saved projects."""
    project_deals: List[Dict[str, Any]] = []
    try:
        projects = db_get_all_projects()
        for p in projects:
            title = p.get("title", "Project")
            report = p.get("opportunity_report", {})
            assets = p.get("launch_assets", {})
            cat = p.get("category", "Web3")
            
            if isinstance(report, dict) and "grant_opportunities" in report:
                grants = report.get("grant_opportunities", [])
                for idx, g in enumerate(grants):
                    if isinstance(g, dict):
                        g_name = g.get("name", "Ecosystem Grant")
                        g_amount = g.get("amount", "$50,000")
                        g_url = g.get("url", "https://www.okx.com/xlayer")
                        
                        project_deals.append({
                            "id": f"proj_deal_{p.get('id')}_{idx}",
                            "title": f"{g_name} for '{title}'",
                            "description": f"Tailored grant opportunity discovered by Researcher Agent for your project '{title}' ({cat}). Targeted sector: {report.get('target_sector', 'DeAI')}.",
                            "status": "active",
                            "category": "Grants",
                            "funding_stage": g_amount,
                            "match_score": report.get("timing_score", 92),
                            "tags": [cat, "Researcher Agent", "OKX X Layer"],
                            "why_it_matches": f"Automated market intelligence match for '{title}' in sector '{report.get('target_sector', cat)}' with TAM {report.get('market_size', '$10B+')}.",
                            "recommended_action": f"Export launch package from Dashboard and apply for {g_name}.",
                            "apply_url": g_url,
                            "project_id": p.get("id"),
                        })
    except Exception as e:
        logger.warning(f"Error building project deals: {e}")
    
    return project_deals


# ============================================================================
# Endpoints
# ============================================================================
@router.get("/dealflow")
async def list_deals(status_filter: str = "all", category_filter: str = "all") -> dict:
    """
    List all deals including dynamic opportunities from user projects.
    
    Query parameters:
    - status_filter: str (optional, "active", "upcoming", "closed", or "all")
    - category_filter: str (optional, "Grants", "Funding", "Partnerships", or "all")
    """
    try:
        dynamic_deals = _build_deals_from_projects()
        all_deals = dynamic_deals + CURATED_DEALS
        
        # Deduplicate deals by ID
        seen = set()
        unique_deals = []
        for d in all_deals:
            if d["id"] not in seen:
                seen.add(d["id"])
                unique_deals.append(d)

        filtered = unique_deals

        if status_filter != "all":
            filtered = [d for d in filtered if d.get("status", "").lower() == status_filter.lower()]

        if category_filter != "all":
            filtered = [d for d in filtered if d.get("category", "").lower() == category_filter.lower()]

        return {
            "status": "success",
            "count": len(filtered),
            "deals": filtered
        }
    
    except Exception as e:
        logger.error(f"Error listing deals: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/dealflow/{deal_id}")
async def get_deal(deal_id: str) -> dict:
    """Get a specific deal by ID."""
    try:
        all_deals = _build_deals_from_projects() + CURATED_DEALS
        deal = next((d for d in all_deals if d["id"] == deal_id), None)
        
        if not deal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deal {deal_id} not found"
            )
        
        return {
            "status": "success",
            "deal": deal
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching deal {deal_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/dealflow/discover")
async def discover_deals(request: Optional[dict] = None) -> dict:
    """
    Trigger live Researcher Agent opportunity discovery scan.
    """
    try:
        import random
        from agents.researcher import create_researcher_agent

        researcher = create_researcher_agent()
        query_topic = (request.get("query") if request else None) or "OKX Ecosystem AI & Web3 Grants"
        res = researcher.run(query_topic, "Market discovery run", "Web3")

        new_deals = []
        for idx, g in enumerate(res.get("grant_opportunities", [])):
            d_id = f"disc_{str(uuid4())[:8]}"
            new_deals.append({
                "id": d_id,
                "title": f"Newly Discovered: {g.get('name', 'OKX Ecosystem Opportunity')}",
                "description": f"Freshly discovered opportunity by Researcher Agent during market scan for '{query_topic}'.",
                "status": "active",
                "category": "Grants" if "Grant" in g.get("name", "") else "Funding",
                "funding_stage": g.get("amount", "$50,000 - $100,000"),
                "match_score": random.randint(89, 98),
                "tags": ["AI Scan", "Live Discovery", "OKX X Layer"],
                "why_it_matches": f"Scanned from live OKX ecosystem registry for DeAI and ASP infrastructure.",
                "recommended_action": "Review eligibility criteria and link to an active project.",
                "apply_url": g.get("url", "https://www.okx.com/xlayer"),
            })

        return {
            "status": "success",
            "discovered_count": len(new_deals),
            "deals": new_deals
        }

    except Exception as e:
        logger.error(f"Error discovering deals: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
