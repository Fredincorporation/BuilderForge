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


@router.post("/launchpad/simulate")
async def simulate_launchpad_deployment(request: dict) -> dict:
    """
    Simulate contract compilation and deployment on OKX X Layer Testnet (Chain ID 195).
    
    Request body:
    - project_id: str (optional)
    - title: str (optional)
    - token_symbol: str (optional)
    - wallet_address: str (optional)
    
    Returns: Complete deployment simulation results with gas used, tx_hash, contract_address, and terminal logs.
    """
    try:
        import random
        import secrets
        from datetime import datetime
        from utils.db import db_get_project_by_id

        project_id = request.get("project_id")
        proj = db_get_project_by_id(project_id) if project_id else None
        
        project_title = request.get("title") or (proj.get("title") if proj else "OKX ASP Project")
        assets = proj.get("launch_assets", {}) if proj else {}
        token_symbol = request.get("token_symbol") or assets.get("token_symbol") or "FORGE"
        
        # Generated or existing contract/tx addresses
        contract_addr = (proj.get("deployment_plan", {}).get("contract_address") if proj else None) or ("0x" + secrets.token_hex(20))
        tx_hash = (proj.get("deployment_plan", {}).get("tx_hash") if proj else None) or ("0x" + secrets.token_hex(32))
        gas_used = f"0.00{random.randint(3800, 5200)} OKT"
        block_num = random.randint(14890000, 14920000)

        logs = [
            f"[0.0s] Initializing Solc v0.8.24 compiler engine...",
            f"[0.2s] Parsing Solidity source code for '{project_title}' ({token_symbol}Token.sol)...",
            f"[0.4s] Optimization pass (runs=200, evmVersion=shanghai) - 0 errors, 0 warnings",
            f"[0.7s] Connecting to OKX X Layer Testnet RPC (https://testrpc.xlayer.tech)...",
            f"[0.9s] Verified Network: OKX X Layer Testnet (Chain ID: 195)",
            f"[1.2s] Estimating deployment gas limit: {random.randint(135000, 168000)} gas units",
            f"[1.5s] Submitting transaction to OKX X Layer memory pool...",
            f"[1.8s] Block #{block_num} confirmed (1.2s block finality)",
            f"[2.0s] Contract deployed successfully at address: {contract_addr}",
            f"[2.1s] Verified ASP manifest compatibility for OKX.AI listing.",
        ]

        result = {
            "status": "success",
            "simulation": {
                "project_id": project_id,
                "project_title": project_title,
                "token_symbol": token_symbol,
                "contract_address": contract_addr,
                "tx_hash": tx_hash,
                "gas_used": gas_used,
                "network": "OKX X Layer Testnet",
                "chain_id": 195,
                "status": "CONFIRMED",
                "explorer_url": f"https://www.okx.com/explorer/xlayer-test/tx/{tx_hash}",
                "timestamp": datetime.now().isoformat(),
                "logs": logs,
            }
        }

        # If project exists in DB, update deployment_plan field
        if proj:
            if "deployment_plan" not in proj or not isinstance(proj["deployment_plan"], dict):
                proj["deployment_plan"] = {}
            proj["deployment_plan"]["contract_address"] = contract_addr
            proj["deployment_plan"]["tx_hash"] = tx_hash
            proj["deployment_plan"]["gas_used_okt"] = gas_used
            proj["deployment_plan"]["status"] = "CONFIRMED"
            proj["deployment_plan"]["network"] = "OKX X Layer Testnet"
            proj["deployment_plan"]["chain_id"] = 195
            from utils.db import db_save_project
            db_save_project(proj)

        return result

    except Exception as e:
        logger.error(f"Error simulating deployment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

