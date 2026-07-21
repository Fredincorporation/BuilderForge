"""DealFlow Endpoints.

Routes for opportunities and deal management.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)
router = APIRouter()

# Mock dealflow data
MOCK_DEALS = [
    {
        "id": "deal_001",
        "title": "OKX AI Agent Framework",
        "description": "A framework for building AI agents on OKX",
        "status": "active",
        "funding_stage": "Series A",
        "tags": ["AI", "OKX", "Web3"],
    },
    {
        "id": "deal_002",
        "title": "DeFi Automation Platform",
        "description": "Automated trading and liquidity management",
        "status": "active",
        "funding_stage": "Seed",
        "tags": ["DeFi", "Trading", "Automation"],
    },
    {
        "id": "deal_003",
        "title": "NFT Marketplace Plus",
        "description": "Enhanced NFT trading with AI curation",
        "status": "closed",
        "funding_stage": "Series B",
        "tags": ["NFT", "Marketplace", "AI"],
    },
]


# ============================================================================
# Endpoints
# ============================================================================
@router.get("/dealflow")
async def list_deals(status_filter: str = "active") -> dict:
    """
    List all available deals.
    
    Query parameters:
    - status_filter: str (optional, "active", "closed", or "all")
    
    Returns: Array of deal objects
    """
    try:
        if status_filter == "all":
            deals = MOCK_DEALS
        else:
            deals = [d for d in MOCK_DEALS if d["status"] == status_filter]
        
        return {
            "status": "success",
            "count": len(deals),
            "deals": deals
        }
    
    except Exception as e:
        logger.error(f"Error listing deals: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/dealflow/{deal_id}")
async def get_deal(deal_id: str) -> dict:
    """
    Get a specific deal by ID.
    
    Path parameters:
    - deal_id: str
    
    Returns: Deal object
    """
    try:
        deal = next((d for d in MOCK_DEALS if d["id"] == deal_id), None)
        
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
