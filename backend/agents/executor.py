"""BuilderForge Executor Agent (OKX X Layer On-Chain Execution)."""

from __future__ import annotations

import logging
from typing import Dict, Any

try:
    from tools.okx_tools import simulate_okx_deployment, estimate_okx_gas
except ImportError:
    from ..tools.okx_tools import simulate_okx_deployment, estimate_okx_gas

logger = logging.getLogger(__name__)


class ExecutorAgent:
    """Agent responsible for OKX wallet interactions, gas estimation, and contract deployment simulation."""

    def __init__(self, mode: str = "SIMULATED"):
        self.mode = mode

    def run(self, project_title: str, smart_contract_code: str) -> Dict[str, Any]:
        """Execute deployment simulation on OKX X Layer Testnet."""
        logger.info(f"[Executor Agent] Deploying smart contract for '{project_title}' on OKX X Layer Testnet...")
        
        deployment_res = simulate_okx_deployment(project_title, smart_contract_code, chain_id=195)
        gas_est = estimate_okx_gas()
        
        return {
            "chain_id": deployment_res["chain_id"],
            "network_name": deployment_res["network_name"],
            "contract_address": deployment_res["contract_address"],
            "tx_hash": deployment_res["tx_hash"],
            "gas_used_okt": deployment_res["gas_used_okt"],
            "estimated_fee_okt": gas_est["estimated_fee_okt"],
            "deployment_status": deployment_res["deployment_status"],
            "explorer_url": deployment_res["explorer_url"],
            "rpc_logs": deployment_res["rpc_logs"],
        }
