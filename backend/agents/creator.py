"""BuilderForge Creator Agent (LaunchPad Asset Synthesis)."""

from __future__ import annotations

import logging
from typing import Dict, Any

try:
    from tools.content_tools import (
        generate_tokenomics_model,
        generate_solidity_contract,
        generate_pitch_deck,
    )
except ImportError:
    from ..tools.content_tools import (
        generate_tokenomics_model,
        generate_solidity_contract,
        generate_pitch_deck,
    )

logger = logging.getLogger(__name__)


class CreatorAgent:
    """Agent responsible for tokenomics modeling, smart contract generation, and pitch material synthesis."""

    def __init__(self, mode: str = "SIMULATED"):
        self.mode = mode

    def run(self, project_title: str, description: str, category: str = "General") -> Dict[str, Any]:
        """Synthesize tokenomics, smart contract code, and pitch assets."""
        logger.info(f"[Creator Agent] Synthesizing launch assets for '{project_title}'...")
        
        tokenomics = generate_tokenomics_model(project_title, category)
        solidity_code = generate_solidity_contract(tokenomics["token_name"], tokenomics["token_symbol"])
        pitch = generate_pitch_deck(project_title, description)
        
        return {
            "token_name": tokenomics["token_name"],
            "token_symbol": tokenomics["token_symbol"],
            "total_supply": tokenomics["total_supply"],
            "allocations": tokenomics["allocations"],
            "utility": tokenomics["utility"],
            "smart_contract_code": solidity_code,
            "pitch_tagline": pitch["pitch_tagline"],
            "elevator_pitch": pitch["elevator_pitch"],
            "key_features": pitch["key_features"],
            "marketing_hooks": pitch["marketing_hooks"],
        }
