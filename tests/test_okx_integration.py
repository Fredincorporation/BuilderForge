"""Unit tests for OKX Web3 and ASP Integration utilities."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch, MagicMock

from utils.okx_integration import (
    connect_wallet,
    build_asp_manifest,
    submit_asp_listing,
    get_asp_status,
    sanitize_dict,
    is_real_asp_enabled,
    is_real_rpc_enabled,
    _is_valid_address,
)


class TestOKXIntegration(unittest.TestCase):
    """Test suite for OKX Integration module."""

    def test_sanitize_dict(self):
        sensitive_data = {
            "api_key": "secret_key_123",
            "public_id": "user_456",
            "nested": {
                "secret_key": "pass_xyz",
                "normal": "value",
            },
        }
        sanitized = sanitize_dict(sensitive_data)
        self.assertEqual(sanitized["api_key"], "***REDACTED***")
        self.assertEqual(sanitized["public_id"], "user_456")
        self.assertEqual(sanitized["nested"]["secret_key"], "***REDACTED***")
        self.assertEqual(sanitized["nested"]["normal"], "value")

    def test_address_validation(self):
        self.assertTrue(_is_valid_address("0x1234567890123456789012345678901234567890"))
        self.assertFalse(_is_valid_address("invalid_address"))
        self.assertFalse(_is_valid_address("0x123"))

    def test_connect_wallet(self):
        wallet = connect_wallet()
        self.assertIn("address", wallet)
        self.assertIn("chain_id", wallet)
        self.assertIn("balance", wallet)
        self.assertTrue(wallet["address"].startswith("0x"))

    def test_build_asp_manifest(self):
        manifest = build_asp_manifest(
            agent_name="Test Agent",
            description="A test ASP agent",
            capabilities=["Testing", "Validation"],
            pricing_model="pay_per_job",
            contact_email="test@builderforge.ai",
        )
        self.assertEqual(manifest["asp_version"], "1.0.0")
        self.assertEqual(manifest["name"], "Test Agent")
        self.assertEqual(manifest["contact_email"], "test@builderforge.ai")
        self.assertIn("capabilities", manifest)
        self.assertIn("pricing", manifest)

    def test_submit_asp_listing_simulated(self):
        manifest = build_asp_manifest(
            agent_name="Simulated Agent",
            description="Testing ASP",
            capabilities=["Testing"],
            pricing_model="pay_per_job",
            contact_email="test@builderforge.ai",
        )
        with patch("utils.okx_integration.is_real_asp_enabled", return_value=False):
            res = submit_asp_listing(manifest)
            self.assertTrue(res["success"])
            self.assertIn("asp_id", res)
            self.assertEqual(res["status"], "pending_review")
            self.assertTrue(res["simulated"])

    def test_get_asp_status_simulated(self):
        with patch("utils.okx_integration.is_real_asp_enabled", return_value=False):
            res = get_asp_status("asp_12345")
            self.assertEqual(res["asp_id"], "asp_12345")
            self.assertEqual(res["status"], "approved")
            self.assertTrue(res["simulated"])

    @patch("requests.post")
    def test_submit_asp_listing_real_success(self, mock_post):
        manifest = build_asp_manifest(
            agent_name="Real Agent",
            description="Testing Real ASP",
            capabilities=["Testing"],
            pricing_model="pay_per_job",
            contact_email="real@builderforge.ai",
        )
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "code": "0",
            "data": [{"asp_id": "asp_real_777", "status": "approved", "listing_url": "https://www.okx.com/ai/asp/asp_real_777"}]
        }
        mock_post.return_value = mock_resp

        with patch("utils.okx_integration.is_real_asp_enabled", return_value=True):
            res = submit_asp_listing(manifest)
            self.assertTrue(res["success"])
            self.assertEqual(res["asp_id"], "asp_real_777")
            self.assertEqual(res["status"], "approved")
            self.assertFalse(res["simulated"])

    def test_generate_okx_headers(self):
        from utils.okx_integration import _generate_okx_headers
        with patch.dict(os.environ, {
            "OKX_API_KEY": "test_api_key",
            "OKX_SECRET_KEY": "test_secret_key",
            "OKX_PASSPHRASE": "test_passphrase",
            "OKX_PROJECT_ID": "test_project_123",
            "OKX_ENV": "testnet",
        }):
            headers = _generate_okx_headers("POST", "/api/v5/ai/asp/submit", '{"test": true}')
            self.assertEqual(headers["OK-ACCESS-KEY"], "test_api_key")
            self.assertEqual(headers["OK-ACCESS-PASSPHRASE"], "test_passphrase")
            self.assertEqual(headers["OK-ACCESS-PROJECT"], "test_project_123")
            self.assertEqual(headers["x-simulated-trading"], "1")
            self.assertIn("OK-ACCESS-SIGN", headers)
            self.assertIn("OK-ACCESS-TIMESTAMP", headers)

    @patch("requests.post")
    def test_submit_asp_listing_real_retry_then_success(self, mock_post):
        manifest = build_asp_manifest(
            agent_name="Retry Agent",
            description="Testing Retry Mechanism",
            capabilities=["Testing"],
            pricing_model="pay_per_job",
            contact_email="retry@builderforge.ai",
        )
        fail_resp = MagicMock()
        fail_resp.status_code = 502
        fail_resp.text = "Bad Gateway"

        success_resp = MagicMock()
        success_resp.status_code = 200
        success_resp.json.return_value = {
            "code": "0",
            "data": [{"asp_id": "asp_retry_123", "status": "approved"}]
        }
        mock_post.side_effect = [fail_resp, success_resp]

        with patch("utils.okx_integration.is_real_asp_enabled", return_value=True), patch("time.sleep", return_value=None):
            res = submit_asp_listing(manifest)
            self.assertTrue(res["success"])
            self.assertEqual(res["asp_id"], "asp_retry_123")
            self.assertFalse(res["simulated"])

    @patch("requests.get")
    def test_get_asp_status_real(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "code": "0",
            "data": [{"status": "approved", "listing_url": "https://www.okx.com/ai/asp/asp_999"}]
        }
        mock_get.return_value = mock_resp

        with patch("utils.okx_integration.is_real_asp_enabled", return_value=True):
            res = get_asp_status("asp_999")
            self.assertEqual(res["asp_id"], "asp_999")
            self.assertEqual(res["status"], "approved")
            self.assertFalse(res["simulated"])

    def test_get_web3_client_disabled(self):
        from utils.okx_integration import get_web3_client
        with patch("utils.okx_integration.is_real_rpc_enabled", return_value=False):
            client = get_web3_client()
            self.assertIsNone(client)


if __name__ == "__main__":
    unittest.main()
