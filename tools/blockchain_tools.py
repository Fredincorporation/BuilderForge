"""Blockchain Tools for BuilderForge.

Provides blockchain simulation, OKX testnet interaction,
and smart contract deployment planning tools.
"""

from __future__ import annotations

import json
from typing import Any
from langchain.tools import tool

from utils.okx_integration import (
    connect_wallet,
    estimate_gas,
    sign_transaction,
    simulate_contract_deploy,
    simulate_token_mint,
    simulate_transaction_sequence,
    submit_asp_listing,
    get_asp_status,
    build_asp_manifest,
    get_web3_client,
    is_real_rpc_enabled,
)


@tool("connect_okx_wallet")
def connect_okx_wallet() -> str:
    """Connect to OKX Web3 wallet or RPC provider.

    Connects to an OKX wallet or queries live RPC on OKC / X Layer testnet.
    Returns wallet address, network chain ID, latest block number, and balance.
    """
    result = connect_wallet()
    return json.dumps(result, indent=2)


@tool("deploy_smart_contract")
def deploy_smart_contract(contract_name: str, contract_code: str, deployer_address: str, confirm_broadcast: bool = False) -> str:
    """Deploy a smart contract on the OKC testnet.

    Simulates deploying an ERC-20 token contract.
    Gated behind operator confirmation (confirm_broadcast=True) when real RPC is active.
    Returns contract address and transaction details.
    """
    if is_real_rpc_enabled() and not confirm_broadcast:
        result = {
            "status": "AWAITING_OPERATOR_CONFIRMATION",
            "message": "Real RPC mode active on OKX X Layer. Pass confirm_broadcast=True to broadcast on-chain transaction.",
            "contract_name": contract_name,
            "deployer": deployer_address,
            "simulated_preview": simulate_contract_deploy(contract_name, contract_code, deployer_address),
        }
        return json.dumps(result, indent=2)

    result = simulate_contract_deploy(contract_name, contract_code, deployer_address)
    return json.dumps(result, indent=2)


@tool("mint_tokens")
def mint_tokens(token_address: str, to_address: str, amount: int) -> str:
    """Mint tokens on OKC testnet.

    Simulates minting tokens to a specified address.
    """
    result = simulate_token_mint(token_address, to_address, amount)
    return json.dumps(result, indent=2)


@tool("estimate_gas")
def estimate_gas_tool(operation: str, chain: str = "OKC") -> str:
    """Estimate gas costs for common contract operations.

    Provides gas estimates for token operations on various chains.
    """
    result = estimate_gas(operation, chain)
    return json.dumps(result, indent=2)


@tool("simulate_transaction_sequence")
def simulate_transaction_sequence_tool(project_name: str, deployer: str) -> str:
    """Simulate a full transaction sequence for launching a token project.

    Creates a realistic sequence of on-chain actions for demo purposes.
    """
    result = simulate_transaction_sequence(project_name, deployer)
    return json.dumps(result, indent=2)


@tool("sign_transaction")
def sign_transaction_tool(from_address: str, to_address: str, value: str = "0", gas_used: int = 21000, gas_price_gwei: float = 0.001) -> str:
    """Sign and broadcast a transaction."""
    tx_data = {
        "from": from_address,
        "to": to_address,
        "value": value,
        "gas_used": gas_used,
        "gas_price_gwei": gas_price_gwei,
    }
    result = sign_transaction(tx_data)
    return json.dumps(result, indent=2)


@tool("submit_asp_listing")
def submit_asp_listing_tool(agent_name: str, description: str, contact_email: str) -> str:
    """Build and submit an ASP manifest to OKX.AI marketplace directory."""
    manifest = build_asp_manifest(
        agent_name=agent_name,
        description=description,
        capabilities=["Market Intelligence", "Tokenomics Generation", "Smart Contract Deployment", "ASP Listing"],
        pricing_model="pay_per_job",
        contact_email=contact_email,
    )
    result = submit_asp_listing(manifest)
    return json.dumps(result, indent=2)
