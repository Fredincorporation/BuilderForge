"""Wallet & Blockchain Endpoints.

Routes for wallet management and OKX testnet simulation.
"""

from __future__ import annotations

import logging
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory wallet storage (replace with database in production)
_wallet_db: dict[str, dict] = {}


# ============================================================================
# Endpoints
# ============================================================================
@router.post("/wallet/connect")
async def connect_wallet(request: dict) -> dict:
    """
    Connect and validate a wallet address.
    
    Request body:
    - address: str (required, OKX wallet address)
    - chain: str (optional, default: "okc")
    
    Returns: Wallet info
    """
    try:
        address = request.get("address", "").strip()
        chain = request.get("chain", "okc").strip().lower()
        
        if not address:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="address is required"
            )
        
        # Basic OKX address validation (starts with 0x, 42 chars)
        if not address.startswith("0x") or len(address) != 42:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OKX wallet address format"
            )
        
        _wallet_db["current"] = {
            "address": address,
            "chain": chain,
            "connected": True,
            "balance": 0.0,  # Simulated
            "connected_at": datetime.now().isoformat(),
        }
        
        logger.info(f"Wallet connected: {address[:10]}... on {chain}")
        
        return {
            "status": "success",
            "message": "Wallet connected",
            "wallet": _wallet_db["current"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error connecting wallet: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/wallet")
async def get_wallet() -> dict:
    """
    Get current connected wallet info.
    
    Returns: Wallet object or empty if not connected
    """
    try:
        if "current" not in _wallet_db:
            return {
                "status": "success",
                "connected": False,
                "message": "No wallet connected"
            }
        
        return {
            "status": "success",
            "connected": True,
            "wallet": _wallet_db["current"]
        }
    
    except Exception as e:
        logger.error(f"Error fetching wallet: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/wallet/disconnect")
async def disconnect_wallet() -> dict:
    """
    Disconnect the current wallet.
    
    Returns: Success message
    """
    try:
        if "current" in _wallet_db:
            address = _wallet_db["current"]["address"]
            del _wallet_db["current"]
            logger.info(f"Wallet disconnected: {address[:10]}...")
        
        return {
            "status": "success",
            "message": "Wallet disconnected"
        }
    
    except Exception as e:
        logger.error(f"Error disconnecting wallet: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/wallet/simulate")
async def simulate_transaction(request: dict) -> dict:
    """
    Simulate a transaction on OKX testnet.
    
    Request body:
    - to: str (recipient address)
    - value: str (amount in OKT)
    - data: str (optional, contract data)
    
    Returns: Simulation result with gas estimate
    """
    try:
        if "current" not in _wallet_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No wallet connected"
            )
        
        to_addr = request.get("to", "").strip()
        value = request.get("value", "0").strip()
        
        if not to_addr:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="to address is required"
            )
        
        # Simulate gas calculation
        base_gas = 21000
        value_float = float(value)
        estimated_gas = base_gas + int(value_float * 1000)
        gas_price = 0.5  # Simulated gwei
        
        simulation = {
            "status": "simulated_success",
            "from": _wallet_db["current"]["address"],
            "to": to_addr,
            "value": value,
            "gas": estimated_gas,
            "gas_price": gas_price,
            "total_cost": (estimated_gas * gas_price) / 1e9,
            "chain": _wallet_db["current"]["chain"],
        }
        
        logger.info(f"Simulated transaction: {to_addr[:10]}... value={value} OKT")
        
        return {
            "status": "success",
            "simulation": simulation
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error simulating transaction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/wallet/gas-estimate")
async def estimate_gas(to: Optional[str] = None, value: Optional[str] = None) -> dict:
    """
    Estimate gas for a transaction.
    
    Query parameters:
    - to: str (recipient address)
    - value: str (amount in OKT)
    
    Returns: Gas estimate in OKT
    """
    try:
        value_float = float(value or "0")
        
        # Simulated gas calculation
        base_gas = 21000
        estimated_gas = base_gas + int(value_float * 1000)
        gas_price = 0.5  # Simulated gwei
        total_cost = (estimated_gas * gas_price) / 1e9
        
        return {
            "status": "success",
            "estimate": {
                "gas": estimated_gas,
                "gas_price": gas_price,
                "total_cost_okt": total_cost,
            }
        }
    
    except Exception as e:
        logger.error(f"Error estimating gas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
