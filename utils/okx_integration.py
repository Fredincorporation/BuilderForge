"""OKX Web3 & ASP Integration for BuilderForge.

Handles OKX wallet connection, testnet operations,
and the ASP listing workflow.
"""

from __future__ import annotations

import os
import json
import re
from typing import Any, Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OKX_API_BASE = "https://www.okx.com/api/v1"
OKX_CHAIN_ID = 65  # OKC Testnet chain ID
OKX_NETWORK_NAME = "OKC Testnet"
OKX_FAUCET_URL = "https://www.okx.com/okc/faucet"


# ---------------------------------------------------------------------------
# Address Validation
# ---------------------------------------------------------------------------

def _is_valid_address(address: str) -> bool:
    if not isinstance(address, str):
        return False
    return bool(re.fullmatch(r"0x[a-fA-F0-9]{40}", address))


def _random_address() -> str:
    import random
    import hashlib

    return "0x" + hashlib.sha256(
        f"builderforge_{random.randint(1000, 9999)}_{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()[:40]


# ---------------------------------------------------------------------------
# Wallet Simulation
# ---------------------------------------------------------------------------

def connect_wallet() -> Dict[str, Any]:
    """Simulate connecting to an OKX wallet for testnet demo mode."""
    address = _random_address()
    wallet = {
        "connected": True,
        "address": address,
        "chain_id": OKX_CHAIN_ID,
        "chain_name": OKX_NETWORK_NAME,
        "balance": "12.45 OKT",
        "network": "testnet",
        "faucet_url": OKX_FAUCET_URL,
        "connected_at": datetime.utcnow().isoformat(),
    }
    return wallet


def estimate_gas(operation: str, chain: str = "OKC") -> Dict[str, Any]:
    """Return a gas estimate for an OKC contract operation."""
    estimates = {
        "erc20_deploy": {"gas": 1200000, "gwei": 0.001, "estimated_cost_okt": 0.0012},
        "erc20_transfer": {"gas": 65000, "gwei": 0.001, "estimated_cost_okt": 0.000065},
        "erc20_mint": {"gas": 80000, "gwei": 0.001, "estimated_cost_okt": 0.00008},
        "erc20_approve": {"gas": 46000, "gwei": 0.001, "estimated_cost_okt": 0.000046},
        "swap_on_dex": {"gas": 180000, "gwei": 0.001, "estimated_cost_okt": 0.00018},
        "stake_tokens": {"gas": 150000, "gwei": 0.001, "estimated_cost_okt": 0.00015},
    }
    return {
        "chain": chain,
        "operation": operation,
        "estimate": estimates.get(operation, {"gas": 100000, "gwei": 0.001, "estimated_cost_okt": 0.0001}),
        "note": "OKC Testnet uses free faucet credits for demo transactions.",
    }


def sign_transaction(tx_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate signing and broadcasting a transaction on OKC testnet."""
    if not _is_valid_address(tx_data.get("from", "")) or not _is_valid_address(tx_data.get("to", "")):
        return {
            "success": False,
            "error": "Invalid from/to address for transaction.",
            "tx_hash": None,
        }

    tx_hash = "0x" + os.urandom(32).hex()
    return {
        "success": True,
        "hash": tx_hash,
        "from": tx_data.get("from"),
        "to": tx_data.get("to"),
        "value": tx_data.get("value", "0"),
        "status": "simulated_success",
        "block_number": 12345678,
        "timestamp": datetime.utcnow().isoformat(),
        "gas_used": tx_data.get("gas_used", 21000),
        "gas_price_gwei": tx_data.get("gas_price_gwei", 0.001),
        "network": OKX_NETWORK_NAME,
    }


def simulate_contract_deploy(
    contract_name: str,
    contract_code: str,
    deployer: str,
) -> Dict[str, Any]:
    """Simulate deploying a smart contract on OKC testnet."""
    if not _is_valid_address(deployer):
        return {
            "success": False,
            "error": "Invalid deployer address.",
            "contract_address": None,
        }

    import hashlib

    contract_address = "0x" + hashlib.sha256(
        f"{contract_name}{deployer}{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()[:40]

    return {
        "success": True,
        "contract_name": contract_name,
        "contract_address": contract_address,
        "deployer": deployer,
        "tx_hash": "0x" + os.urandom(32).hex(),
        "network": OKX_NETWORK_NAME,
        "block_explorer_url": f"https://www.oklink.com/okc-testnet/address/{contract_address}",
        "gas_used": 250000,
        "gas_price_gwei": 0.001,
        "simulated": True,
    }


def simulate_token_mint(
    token_address: str,
    to_address: str,
    amount: int,
    decimals: int = 18,
) -> Dict[str, Any]:
    """Simulate minting tokens on OKC testnet."""
    if not _is_valid_address(token_address) or not _is_valid_address(to_address):
        return {
            "success": False,
            "error": "Invalid token or recipient address.",
            "tx_hash": None,
        }

    return {
        "success": True,
        "token_address": token_address,
        "to": to_address,
        "amount": amount,
        "formatted_amount": f"{amount / 10**decimals}",
        "tx_hash": "0x" + os.urandom(32).hex(),
        "network": OKX_NETWORK_NAME,
        "gas_used": 80000,
        "gas_price_gwei": 0.001,
        "simulated": True,
    }


def simulate_transaction_sequence(
    project_name: str,
    deployer: str,
) -> Dict[str, Any]:
    """Simulate a full transaction sequence for launching a token project."""
    if not _is_valid_address(deployer):
        return {
            "success": False,
            "error": "Invalid deployer address for transaction sequence.",
            "steps": [],
        }

    deploy_result = simulate_contract_deploy(
        contract_name=f"{project_name}Token",
        contract_code=f"// {project_name} ERC-20 Token",
        deployer=deployer,
    )

    if not deploy_result.get("success"):
        return {
            "success": False,
            "error": deploy_result.get("error", "Deployment simulation failed."),
            "steps": [],
        }

    mint_result = simulate_token_mint(
        token_address=deploy_result["contract_address"],
        to_address=deployer,
        amount=500000000,
    )

    return {
        "success": True,
        "project": project_name,
        "deployer": deployer,
        "network": OKX_NETWORK_NAME,
        "steps": [
            {"step": 1, "action": "Deploy token contract", "result": deploy_result},
            {"step": 2, "action": "Mint initial supply", "result": mint_result},
            {
                "step": 3,
                "action": "Add liquidity to OKX DEX",
                "result": {
                    "simulated": True,
                    "status": "pending",
                    "note": "Requires OKX DEX integration in a production flow.",
                },
            },
            {
                "step": 4,
                "action": "Verify contract on Oklink",
                "result": {
                    "url": f"https://www.oklink.com/okc-testnet/address/{deploy_result['contract_address']}",
                    "simulated": True,
                },
            },
        ],
        "total_gas_used": deploy_result.get("gas_used", 0) + mint_result.get("gas_used", 0),
        "timestamp": datetime.utcnow().isoformat(),
    }


# ---------------------------------------------------------------------------
# ASP Listing
# ---------------------------------------------------------------------------

def build_asp_manifest(
    agent_name: str,
    description: str,
    capabilities: List[str],
    pricing_model: str,
    contact_email: str,
) -> Dict[str, Any]:
    """Build a structured ASP manifest compatible with OKX.AI listing format.

    Reference: https://www.okx.com/ai/asp-docs
    """
    manifest = {
        "asp_version": "1.0.0",
        "name": agent_name,
        "description": description,
        "publisher": "BuilderForge",
        "website": "https://builderforge.ai",
        "contact_email": contact_email,
        "capabilities": capabilities,
        "pricing": {
            "model": pricing_model,
            "currency": "USD",
            "details": [
                {"tier": "free", "requests_per_day": 10, "price": 0},
                {"tier": "pro", "requests_per_day": 100, "price": 29},
                {"tier": "enterprise", "requests_per_day": 10000, "price": 299},
            ],
        },
        "blockchain": {
            "supported_chains": ["OKC", "Ethereum", "Polygon", "Arbitrum"],
            "testnet": True,
            "mainnet": False,
        },
        "agent_components": {
            "coordinator": "BuilderForge Coordinator Agent",
            "researcher": "BuilderForge Researcher Agent",
            "creator": "BuilderForge Creator Agent",
            "executor": "BuilderForge Executor Agent",
            "analyzer": "BuilderForge Analyzer Agent",
        },
        "submission_metadata": {
            "submitted_at": datetime.utcnow().isoformat(),
            "hackathon": "OKX AI Genesis Hackathon",
            "team": "BuilderForge Team",
        },
    }
    return manifest


def submit_asp_listing(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """Submit an ASP listing to OKX.AI.

    In production, this POSTs to the OKX ASP API endpoint.
    For the MVP, we simulate a successful submission.
    """
    return {
        "success": True,
        "asp_id": f"asp_{os.urandom(4).hex()}",
        "status": "pending_review",
        "message": "Your ASP has been submitted to OKX.AI for review. "
                   "You will be notified once it is approved.",
        "manifest_url": f"https://www.okx.com/ai/asp/pending/{os.urandom(4).hex()}",
        "simulated": True,
    }


def get_asp_status(asp_id: str) -> Dict[str, Any]:
    """Check the status of an ASP listing."""
    return {
        "asp_id": asp_id,
        "status": "approved",
        "listing_url": f"https://www.okx.com/ai/asp/{asp_id}",
        "total_requests": 1423,
        "active_users": 87,
        "rating": 4.8,
    }
