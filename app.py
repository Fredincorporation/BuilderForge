"""BuilderForge - Pixel-accurate Homepage (Streamlit)

This page replicates the provided screenshot: dark theme, orange accents,
left sidebar navigation, centered hero, execution pipeline, feature cards,
tech row and footer. Uses the shared `ui.styles` CSS and `ui.components` helper.
"""

import streamlit as st
import time
from dotenv import load_dotenv

from utils.state import init_session_state
from ui.styles import apply_theme, phase_stepper
from ui.components import render_sidebar, render_status_card

load_dotenv()

# Page config
st.set_page_config(
    page_title="BuilderForge - Home",
    page_icon="🔨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Theme + state
apply_theme()
init_session_state()

# Sidebar (left nav)
with st.sidebar:
    render_sidebar("app.py")
    st.markdown("<hr class='bf-sidebar-divider'>", unsafe_allow_html=True)
    render_status_card()

# Hero
st.markdown(
    """
    <div class="hero-section">
        <div class="hero-badge">OKX AI Genesis Hackathon MVP</div>
        <h1 class="hero-title">BuilderForge</h1>
        <p class="hero-copy">The Autonomous Idea-to-Launch Agent for the OKX Ecosystem. Transform vision into architecture in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# CTA buttons (styled to match screenshot but functional)
col1, col2, col3 = st.columns([1, 0.45, 0.45])
with col1:
    st.write("")
with col2:
    if st.button("Start New Project", key="start_new", use_container_width=True, type="primary"):
        st.session_state["started"] = True
with col3:
    if st.button("Explore DealFlow", key="explore", use_container_width=True):
        st.session_state["explore"] = True

st.markdown("<div class='home-pipeline-space'></div>", unsafe_allow_html=True)

# Execution pipeline
st.markdown(
    """
    <div class="section-heading">
        <div class="section-label">Execution Pipeline</div>
        <div class="section-divider"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

phases = ["Idea Input", "Research", "Creation", "Execution", "Analysis"]
current_phase = st.session_state.get("current_phase", phases[0])
phase_stepper(current_phase, phases)

# If user started a new project, simulate multi-agent flow progress
if st.session_state.get("started"):
    st.info("Launching BuilderForge crew — simulating steps...")
    progress = st.progress(0)
    for i, p in enumerate(phases):
        st.session_state["current_phase"] = p
        phase_stepper(p, phases)
        for j in range(20):
            progress.progress(int((i * 20 + j + 1) / (len(phases) * 20) * 100))
            time.sleep(0.02)
        st.success(f"{p} complete")
    st.balloons()
    st.session_state["started"] = False
    del st.session_state["current_phase"]

# Feature cards
st.markdown(
    """
    <div class="feature-row">
        <div class="feature-card">
            <div class="feature-card-icon feature-card-icon-agents"><i class="ti ti-users"></i></div>
            <h3>5 Specialized Agents</h3>
            <p>Coordinator, Researcher, Creator, Executor, and Analyzer work in perfect sync to handle the complexity of your deployment.</p>
        </div>
        <div class="feature-card">
            <div class="feature-card-icon feature-card-icon-testnet"><i class="ti ti-cube"></i></div>
            <h3>OKX Testnet Integration</h3>
            <p>Simulate token deployment and smart contract interactions on OKC testnet with precision gas estimation.</p>
        </div>
        <div class="feature-card">
            <div class="feature-card-icon feature-card-icon-asp"><i class="ti ti-currency-dollar"></i></div>
            <h3>ASP Ready</h3>
            <p>Seamlessly list on the OKX.AI marketplace with pre-structured manifests and dynamic pricing capabilities.</p>
        </div>
    </div>

    <div class="tech-bar">
        <span class="tech-pill">PYTHON</span>
        <span class="tech-pill">CREWAI</span>
        <span class="tech-pill">LANGCHAIN</span>
        <span class="tech-pill">STREAMLIT</span>
        <span class="tech-pill">CLAUDE</span>
        <span class="tech-pill">OKX WEB3</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='home-footer-space'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="home-footer">
        <p>BuilderForge · AI Genesis Hackathon 2026 &nbsp;&nbsp; • &nbsp;&nbsp; <a href="#">Documentation</a> &nbsp;&nbsp; <a href="#">GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True,
)
