"""BuilderForge - Dashboard Page.

Main results view showing all project outputs across phases.
"""

import streamlit as st

from utils.state import (
    init_session_state,
    ProjectData,
    ProjectPhase,
    get_current_project,
    save_project,
)
from ui.styles import apply_theme, phase_stepper, console_log, status_badge
from ui.components import (
    render_app_nav,
    render_header,
    render_phase_output,
    render_metric_card,
    render_export_options,
    render_wallet_status,
    render_transaction_card,
)

st.set_page_config(page_title="BuilderForge - Dashboard", page_icon="📊", layout="wide")
apply_theme()
init_session_state()
main_col = render_app_nav("pages/2_Dashboard.py")
with main_col:
    project = get_current_project()

    # ---------------------------------------------------------------------------
    # Main Content
    # ---------------------------------------------------------------------------

    render_header("Project Dashboard", "Full results from the BuilderForge pipeline")

    if not project:
        st.markdown(
            """
            <div class="glass-card" style="padding: 3rem; text-align: center; border-radius: 16px;">
                <h3 style="margin-top: 0 !important;">No project selected</h3>
                <p style="margin-bottom: 2rem !important;">Create a new project first to view the dashboard results.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("→ CREATE A NEW PROJECT", use_container_width=True):
            st.switch_page("pages/1_New_Project.py")
        st.stop()

    # Project Overview Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card("Phase", project.phase)
    with col2:
        render_metric_card("Progress", f"{int(project.progress * 100)}%")
    with col3:
        render_metric_card("Category", project.category)
    with col4:
        render_metric_card("Created", project.created_at.split()[0] if project.created_at else "N/A")

    st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

    # Project Title & Description
    st.markdown(f"<h2 style='margin-bottom: 0.5rem !important;'>{project.title}</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"<div style='color: #94A3B8; font-size: 1rem;'>{project.description}</div>", unsafe_allow_html=True)
    with col2:
        if project.goals:
            st.markdown(
                """
                <div class="glass-card" style="padding: 1.5rem; border-radius: 12px;">
                    <div style="font-size: 0.65rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 1rem;">Goals</div>
                """,
                unsafe_allow_html=True
            )
            for g in project.goals:
                st.markdown(f"<div style='font-size: 0.85rem; color: #E2E8F0; margin-bottom: 0.5rem;'>• {g}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

    # Phase Outputs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🔍 Research", "🎨 Creation", "⚡ Execution", "📊 Analysis", "📦 Export"]
    )

    with tab1:
        render_phase_output("Research & Discovery", project.opportunity_report, "🔍")
        if project.research_output:
            with st.expander("Raw Agent Output"):
                st.code(project.research_output, language="json")

    with tab2:
        render_phase_output("Content & Assets", project.launch_assets, "🎨")
        if project.creation_output:
            with st.expander("Raw Agent Output"):
                st.code(project.creation_output, language="json")

    with tab3:
        render_phase_output("Deployment Plan", project.deployment_plan, "⚡")
        if project.transactions:
            st.markdown("### 💳 Recent Transactions")
            for tx in project.transactions[-5:]:
                render_transaction_card(tx)

    with tab4:
        render_phase_output("Analysis & Metrics", project.metrics_report, "📊")

    with tab5:
        render_export_options(project)

    st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)

    # Wallet Connection
    st.markdown("## 🔌 OKX Web3 Connection")
    col1, col2 = st.columns([2, 1])
    with col1:
        wallet = project.deployment_plan.get("wallet", {}) if isinstance(project.deployment_plan, dict) else {}
        addr = wallet.get("address", "") if isinstance(wallet, dict) else ""
        balance = wallet.get("balance", "0") if isinstance(wallet, dict) else "0"
        render_wallet_status(addr, balance)

    with col2:
        if st.button("SIMULATE WALLET CONNECT", key="sim_wallet", use_container_width=True):
            from utils.okx_integration import connect_wallet
            result = connect_wallet()
            if isinstance(project.deployment_plan, dict):
                project.deployment_plan["wallet"] = result
            else:
                project.deployment_plan = {"wallet": result}
            save_project(project)
            st.rerun()

    st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)

    # Agent Execution Log
    st.markdown("### 📋 Agent Execution Log")
    console_log(st.session_state.get("crew_log", []))

    st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #334155; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; padding-bottom: 2rem;">
            BuilderForge — AI Genesis Hackathon 2026
        </div>
        """,
        unsafe_allow_html=True,
    )
