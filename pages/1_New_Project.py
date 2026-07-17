"""BuilderForge - New Project Page.

Idea input and project creation step.
User enters their idea, goals, and triggers the AI pipeline.
"""

import streamlit as st
from datetime import datetime

from utils.state import (
    init_session_state,
    ProjectData,
    ProjectPhase,
    save_project,
    new_project_id,
    add_crew_log,
    clear_crew_log,
)
from ui.styles import apply_theme, phase_stepper, console_log
from ui.components import render_header, render_action_button, render_sidebar, render_status_card

# Page config
st.set_page_config(
    page_title="BuilderForge - New Project",
    page_icon="🔨",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
init_session_state()

# ---------------------------------------------------------------------------
# Sidebar Navigation (Consistent)
# ---------------------------------------------------------------------------

with st.sidebar:
    render_sidebar("pages/1_New_Project.py")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.65rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 1rem; padding-left: 0.5rem;'>Settings</div>", unsafe_allow_html=True)

    use_simulated = st.toggle("Simulated Mode", value=True, help="No API keys required")
    st.session_state["use_simulated"] = use_simulated

    render_status_card()

# ---------------------------------------------------------------------------
# Main Content
# ---------------------------------------------------------------------------

render_header(
    "New Project",
    "Describe your vision and let the agents handle the architecture."
)

st.markdown("<div style='margin-bottom: 3rem;'></div>", unsafe_allow_html=True)

# Form Container
with st.container():
    st.markdown(
        """
        <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 2.5rem; backdrop-filter: blur(8px);">
            <h2 style="margin-top: 0 !important; font-size: 1.5rem !important;">What are you building?</h2>
        """,
        unsafe_allow_html=True
    )

    with st.form("new_project_form_deck", clear_on_submit=False):
        title = st.text_input(
            "Project Name *",
            placeholder="e.g., AI-Powered Yield Aggregator",
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            category = st.selectbox(
                "Category",
                options=["DeFi", "AI/ML", "Infrastructure", "SocialFi", "NFT/Gaming", "DAO", "Other"],
            )
        with col2:
            target_chain = st.selectbox(
                "Target Chain",
                options=["OKC", "Ethereum", "Polygon", "Base", "Solana"],
            )

        description = st.text_area(
            "Describe your idea in detail *",
            placeholder="What problem does it solve? Who is it for? How does it work?",
            height=150,
        )

        st.markdown(
            """
            <div style="display: flex; gap: 0.75rem; margin-top: 0.5rem; margin-bottom: 1.5rem;">
                <span style="font-size: 0.7rem; color: #64748B; padding-top: 0.2rem;">Suggestions:</span>
                <span style="font-size: 0.65rem; padding: 0.2rem 0.6rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 4px; color: #94A3B8;">DeFi Dashboard</span>
                <span style="font-size: 0.65rem; padding: 0.2rem 0.6rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 4px; color: #94A3B8;">NFT Marketplace</span>
                <span style="font-size: 0.65rem; padding: 0.2rem 0.6rem; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); border-radius: 4px; color: #94A3B8;">DAO Tooling</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        goals_text = st.text_area(
            "Goals & Objectives",
            placeholder="List your goals, one per line (e.g., Launch ERC-20, Build community...)",
            height=100,
        )

        with st.expander("⚙️ Advanced Settings"):
            include_contract = st.checkbox("Generate Smart Contract", value=True)
            include_social = st.checkbox("Generate Social Media Copy", value=True)

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button(
            "LAUNCH BUILDERFORGE →",
            use_container_width=True,
            type="primary",
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Logic
# ---------------------------------------------------------------------------

if submitted:
    if not title or not description:
        st.error("Please provide both a project name and description.")
        st.stop()

    # Import dependencies for running crew
    from crew.builderforge_crew import run_simulated_crew, build_full_crew
    
    # Parse goals
    goals = [g.strip("- ").strip() for g in goals_text.split("\\n") if g.strip()]

    # Create project
    project = ProjectData(
        id=new_project_id(),
        title=title,
        description=description,
        goals=goals,
        category=category,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        phase=ProjectPhase.RESEARCH.value,
        progress=0.0,
    )
    save_project(project)
    st.session_state["current_project_id" ] = project.id
    clear_crew_log()

    # Run the crew
    with st.status("🤖 Initializing BuilderForge agents...", expanded=True) as status:
        try:
            use_sim = st.session_state.get("use_simulated", True)
            if use_sim:
                add_crew_log("🚀 Project created. Initializing agents...")
                project = run_simulated_crew(project)
            else:
                add_crew_log("🔄 Running real CrewAI pipeline...")
                crew = build_full_crew(verbose=True)
                crew.kickoff()

            save_project(project)
            status.update(label="✅ Architecture generation complete!", state="complete", expanded=False)
            st.success(f"✅ Project '{title}' is ready for review.")
            if st.button("GO TO DASHBOARD →", use_container_width=True):
                st.switch_page("pages/2_Dashboard.py")

        except Exception as e:
            status.update(label="❌ Pipeline failed", state="error")
            st.error(f"Error: {str(e)}")

st.markdown("<div style='margin-bottom: 4rem;'></div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div style="text-align: center; border-top: 1px solid #1E293B; padding-top: 2rem; margin-top: 4rem;">
        <div style="font-size: 0.65rem; font-weight: 700; color: #334155; text-transform: uppercase; letter-spacing: 0.1em; padding-bottom: 2rem;">
            BuilderForge — AI Genesis Hackathon 2026
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
