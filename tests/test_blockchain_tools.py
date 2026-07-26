"""Unit tests for Blockchain Tools module."""

from __future__ import annotations

import json
import unittest

from tools.blockchain_tools import (
    connect_okx_wallet,
    deploy_smart_contract,
    mint_tokens,
    estimate_gas_tool,
    simulate_transaction_sequence_tool,
    submit_asp_listing_tool,
)


def _exec_tool(tool_obj, *args, **kwargs):
    """Helper to execute a tool function directly."""
    if hasattr(tool_obj, "func") and callable(getattr(tool_obj, "func")):
        return tool_obj.func(*args, **kwargs)
    return tool_obj(*args, **kwargs)


class TestBlockchainTools(unittest.TestCase):
    """Test suite for tools/blockchain_tools.py."""

    def test_connect_okx_wallet_tool(self):
        raw_res = _exec_tool(connect_okx_wallet)
        data = json.loads(raw_res) if isinstance(raw_res, str) else raw_res
        self.assertIn("address", data)
        self.assertIn("chain_id", data)

    def test_deploy_smart_contract_tool(self):
        raw_res = _exec_tool(
            deploy_smart_contract,
            "MyToken",
            "pragma solidity ^0.8.20; contract MyToken {}",
            "0x1234567890123456789012345678901234567890"
        )
        data = json.loads(raw_res) if isinstance(raw_res, str) else raw_res
        if data.get("status") == "AWAITING_OPERATOR_CONFIRMATION":
            self.assertEqual(data["contract_name"], "MyToken")
            self.assertIn("simulated_preview", data)
        else:
            self.assertEqual(data["contract_name"], "MyToken")
            self.assertIn("contract_address", data)

    def test_mint_tokens_tool(self):
        raw_res = _exec_tool(
            mint_tokens,
            "0x1111111111111111111111111111111111111111",
            "0x2222222222222222222222222222222222222222",
            5000
        )
        data = json.loads(raw_res) if isinstance(raw_res, str) else raw_res
        self.assertTrue(data.get("success", False))
        self.assertEqual(data["amount"], 5000)

    def test_estimate_gas_tool(self):
        raw_res = _exec_tool(estimate_gas_tool, "deploy_token", "OKC")
        data = json.loads(raw_res) if isinstance(raw_res, str) else raw_res
        self.assertIn("estimate", data)

    def test_simulate_transaction_sequence_tool(self):
        raw_res = _exec_tool(
            simulate_transaction_sequence_tool,
            "Test Project",
            "0x1234567890123456789012345678901234567890"
        )
        data = json.loads(raw_res) if isinstance(raw_res, str) else raw_res
        self.assertEqual(data["project"], "Test Project")
        self.assertIn("steps", data)

    def test_submit_asp_listing_tool(self):
        raw_res = _exec_tool(
            submit_asp_listing_tool,
            "Test ASP Tool Agent",
            "ASP agent for testing",
            "asp_test@builderforge.ai"
        )
        data = json.loads(raw_res) if isinstance(raw_res, str) else raw_res
        self.assertTrue(data.get("success", False))
        self.assertIn("asp_id", data)


if __name__ == "__main__":
    unittest.main()
