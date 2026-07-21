"""BuilderForge - OKX ASP Listing Page.

Complete workflow to list BuilderForge as an Agentic Service Provider on OKX.AI.
Includes manifest builder, submission simulation, and status tracking.
"""

import streamlit as st
import json
import os
from datetime import datetime

from utils.state import init_session_state
from ui.styles import apply_theme, status_badge
from ui.components import render_header, render_action_button, render_app_nav
from utils.okx_integration import (
    build_asp_manifest,
    submit_asp_listing,
    get_asp_status,
)

st.set_page_config(page_title="BuilderForge - OKX ASP Listing", page_icon="🔗", layout="wide")
apply_theme()
init_session_state()
main_col = render_app_nav("pages/5_OKX_ASP_Listing.py")
with main_col:

    # ---------------------------------------------------------------------------
    # Main Content
    # ---------------------------------------------------------------------------

    render_header(
        "List as ASP on OKX.AI",
        "Submit BuilderForge as an Agentic Service Provider to the OKX AI marketplace"
    )

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # ASP Overview
    st.markdown(
        """
        <div class="glass-card" style="padding: 2rem; border-radius: 16px; margin-bottom: 3rem;">
            <h3 style="margin-top: 0 !important;">What is an Agentic Service Provider (ASP)?</h3>
            <p style="color: #94A3B8; font-size: 0.95rem; line-height: 1.6;">
                An <strong>ASP</strong> on OKX.AI is an AI-powered service that can be discovered, used, and monetized 
                through the OKX ecosystem. By listing BuilderForge as an ASP, you enable users to discover your agent 
                in the OKX.AI marketplace and use your multi-agent pipeline directly.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ASP Manifest Builder
    st.markdown("## 📝 ASP Manifest Builder")
    st.caption("Fill in the details below to build your ASP listing manifest")

    with st.form("asp_manifest_form_deck"):
        col1, col2 = st.columns(2)

        with col1:
            agent_name = st.text_input(
                "ASP Name *",
                value="BuilderForge",
                help="The name shown in the OKX.AI marketplace",
            )
            contact_email = st.text_input(
                "Contact Email *",
                placeholder="team@builderforge.ai",
            )
            pricing_model = st.selectbox(
                "Pricing Model",
                options=["freemium", "subscription", "pay_per_use", "free"],
                index=0,
            )

        with col2:
            description = st.text_area(
                "Short Description *",
                value="Multi-agent system that autonomously researches, creates, and deploys web3 projects.",
                height=80,
                help="One-line description for marketplace listing",
            )
            category = st.selectbox(
                "Category",
                options=[
                    "DeFi Agent",
                    "AI Content Creator",
                    "Smart Contract Generator",
                    "Market Analyzer",
                    "Launchpad Assistant",
                    "Multi-Agent Orchestrator",
                ],
                index=5,
            )

        st.markdown("### 🎯 Capabilities")
        st.caption("Select the capabilities your ASP provides")

        capabilities = []
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.checkbox("Market Research", value=True): capabilities.append("market_research")
            if st.checkbox("Competitor Analysis", value=True): capabilities.append("competitor_analysis")
            if st.checkbox("Grant Discovery", value=True): capabilities.append("grant_discovery")
        with col2:
            if st.checkbox("Tokenomics Design", value=True): capabilities.append("tokenomics_design")
            if st.checkbox("Content Generation", value=True): capabilities.append("content_generation")
            if st.checkbox("Smart Contract Creation", value=True): capabilities.append("smart_contract_creation")
        with col3:
            if st.checkbox("Blockchain Simulation", value=True): capabilities.append("blockchain_simulation")
            if st.checkbox("Deployment Planning", value=True): capabilities.append("deployment_planning")
            if st.checkbox("Analytics & Reporting", value=True): capabilities.append("analytics_reporting")

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔨 BUILD MANIFEST", use_container_width=True, type="primary")

    if submitted:
        if not contact_email:
            st.error("Contact email is required for ASP listing.")
            st.stop()

        manifest = build_asp_manifest(
            agent_name=agent_name,
            description=description,
            capabilities=capabilities,
            pricing_model=pricing_model,
            contact_email=contact_email,
        )

        st.session_state["asp_manifest"] = manifest
        st.session_state["asp_manifest_built"] = True

        st.success("✅ ASP Manifest built successfully!")
        st.balloons()

        st.divider()
        st.markdown("### 📄 Generated Manifest")
        st.json(manifest)

        st.download_button(
            label="💾 DOWNLOAD MANIFEST JSON",
            data=json.dumps(manifest, indent=2),
            file_name=f"asp_manifest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True,
        )

    st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)

    # Submit to OKX.AI
    st.markdown("## 🚀 Submit to OKX.AI Marketplace")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            """
            Once your manifest is ready, submit it to the OKX.AI marketplace. 
            The submission will be reviewed by the OKX team to ensure it meets the technical standards.
            """
        )
    with col2:
        manifest_ready = st.session_state.get("asp_manifest_built", False)
        if st.button(
            "📤 SUBMIT TO OKX.AI",
            key="submit_asp",
            use_container_width=True,
            disabled=not manifest_ready,
            help="Build a manifest first" if not manifest_ready else None,
        ):
            with st.spinner("Submitting to OKX.AI marketplace..."):
                manifest = st.session_state.get("asp_manifest", {})
                result = submit_asp_listing(manifest)
                st.session_state["asp_submission"] = result
                st.session_state["okx_asp_listed"] = True
                st.success("✅ Submitted to OKX.AI!")
                st.json(result)

    st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)

    # ASP Status Dashboard
    st.markdown("## 📊 ASP Status Dashboard")

    if st.session_state.get("okx_asp_listed", False):
        submission = st.session_state.get("asp_submission", {})

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status_badge(submission.get("status", "pending"), "active")
        with col2:
            render_metric_card("ASP ID", submission.get("asp_id", "N/A"))
        with col3:
            render_metric_card("Simulated", "✅" if submission.get("simulated") else "❌")
        with col4:
            status_badge("Listed on OKX.AI", "done")

        st.json(submission)
    else:
        st.info("No ASP submission yet. Build a manifest and submit it above.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #334155; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; padding-bottom: 2rem;">
            BuilderForge — AI Genesis Hackathon 2026
        </div>
        """,
        unsafe_allow_html=True,
    )
