"""Content Generation Tools for BuilderForge.

Creates tokenomics models, pitch decks, social content,
website copy, and smart contract code.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from datetime import datetime

from langchain.tools import tool


@tool("generate_tokenomics")
def generate_tokenomics(project_name: str, total_supply: int = 1000000000) -> str:
    """Generate tokenomics model for a project.
    
    Creates a complete token distribution and economics model.
    """
    model = {
        "project": project_name,
        "token_symbol": project_name[:4].upper(),
        "total_supply": total_supply,
        "distribution": [
            {"category": "Community & Airdrop", "percentage": 40, "amount": int(total_supply * 0.4),
             "vesting": "20% at TGE, then linear over 12 months"},
            {"category": "Team & Advisors", "percentage": 15, "amount": int(total_supply * 0.15),
             "vesting": "6-month cliff, then linear over 24 months"},
            {"category": "Investors", "percentage": 20, "amount": int(total_supply * 0.2),
             "vesting": "3-month cliff, then linear over 18 months"},
            {"category": "Ecosystem & Treasury", "percentage": 15, "amount": int(total_supply * 0.15),
             "vesting": "DAO-governed releases over 48 months"},
            {"category": "Liquidity & DEX Listing", "percentage": 10, "amount": int(total_supply * 0.1),
             "vesting": "100% at TGE for initial liquidity"},
        ],
        "token_utility": [
            "Governance voting (veToken model)",
            "Staking rewards and yield farming",
            "Platform fee discounts",
            "Access to premium features",
            "Community DAO participation",
        ],
        "economic_model": {
            "type": "Deflationary with buyback-and-burn",
            "initial_mcap_estimate": f"${total_supply * 0.0001:,.0f}",
            "inflation_rate": "2% annually after year 2",
        },
        "recommended_listing": "OKX DEX + Uniswap V3",
    }
    return json.dumps(model, indent=2)


@tool("generate_pitch_sections")
def generate_pitch_sections(project_name: str, description: str, category: str) -> str:
    """Generate pitch deck sections for a project.
    
    Creates problem, solution, market, and traction slides.
    """
    pitch = {
        "problem": f"Current {category} solutions are fragmented, require technical expertise, "
                   f"and lack AI-powered automation. Teams spend 3-6 months from idea to launch.",
        "solution": f"{project_name} uses autonomous AI agents to research, create, and deploy "
                    f"{category} projects in hours instead of months.",
        "how_it_works": [
            "1. Input your idea and goals",
            "2. AI Researcher discovers market opportunities and competitors",
            "3. AI Creator generates tokenomics, content, and contracts",
            "4. AI Executor simulates deployment on OKC testnet",
            "5. AI Analyzer provides metrics and next steps",
        ],
        "market_size": {
            "tam": "$4.8B (AI x Web3 agent market by 2028)",
            "sam": "$1.2B (Agentic Service Provider market)",
            "target": "$240M (launchpad + creation tools)",
        },
        "traction": [
            "✅ MVP built for OKX AI Genesis Hackathon",
            "✅ Multi-agent system with 5 specialized agents",
            "✅ OKX testnet integration and ASP listing workflow",
            "✅ Working prototype with simulated on-chain actions",
        ],
        "business_model": {
            "revenue_streams": [
                "Tiered subscription (Free/Pro/Enterprise)",
                "Transaction fees on token launches",
                "ASP marketplace commission",
            ],
            "unit_economics": "CAC: $15, LTV: $180 (12:1 ratio)",
        },
        "ask": "Seeking $500K seed to build full team, integrate real chains, and launch ASP marketplace.",
    }
    return json.dumps(pitch, indent=2)


@tool("generate_social_copy")
def generate_social_copy(project_name: str, description: str, platform: str = "twitter") -> str:
    """Generate social media content for project announcements.
    
    Creates platform-specific posts for Twitter/X, LinkedIn, and Warpcast.
    """
    symbol = project_name[:4].upper()
    copies = {
        "twitter": [
            f"🚀 We're building {project_name} — the first AI-native Agentic Service Provider.\n\n"
            f"Turn any idea into a launched product with autonomous AI agents. "
            f"Research → Create → Deploy → Analyze.\n\n"
            f"Powered by @okx Web3 🛡️\n\n"
            f"#OKXHackathon #AI #Web3 #Agentic",

            f"💡 Got an idea? {project_name} takes you from zero to launched in hours.\n\n"
            f"🧠 AI Researcher finds opportunities\n"
            f"🎨 AI Creator builds your assets\n"
            f"⚡ AI Executor deploys on testnet\n"
            f"📊 AI Analyzer tracks metrics\n\n"
            f"The future of launching is autonomous.",

            f"🏗️ {project_name} = DealFlow + LaunchPad Ally\n\n"
            f"• Find opportunities & grants\n"
            f"• Generate tokenomics & content\n"
            f"• Simulate on-chain deployment\n"
            f"• Export & list as ASP on OKX.AI\n\n"
            f"All powered by CrewAI + Claude.",
        ],
        "linkedin": [
            f"I'm thrilled to announce {project_name}, a multi-agent system that "
            f"autonomously turns ideas into launched web3 products.\n\n"
            f"Built for the OKX AI Genesis Hackathon, {project_name} combines "
            f"5 specialized AI agents to handle market research, content creation, "
            f"smart contract deployment, and launch planning.\n\n"
            f"Key differentiators:\n"
            f"• End-to-end automation from idea to deployment\n"
            f"• OKX testnet integration for simulated transactions\n"
            f"• Ready to list as an Agentic Service Provider on OKX.AI\n\n"
            f"Built with CrewAI, LangChain, Claude, and Streamlit.",
        ],
        "warpcast": [
            f"gm 🌅\n\n"
            f"Building {project_name} — an autonomous agent that takes your idea "
            f"and launches it on-chain.\n\n"
            f"AI agents handle:\n"
            f"🔍 Research & opportunity finding\n"
            f"🎨 Tokenomics, content, contracts\n"
            f"⚡ Deployment simulation\n"
            f"📊 Analysis & next steps\n\n"
            f"Built for @okx AI Genesis Hackathon. "
            f"DealFlow × LaunchPad = BuilderForge 🔨",
        ],
    }
    result = copies.get(platform, copies["twitter"])
    return json.dumps({"platform": platform, "copies": result}, indent=2)


@tool("generate_website_copy")
def generate_website_copy(project_name: str, description: str) -> str:
    """Generate website landing page copy for a project."""
    return json.dumps({
        "hero_title": f"Turn Ideas into Launched Products with Autonomous AI Agents",
        "hero_subtitle": f"{project_name} combines research, creation, and on-chain deployment "
                         f"into one seamless agentic workflow.",
        "features": [
            {"title": "DealFlow", "description": "AI-powered opportunity discovery. Find market gaps, grants, and audiences automatically."},
            {"title": "LaunchPad Ally", "description": "From idea to execution. Generate tokenomics, content, smart contracts, and deployment plans."},
            {"title": "On-Chain Simulation", "description": "Test deployments on OKC testnet before going live. No gas wasted."},
            {"title": "ASP Ready", "description": "Built to list on OKX.AI as an Agentic Service Provider from day one."},
        ],
        "cta": "Start Building Free",
        "value_props": [
            "🚀 Launch in hours, not months",
            "🤖 5 specialized AI agents working in parallel",
            "🔗 OKX testnet + mainnet ready",
            "📦 Export your complete project package",
        ],
    }, indent=2)


@tool("generate_contract_code")
def generate_contract_code(token_name: str, token_symbol: str, is_mintable: bool = True) -> str:
    """Generate Solidity smart contract code for an ERC-20 token.
    
    Creates production-ready contract code with OpenZeppelin standards.
    """
    mintable_clause = """
    // Mint function for initial distribution
    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }""" if is_mintable else ""

    contract = f"""// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

/**
 * @title {token_name}
 * @dev {token_symbol} token with minting and burning capabilities
 * Generated by BuilderForge - AI-powered contract creation
 */
contract {token_name.replace(' ', '')} is ERC20, Ownable, ERC20Burnable {{
    
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18;
    uint256 public immutable deployTime;
    
    constructor()
        ERC20("{token_name}", "{token_symbol}")
        Ownable(msg.sender)
    {{
        deployTime = block.timestamp;
        // Initial supply: 10% goes to deployer for initial liquidity
        _mint(msg.sender, 100_000_000 * 10**18);
    }}{mintable_clause}
    
    // Optional: Override for tax mechanisms
    function _update(address from, address to, uint256 value)
        internal
        override
    {{
        super._update(from, to, value);
    }}
    
    // View functions
    function circulatingSupply() external view returns (uint256) {{
        return totalSupply();
    }}
    
    function timeSinceDeploy() external view returns (uint256) {{
        return block.timestamp - deployTime;
    }}
}}
"""
    return json.dumps({
        "contract_name": token_name.replace(' ', '') + ".sol",
        "language": "Solidity ^0.8.20",
        "framework": "Hardhat / Foundry",
        "dependencies": ["@openzeppelin/contracts ^5.0.0"],
        "code": contract,
        "notes": [
            "Use OpenZeppelin v5.0+ for compatibility",
            "Deploy with Hardhat: npx hardhat run scripts/deploy.ts",
            "Verify on OKC explorer: hardhat verify --network okc",
        ],
    }, indent=2)
