"""BuilderForge - LaunchPad Ally Page.

Content generation, tokenomics, smart contracts, and deployment simulation.
"""

import streamlit as st
import json

from utils.state import init_session_state, get_current_project, save_project
from ui.styles import apply_theme
from ui.components import render_header, render_phase_output, render_action_button, render_wallet_status, render_sidebar, render_status_card
from tools.content_tools import generate_tokenomics, generate_contract_code, generate_social_copy
from tools.blockchain_tools import simulate_transaction_sequence

st.set_page_config(page_title="BuilderForge - LaunchPad", page_icon="🚀", layout="wide")
apply_theme()
init_session_state()

# ---------------------------------------------------------------------------
# Sidebar Navigation (Consistent)
# ---------------------------------------------------------------------------

with st.sidebar:
    render_sidebar("pages/4_LaunchPad.py")
    render_status_card()

# ---------------------------------------------------------------------------
# Main Content
# ---------------------------------------------------------------------------

render_header("LaunchPad Ally", "From idea to execution — assets, contracts, and deployment")

project = get_current_project()

if not project:
    st.warning("No project selected. Create one first!")
    st.page_link("pages/1_New_Project.py", label="→ Create a New Project", icon="🚀")
    st.stop()

st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# LaunchPad Sections
# ---------------------------------------------------------------------------

tab1, tab2, tab3 = st.tabs(["🎯 Tokenomics & Pitch", "📝 Content & Contracts", "⛓️ On-Chain Simulation"])

with tab1:
    st.markdown("## Tokenomics Model")
    if st.button("🎯 GENERATE TOKENOMICS", key="gen_tokenomics", use_container_width=True):
        with st.spinner("Creator agent designing tokenomics..."):
            result = generate_tokenomics(project.title)
            data = json.loads(result)
            if not isinstance(project.launch_assets, dict):
                project.launch_assets = {}
            project.launch_assets["tokenomics"] = data
            save_project(project)
            st.success("Tokenomics generated!")

    tokenomics = project.launch_assets.get("tokenomics", {}) if isinstance(project.launch_assets, dict) else {}
    if tokenomics:
        st.json(tokenomics)
        
        # Distribution visual
        dist = tokenomics.get("distribution", [])
        if dist:
            st.markdown("### Distribution Breakdown")
            for item in dist:
                st.markdown(
                    f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <span style="font-size: 0.85rem; font-weight: 600; color: #ffffff;">{item.get('category')}</span>
                            <span style="font-size: 0.85rem; color: #FF4D00;">{item.get('percentage')}%</span>
                        </div>
                        <div style="height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden;">
                            <div style="width: {item.get('percentage')}%; height: 100%; background: #FF4D00;"></div>
                        </div>
                        <div style="font-size: 0.7rem; color: #64748B; margin-top: 0.25rem;">Vesting: {item.get('vesting', 'N/A')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## Pitch Deck Sections")
    from tools.content_tools import generate_pitch_sections
    if st.button("📊 GENERATE PITCH DECK", key="gen_pitch", use_container_width=True):
        with st.spinner("Creating pitch deck content..."):
            result = generate_pitch_sections(project.title, project.description, project.category)
            data = json.loads(result)
            if not isinstance(project.launch_assets, dict):
                project.launch_assets = {}
            project.launch_assets["pitch_deck"] = data
            save_project(project)
            st.success("Pitch deck sections generated!")

    pitch = project.launch_assets.get("pitch_deck", {}) if isinstance(project.launch_assets, dict) else {}
    if pitch:
        for k, v in pitch.items():
            st.markdown(f"<div style='margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 0.7rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem;'>{k.replace('_', ' ')}</div>", unsafe_allow_html=True)
            if isinstance(v, str):
                st.markdown(f"<div class='glass-card' style='padding: 1.25rem; border-radius: 12px; color: #E2E8F0; line-height: 1.6;'>{v}</div>", unsafe_allow_html=True)
            elif isinstance(v, list):
                for item in v:
                    st.markdown(f"<div class='glass-card' style='padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem; color: #E2E8F0;'>• {item}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("## Social Media Copy")
    platform = st.selectbox("Platform", ["twitter", "linkedin", "warpcast"], index=0)
    if st.button("📝 GENERATE SOCIAL COPY", key="gen_social", use_container_width=True):
        with st.spinner("Creating social media content..."):
            result = generate_social_copy(project.title, project.description, platform)
            data = json.loads(result)
            if not isinstance(project.launch_assets, dict):
                project.launch_assets = {}
            project.launch_assets["social_copy"] = data
            save_project(project)
            st.success(f"Social copy for {platform} generated!")

    social = project.launch_assets.get("social_copy", {}) if isinstance(project.launch_assets, dict) else {}
    if social:
        copies = social.get("copies", [])
        for i, copy in enumerate(copies):
            st.markdown(
                f"""
                <div class="glass-card" style="padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                    <div style="font-size: 0.65rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 1rem;">Variant {i+1}</div>
                    <div style="color: #E2E8F0; line-height: 1.6; margin-bottom: 1rem;">{copy}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"📋 COPY VARIANT {i+1}", key=f"copy_{i}"):
                st.toast("Copied to clipboard! (simulated)")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## Smart Contract Code")
    token_symbol = st.text_input("Token Symbol", value=project.title[:4].upper(), max_chars=5)

    if st.button("📄 GENERATE CONTRACT", key="gen_contract", use_container_width=True):
        with st.spinner("Generator agent creating Solidity contract..."):
            result = generate_contract_code(project.title, token_symbol)
            data = json.loads(result)
            if not isinstance(project.launch_assets, dict):
                project.launch_assets = {}
            project.launch_assets["smart_contract"] = data
            save_project(project)
            st.success("Smart contract generated!")

    contract = project.launch_assets.get("smart_contract", {}) if isinstance(project.launch_assets, dict) else {}
    if contract:
        st.code(contract.get("code", ""), language="solidity")
        st.caption(f"Framework: {contract.get('framework', 'N/A')}")

with tab3:
    st.markdown("## On-Chain Simulation")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔌 CONNECT OKX WALLET", key="launch_connect", use_container_width=True):
            from utils.okx_integration import connect_wallet
            result = connect_wallet()
            if not isinstance(project.deployment_plan, dict):
                project.deployment_plan = {}
            project.deployment_plan["wallet"] = result
            save_project(project)
            st.success("Wallet connected!")

    with col2:
        if st.button("⛓️ SIMULATE DEPLOYMENT", key="sim_deploy", use_container_width=True):
            with st.spinner("Simulating deployment sequence..."):
                wallet_info = project.deployment_plan.get("wallet", {}) if isinstance(project.deployment_plan, dict) else {}
                deployer = wallet_info.get("address", "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18")
                result = simulate_transaction_sequence(project.title, deployer)
                data = json.loads(result)
                project.deployment_plan["deployment_sequence"] = data
                save_project(project)
                st.success("Deployment simulation complete!")

    wallet_info = project.deployment_plan.get("wallet", {}) if isinstance(project.deployment_plan, dict) else {}
    if wallet_info:
        render_wallet_status(wallet_info.get("address", ""), wallet_info.get("balance", "0"))

    dep_seq = project.deployment_plan.get("deployment_sequence", {}) if isinstance(project.deployment_plan, dict) else {}
    if dep_seq:
        st.markdown("### Deployment Sequence")
        for step in dep_seq.get("steps", []):
            st.markdown(
                f"""
                <div class="glass-card" style="padding: 1.25rem; border-radius: 12px; margin-bottom: 0.75rem;">
                    <div style="font-weight: 700; color: #ffffff; margin-bottom: 0.5rem;">Step {step.get('step')}: {step.get('action')}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.info(f"⛽ Total gas used: {dep_seq.get('total_gas_used', 0)} OKT | Network: OKC Testnet")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align: center; color: #334155; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; padding-bottom: 2rem;">
        BuilderForge — AI Genesis Hackathon 2026
    </div>
    """,
    unsafe_allow_html=True,
)
