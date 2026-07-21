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
)


@tool("connect_okx_wallet")
def connect_okx_wallet() -> str:
    """Connect to OKX Web3 wallet.

    Simulates connecting to an OKX wallet on OKC testnet.
    Returns wallet address and balance.
    """
    result = connect_wallet()
    return json.dumps(result, indent=2)


@tool("deploy_smart_contract")
def deploy_smart_contract(contract_name: str, contract_code: str, deployer_address: str) -> str:
    """Deploy a smart contract on the OKC testnet.

    Simulates deploying an ERC-20 token contract.
    Returns contract address and transaction details.
    """
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
    """Sign and broadcast a simulated transaction."""
    tx_data = {
        "from": from_address,
        "to": to_address,
        "value": value,
        "gas_used": gas_used,
        "gas_price_gwei": gas_price_gwei,
    }
    result = sign_transaction(tx_data)
    return json.dumps(result, indent=2)
