"""BuilderForge Reusable UI Components.

Streamlit widgets styled with the refined Command Deck theme.
"""

import streamlit as st
import json
from typing import Any, Dict, List, Optional, Callable
from datetime import datetime

from utils.state import ProjectData, ProjectPhase


def render_header(title: str, subtitle: Optional[str] = None) -> None:
    """Render a page header with logo and title."""
    st.markdown(
        f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="margin-bottom: 0.5rem !important;">{title}</h1>
            {f'<p style="font-size: 1.1rem; color: #94A3B8 !important; margin-top: 0 !important;">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metric_card(label: str, value: str, delta: Optional[str] = None) -> None:
    """Render a single metric card with optional delta."""
    st.metric(label=label, value=value, delta=delta)


def render_project_card(project: ProjectData, on_click: Optional[Callable] = None) -> None:
    """Render a project card for the dashboard."""
    st.markdown(
        f"""
        <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; backdrop-filter: blur(8px);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                    <h3 style="margin: 0 !important; color: #ffffff !important;">{project.title}</h3>
                    <p style="font-size: 0.85rem; color: #94A3B8 !important; margin-top: 0.25rem !important;">{project.description[:120]}...</p>
                </div>
                <div style="text-align: right;">
                    <span style="font-size: 0.7rem; font-weight: 700; color: #FF4D00; text-transform: uppercase;">{project.phase}</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="flex-grow: 1; height: 6px; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden;">
                    <div style="width: {int(project.progress * 100)}%; height: 100%; background: #FF4D00; box-shadow: 0 0 10px rgba(255,77,0,0.5);"></div>
                </div>
                <span style="font-size: 0.8rem; font-weight: 600; color: #ffffff;">{int(project.progress * 100)}%</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button(f"OPEN PROJECT →", key=f"open_{project.id}", use_container_width=True):
        if on_click:
            on_click(project.id)


def render_phase_output(phase_name: str, data: Dict[str, Any], icon: str = "📋") -> None:
    """Render a collapsible phase output section."""
    with st.expander(f"{icon} {phase_name} Output", expanded=True):
        if not data:
            st.info("No output generated yet. Run the crew to produce results.")
            return

        for key, value in data.items():
            st.markdown(f"<div style='margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 0.5rem;'>{key.replace('_', ' ')}</div>", unsafe_allow_html=True)
            
            if isinstance(value, str):
                st.markdown(f"<div style='background: rgba(15, 23, 42, 0.4); padding: 1rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.03); color: #E2E8F0; line-height: 1.6;'>{value}</div>", unsafe_allow_html=True)
            elif isinstance(value, list):
                for item in value:
                    st.markdown(f"<div style='background: rgba(15, 23, 42, 0.4); padding: 0.75rem; border-radius: 8px; border: 1px solid rgba(255,255,255,0.03); margin-bottom: 0.5rem; color: #E2E8F0;'>{item}</div>", unsafe_allow_html=True)
            elif isinstance(value, dict):
                st.json(value)
            else:
                st.markdown(f"<div style='color: #E2E8F0;'>{value}</div>", unsafe_allow_html=True)
            st.markdown(f"</div>", unsafe_allow_html=True)


def render_transaction_card(tx: Dict[str, Any]) -> None:
    """Render a blockchain transaction card."""
    status_icon = "ti-check" if tx.get("status") == "simulated_success" else "ti-loader"
    status_color = "#10B981" if tx.get("status") == "simulated_success" else "#64748B"
    
    st.markdown(
        f"""
        <div style="background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.03); border-radius: 8px; padding: 1rem; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 1rem;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: rgba(255,255,255,0.03); display: flex; align-items: center; justify-content: center; color: {status_color};">
                <i class="ti {status_icon}" style="font-size: 1.2rem;"></i>
            </div>
            <div style="flex-grow: 1;">
                <div style="font-family: monospace; font-size: 0.85rem; color: #ffffff;">{tx.get('hash', 'N/A')[:24]}...</div>
                <div style="font-size: 0.7rem; color: #64748B;">To: {tx.get('to', 'N/A')[:16]}...</div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 700; color: #ffffff; font-size: 0.9rem;">{tx.get('value', '0')} OKT</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_chat_message(role: str, content: str, agent_name: str = "") -> None:
    """Render a styled message for the agent chat interface."""
    # Standard Streamlit chat message with custom logic for agent name
    with st.chat_message(role):
        if agent_name:
            st.markdown(f"<div style='font-size: 0.7rem; font-weight: 700; color: #FF4D00; text-transform: uppercase; margin-bottom: 0.25rem;'>{agent_name}</div>", unsafe_allow_html=True)
        st.markdown(content)


def render_action_button(
    label: str,
    key: str,
    icon: str = "🚀",
    disabled: bool = False,
    help_text: Optional[str] = None,
) -> bool:
    """Render a styled action button."""
    btn_label = f"{icon} {label}"
    return st.button(btn_label, key=key, disabled=disabled, help=help_text, use_container_width=True)


def render_export_options(project: ProjectData) -> None:
    """Render export buttons for project outputs."""
    st.markdown("### 📦 Export Options")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 JSON", key="export_json", use_container_width=True):
            export_data = {
                "project": {
                    "id": project.id,
                    "title": project.title,
                    "description": project.description,
                    "goals": project.goals,
                    "phase": project.phase,
                    "created_at": project.created_at,
                },
                "opportunity_report": project.opportunity_report,
                "launch_assets": project.launch_assets,
                "deployment_plan": project.deployment_plan,
                "metrics_report": project.metrics_report,
                "transactions": project.transactions,
            }
            st.download_button(
                label="💾 DOWNLOAD",
                data=json.dumps(export_data, indent=2),
                file_name=f"builderforge_{project.id}.json",
                mime="application/json",
                key="download_json",
                use_container_width=True,
            )

    with col2:
        st.button("📝 MARKDOWN", key="export_md", disabled=True, use_container_width=True,
                  help="Markdown export coming soon")

    with col3:
        st.button("📸 PDF", key="export_pdf", disabled=True, use_container_width=True,
                  help="PDF export coming soon")


def render_sidebar(current_file: str) -> None:
    """Render the premium Command Deck sidebar navigation."""
    st.markdown(
        """
        <div class="bf-sidebar-brand">
            <div class="bf-sidebar-brand-row">
                <div class="bf-sidebar-logo"><i class="ti ti-hammer"></i></div>
                <span class="bf-sidebar-name">BuilderForge</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='bf-sidebar-label'>Navigation</div>", unsafe_allow_html=True)

    pages = {
        "Home": ("app.py", "ti-home"),
        "New Project": ("pages/1_New_Project.py", "ti-plus"),
        "Dashboard": ("pages/2_Dashboard.py", "ti-layout-dashboard"),
        "DealFlow": ("pages/3_DealFlow.py", "ti-briefcase"),
        "LaunchPad": ("pages/4_LaunchPad.py", "ti-rocket"),
        "OKX ASP Listing": ("pages/5_OKX_ASP_Listing.py", "ti-link"),
    }

    for label, (path, icon) in pages.items():
        is_active = current_file in path
        cls = "nav-active" if is_active else ""
        st.markdown(f"<div class='bf-sidebar-item {cls}'>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='bf-sidebar-content'><i class='ti {icon}'></i><span>{label}</span></div>",
            unsafe_allow_html=True,
        )
        if st.button(" ", key=f"nav_{path}", use_container_width=True):
            st.switch_page(path)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    projects = st.session_state.get("projects", [])
    if projects:
        st.markdown("<div style='font-size: 0.65rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem; padding-left: 1rem;'>Active Projects</div>", unsafe_allow_html=True)
        for p in projects[-3:]:
            st.markdown(
                f"""
                <div style="padding: 0.5rem 1rem; margin-bottom: 0.5rem; background: rgba(255,255,255,0.02); border-radius: 6px;">
                    <div style="font-size: 0.8rem; color: white; font-weight: 500;">{p.title}</div>
                    <div style="font-size: 0.7rem; color: #64748B;">{int(p.progress * 100)}% complete</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_status_card() -> None:
    """Render the system status card at the bottom of the sidebar."""
    st.markdown(
        """
        <div class="bf-system-status">
            <div class="bf-system-status-heading">
                <div class="bf-system-status-dot"></div>
                <span>System Online</span>
            </div>
            <div class="bf-system-status-version">v1.2.4 — Simulated Mode</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_wallet_status(address: str, balance: str = "0") -> None:
    """Render wallet connection status."""
    if address:
        short_addr = address[:8] + "..." + address[-4:]
        st.markdown(
            f"""
            <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background: #10B981; box-shadow: 0 0 10px #10B981;"></div>
                    <span style="color: #10B981; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;">Connected</span>
                </div>
                <div style="font-family: monospace; font-size: 0.9rem; color: #ffffff; margin-bottom: 0.25rem;">{short_addr}</div>
                <div style="font-size: 0.8rem; font-weight: 600; color: #94A3B8;">{balance} <span style="color: #64748B;">OKT</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 1rem; text-align: center;">
                <span style="color: #EF4444; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;">Disconnected</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_top_nav(current_file: str) -> None:
    """Render a top navigation bar with links to all sub-pages.

    Uses Streamlit page_link for actual navigation.
    """
    pages = [
        ("Dashboard", "pages/2_Dashboard.py"),
        ("New Project", "pages/1_New_Project.py"),
        ("DealFlow", "pages/3_DealFlow.py"),
        ("LaunchPad", "pages/4_LaunchPad.py"),
        ("OKX ASP", "pages/5_OKX_ASP_Listing.py"),
    ]

    # Visual nav bar (decorative HTML)
    links_html = ""
    for label, path in pages:
        active_class = " nav-top-active" if current_file == path else ""
        links_html += f'<span class="nav-top-link{active_class}">{label}</span>'

    st.markdown(
        f"""
        <div class="top-nav">
            <div class="top-nav-inner">
                <div class="top-nav-brand">
                    <div class="top-nav-logo">
                        <i class="ti ti-hammer"></i>
                    </div>
                    <span class="top-nav-brand-text">BuilderForge</span>
                </div>
                <div class="top-nav-links">
                    {links_html}
                </div>
            </div>
        </div>
        <div class="top-nav-spacer"></div>
        """,
        unsafe_allow_html=True,
    )

    # Use a single row of page_link components
    # These are the actual interactive elements
    cols = st.columns(len(pages))
    for i, (label, path) in enumerate(pages):
        with cols[i]:
            st.page_link(path, label=f"→ {label}", use_container_width=True)
