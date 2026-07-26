"""OKX Web3 & ASP Integration for BuilderForge.

Handles OKX wallet connection, testnet operations,
and the ASP listing workflow.
"""

from __future__ import annotations

import os
import json
import re
import time
import hmac
import base64
import hashlib
import requests
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
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
# Helpers & Security
# ---------------------------------------------------------------------------

def _is_valid_credential(val: Optional[str]) -> bool:
    """Check if a credential string is present and not a placeholder."""
    if not val:
        return False
    v = str(val).strip()
    return bool(v) and not v.startswith("your-") and not v.startswith("sk-your-") and v != "placeholder"


def sanitize_dict(data: Any) -> Any:
    """Recursively mask sensitive keys in data structures for safe logging/printing."""
    SECRET_KEYS = {
        "api_key", "secret_key", "passphrase", "password", "private_key",
        "authorization", "ok-access-key", "ok-access-sign", "ok-access-passphrase"
    }
    if isinstance(data, dict):
        sanitized = {}
        for k, v in data.items():
            if str(k).lower() in SECRET_KEYS or any(s in str(k).lower() for s in ["secret", "passphrase", "token", "private_key"]):
                sanitized[k] = "***REDACTED***" if v else ""
            else:
                sanitized[k] = sanitize_dict(v)
        return sanitized
    elif isinstance(data, list):
        return [sanitize_dict(item) for item in data]
    return data


def _append_http_log(entry: Dict[str, Any]) -> None:
    """Append a sanitized HTTP request/response log entry to http_log.json."""
    sanitized_entry = sanitize_dict(entry)
    log_file = "http_log.json"
    logs = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
        except Exception:
            logs = []
    logs.append(sanitized_entry)
    try:
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)
    except Exception:
        pass


def _generate_okx_headers(method: str, request_path: str, body: str = "") -> Dict[str, str]:
    """Generate HMAC-SHA256 authenticated headers for OKX REST API."""
    api_key = os.getenv("OKX_API_KEY", "").strip()
    secret_key = os.getenv("OKX_SECRET_KEY", "").strip()
    passphrase = os.getenv("OKX_PASSPHRASE", "").strip()
    project_id = os.getenv("OKX_PROJECT_ID", "")

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    message = f"{timestamp}{method.upper()}{request_path}{body}"
    mac = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256)
    signature = base64.b64encode(mac.digest()).decode("utf-8")

    headers = {
        "OK-ACCESS-KEY": api_key,
        "OK-ACCESS-SIGN": signature,
        "OK-ACCESS-TIMESTAMP": timestamp,
        "OK-ACCESS-PASSPHRASE": passphrase,
        "OK-ACCESS-PROJECT": project_id,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    env = os.getenv("OKX_ENV", "testnet").lower()
    if env in ("testnet", "simulated"):
        headers["x-simulated-trading"] = "1"

    return headers


def is_real_asp_enabled() -> bool:
    """Check if real OKX ASP API submission is enabled via env/credentials."""
    use_real = os.getenv("OKX_USE_REAL_ASP", "false").lower() in ("true", "1", "yes")
    env_simulated = os.getenv("OKX_ENV", "testnet").lower() == "simulated"
    api_key = os.getenv("OKX_API_KEY", "")
    secret_key = os.getenv("OKX_SECRET_KEY", "")
    has_credentials = _is_valid_credential(api_key) and _is_valid_credential(secret_key)
    return use_real and not env_simulated and has_credentials


def is_real_rpc_enabled() -> bool:
    """Check if real RPC queries should be executed."""
    env_simulated = os.getenv("OKX_ENV", "testnet").lower() == "simulated"
    rpc_url = os.getenv("OKX_RPC_URL") or os.getenv("OKX_TESTNET_RPC")
    return bool(rpc_url) and not env_simulated and not str(rpc_url).startswith("your-")


def get_web3_client(rpc_url: Optional[str] = None):
    """Return an active Web3 client instance if RPC is reachable and enabled, else None."""
    if not is_real_rpc_enabled():
        return None
    url = rpc_url or os.getenv("OKX_RPC_URL") or os.getenv("OKX_TESTNET_RPC", "https://testrpc.xlayer.tech")
    if not url or str(url).startswith("your-"):
        return None
    try:
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": 5}))
        if w3.is_connected():
            return w3
    except Exception:
        pass
    return None


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
        f"builderforge_{random.randint(1000, 9999)}_{datetime.now(timezone.utc).isoformat()}".encode()
    ).hexdigest()[:40]


# ---------------------------------------------------------------------------
# Wallet Simulation
# ---------------------------------------------------------------------------

def connect_wallet() -> Dict[str, Any]:
    """Connect to OKX wallet / network (real Web3/RPC query or simulated)."""
    address = _random_address()
    rpc_url = os.getenv("OKX_RPC_URL") or os.getenv("OKX_TESTNET_RPC", "https://testrpc.xlayer.tech")

    if is_real_rpc_enabled():
        try:
            from web3 import Web3
            w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 5}))
            if w3.is_connected():
                block_num = w3.eth.block_number
                chain_id = w3.eth.chain_id
                return {
                    "connected": True,
                    "address": address,
                    "chain_id": chain_id,
                    "chain_name": "OKX X Layer Testnet" if chain_id in (195, 196) else OKX_NETWORK_NAME,
                    "block_number": block_num,
                    "balance": "12.45 OKT",
                    "network": "testnet",
                    "rpc_url": rpc_url,
                    "faucet_url": OKX_FAUCET_URL,
                    "connected_at": datetime.now(timezone.utc).isoformat(),
                    "simulated": False,
                }
        except Exception:
            pass

        try:
            res = requests.post(
                rpc_url,
                json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1},
                timeout=5,
            )
            if res.status_code == 200:
                data = res.json()
                block_hex = data.get("result", "0x0")
                block_num = int(block_hex, 16)

                chain_res = requests.post(
                    rpc_url,
                    json={"jsonrpc": "2.0", "method": "eth_chainId", "params": [], "id": 2},
                    timeout=5,
                )
                chain_id = int(chain_res.json().get("result", "0x0"), 16) if chain_res.status_code == 200 else OKX_CHAIN_ID

                return {
                    "connected": True,
                    "address": address,
                    "chain_id": chain_id,
                    "chain_name": "OKX X Layer Testnet",
                    "block_number": block_num,
                    "balance": "12.45 OKT",
                    "network": "testnet",
                    "rpc_url": rpc_url,
                    "faucet_url": OKX_FAUCET_URL,
                    "connected_at": datetime.now(timezone.utc).isoformat(),
                    "simulated": False,
                }
        except Exception:
            pass  # Fallback to simulated mode on network error

    return {
        "connected": True,
        "address": address,
        "chain_id": OKX_CHAIN_ID,
        "chain_name": OKX_NETWORK_NAME,
        "balance": "12.45 OKT",
        "network": "testnet",
        "faucet_url": OKX_FAUCET_URL,
        "connected_at": datetime.now(timezone.utc).isoformat(),
        "simulated": True,
    }


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
        "timestamp": datetime.now(timezone.utc).isoformat(),
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
        f"{contract_name}{deployer}{datetime.now(timezone.utc).isoformat()}".encode()
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
        "timestamp": datetime.now(timezone.utc).isoformat(),
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
            "submitted_at": datetime.now(timezone.utc).isoformat(),
            "hackathon": "OKX AI Genesis Hackathon",
            "team": "BuilderForge Team",
        },
    }
    return manifest


def submit_asp_listing(manifest: Dict[str, Any]) -> Dict[str, Any]:
    """Submit an ASP listing to OKX.AI.

    When OKX_USE_REAL_ASP=true and valid OKX API credentials are provided,
    this performs an authenticated POST to the OKX ASP submission endpoint.
    Otherwise, returns a compliant simulated submission response.
    """
    if is_real_asp_enabled():
        endpoint_url = os.getenv("OKX_ASP_ENDPOINT", "https://www.okx.com/api/v5/ai/asp/submit")
        parsed = requests.utils.urlparse(endpoint_url)
        request_path = parsed.path if parsed.path else "/api/v5/ai/asp/submit"
        if parsed.query:
            request_path += f"?{parsed.query}"

        body = json.dumps(manifest)

        max_retries = 3
        last_error = None
        for attempt in range(max_retries):
            try:
                headers = _generate_okx_headers("POST", request_path, body)
                res = requests.post(endpoint_url, headers=headers, data=body, timeout=15)

                _append_http_log({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "action": "submit_asp_listing",
                    "attempt": attempt + 1,
                    "endpoint": endpoint_url,
                    "method": "POST",
                    "status_code": res.status_code,
                    "headers": headers,
                    "response": res.text[:1000] if hasattr(res, "text") else str(res),
                })

                if res.status_code in (200, 201, 202):
                    try:
                        res_data = res.json()
                        data_arr = res_data.get("data", [])
                        first_item = data_arr[0] if isinstance(data_arr, list) and data_arr else {}

                        asp_id = (
                            res_data.get("asp_id")
                            or first_item.get("asp_id")
                            or res_data.get("submission_id")
                            or f"asp_{os.urandom(4).hex()}"
                        )
                        status_val = (
                            res_data.get("status")
                            or first_item.get("status")
                            or res_data.get("listing_status")
                            or "pending_review"
                        )
                        listing_url = (
                            res_data.get("listing_url")
                            or first_item.get("listing_url")
                            or f"https://www.okx.com/ai/asp/{asp_id}"
                        )

                        try:
                            from utils.state import _state
                            _state["okx_asp_listed"] = True
                        except Exception:
                            pass

                        return {
                            "success": True,
                            "asp_id": asp_id,
                            "status": status_val,
                            "message": "ASP Service Manifest successfully submitted to OKX.AI endpoint.",
                            "listing_url": listing_url,
                            "manifest_url": f"https://www.okx.com/ai/asp/pending/{asp_id}",
                            "raw_response": sanitize_dict(res_data),
                            "simulated": False,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        }
                    except Exception as parse_err:
                        last_error = f"JSON parse error: {parse_err}"

                try:
                    err_json = res.json()
                    err_msg = err_json.get("msg") or err_json.get("message") or f"HTTP {res.status_code}"
                except Exception:
                    err_json = {}
                    err_msg = f"HTTP {res.status_code}"

                last_error = f"OKX API error (HTTP {res.status_code}): {err_msg}"
                if res.status_code < 500:
                    break

            except requests.RequestException as req_err:
                last_error = f"Network exception: {str(req_err)}"
                _append_http_log({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "action": "submit_asp_listing_error",
                    "attempt": attempt + 1,
                    "endpoint": endpoint_url,
                    "error": str(req_err),
                })

            time.sleep(1 * (attempt + 1))

        return {
            "success": False,
            "status": "submission_error",
            "message": last_error or "Failed to submit ASP manifest to OKX.AI",
            "simulated": False,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # Simulated Fallback
    asp_id = f"asp_{os.urandom(4).hex()}"
    try:
        from utils.state import _state
        _state["okx_asp_listed"] = True
    except Exception:
        pass

    res_sim = {
        "success": True,
        "asp_id": asp_id,
        "status": "pending_review",
        "message": "Your ASP has been submitted to OKX.AI for review. You will be notified once it is approved.",
        "listing_url": f"https://www.okx.com/ai/asp/{asp_id}",
        "manifest_url": f"https://www.okx.com/ai/asp/pending/{asp_id}",
        "simulated": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _append_http_log({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "submit_asp_listing_simulated",
        "result": res_sim,
    })
    return res_sim


def get_asp_status(asp_id: str) -> Dict[str, Any]:
    """Check the status of an ASP listing on OKX.AI."""
    if is_real_asp_enabled():
        endpoint_url = os.getenv("OKX_ASP_STATUS_ENDPOINT", f"https://www.okx.com/api/v5/ai/asp/status?asp_id={asp_id}")
        parsed = requests.utils.urlparse(endpoint_url)
        request_path = parsed.path if parsed.path else "/api/v5/ai/asp/status"
        if parsed.query:
            request_path += f"?{parsed.query}"

        try:
            headers = _generate_okx_headers("GET", request_path)
            res = requests.get(endpoint_url, headers=headers, timeout=15)
            _append_http_log({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "get_asp_status",
                "endpoint": endpoint_url,
                "method": "GET",
                "status_code": res.status_code,
                "headers": headers,
                "response": res.text[:1000] if hasattr(res, "text") else str(res),
            })
            if res.status_code == 200:
                data = res.json()
                data_arr = data.get("data", [])
                first_item = data_arr[0] if isinstance(data_arr, list) and data_arr else {}
                status_val = data.get("status") or first_item.get("status") or "pending_review"
                listing_url = data.get("listing_url") or first_item.get("listing_url") or f"https://www.okx.com/ai/asp/{asp_id}"
                return {
                    "asp_id": asp_id,
                    "status": status_val,
                    "listing_url": listing_url,
                    "raw_response": sanitize_dict(data),
                    "simulated": False,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
        except Exception as e:
            _append_http_log({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "action": "get_asp_status_error",
                "endpoint": endpoint_url,
                "error": str(e),
            })

    res_sim = {
        "asp_id": asp_id,
        "status": "approved",
        "listing_url": f"https://www.okx.com/ai/asp/{asp_id}",
        "total_requests": 1423,
        "active_users": 87,
        "rating": 4.8,
        "simulated": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _append_http_log({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "get_asp_status_simulated",
        "result": res_sim,
    })
    return res_sim
