"""LaunchPad Endpoints.

Routes for upcoming launches and marketplace listings.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)
router = APIRouter()

# Mock launchpad data
MOCK_LAUNCHES = [
    {
        "id": "launch_001",
        "title": "TokenX on OKX",
        "description": "New token launching on OKX ASP",
        "launch_date": "2026-08-15",
        "status": "upcoming",
        "category": "token",
        "tags": ["Token", "OKX", "ASP"],
    },
    {
        "id": "launch_002",
        "title": "DeFi Protocol V2",
        "description": "Major upgrade with new features",
        "launch_date": "2026-08-22",
        "status": "upcoming",
        "category": "protocol",
        "tags": ["DeFi", "Protocol", "Upgrade"],
    },
    {
        "id": "launch_003",
        "title": "NFT Collection Premiere",
        "description": "Limited edition AI-generated NFTs",
        "launch_date": "2026-08-01",
        "status": "live",
        "category": "nft",
        "tags": ["NFT", "AI", "Collection"],
    },
]


# ============================================================================
# Endpoints
# ============================================================================
@router.get("/launchpad")
async def list_launches(status_filter: str = "upcoming") -> dict:
    """
    List all launches on LaunchPad.
    
    Query parameters:
    - status_filter: str (optional, "upcoming", "live", or "all")
    
    Returns: Array of launch objects
    """
    try:
        if status_filter == "all":
            launches = MOCK_LAUNCHES
        else:
            launches = [l for l in MOCK_LAUNCHES if l["status"] == status_filter]
        
        return {
            "status": "success",
            "count": len(launches),
            "launches": launches
        }
    
    except Exception as e:
        logger.error(f"Error listing launches: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/launchpad/{launch_id}")
async def get_launch(launch_id: str) -> dict:
    """
    Get a specific launch by ID.
    
    Path parameters:
    - launch_id: str
    
    Returns: Launch object
    """
    try:
        launch = next((l for l in MOCK_LAUNCHES if l["id"] == launch_id), None)
        
        if not launch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Launch {launch_id} not found"
            )
        
        return {
            "status": "success",
            "launch": launch
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching launch {launch_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
