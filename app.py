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
from ui.components import render_app_nav

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
main_col = render_app_nav("app.py")
with main_col:

    # Hero
    st.markdown(
        """
        <div class="hero-grid">
            <div class="hero-copy">
                <span class="hero-badge">OKX AI Genesis Hackathon MVP</span>
                <h1 class="hero-title">BuilderForge</h1>
                <p class="hero-text">The autonomous idea-to-launch platform for the OKX ecosystem. Convert concepts into deployable architecture, smart contract strategy, and launch-ready assets in minutes.</p>
                <div class="hero-actions">
                    <a href="/New_Project" class="btn btn-primary">Start New Project</a>
                    <a href="/DealFlow" class="btn btn-secondary">Explore DealFlow</a>
                </div>
                <div class="hero-metrics">
                    <div class="metric-pill"><strong>5</strong> Specialized Agents</div>
                    <div class="metric-pill"><strong>OKX</strong> Native Testnet</div>
                    <div class="metric-pill"><strong>ASP</strong> Marketplace Ready</div>
                </div>
            </div>
            <div class="hero-panel card">
                <div class="card-header">
                    <span class="badge badge-secondary">Pipeline preview</span>
                    <h2 class="card-title">AI launch flow</h2>
                </div>
                <div class="pipeline-preview">
                    <div class="pipeline-step active">Concept</div>
                    <div class="pipeline-step">Research</div>
                    <div class="pipeline-step">Design</div>
                    <div class="pipeline-step">Deploy</div>
                    <div class="pipeline-step">Analyze</div>
                </div>
                <p class="pipeline-copy">BuilderForge orchestrates ideation, architecture, and execution into a single continuous flow tuned for OKX launch readiness.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="stats-grid">
            <div class="stats-card">
                <span class="stats-number">120+</span>
                <span class="stats-label">Projects Scoped</span>
            </div>
            <div class="stats-card">
                <span class="stats-number">5</span>
                <span class="stats-label">AI Crew Agents</span>
            </div>
            <div class="stats-card">
                <span class="stats-number">98%</span>
                <span class="stats-label">Workflow Accuracy</span>
            </div>
            <div class="stats-card">
                <span class="stats-number">ASP Ready</span>
                <span class="stats-label">Marketplace Ready</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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

    st.markdown(
        """
        <div class="section-heading">
            <div class="section-label">How it works</div>
            <div class="section-divider"></div>
        </div>
        <div class="work-grid">
            <div class="work-step-card">
                <strong>01 — Seed & scope</strong>
                <p>Describe your idea and BuilderForge crafts a structured OKX launch brief, goals, chain targets, and deployment strategy.</p>
            </div>
            <div class="work-step-card">
                <strong>02 — Research & design</strong>
                <p>Specialized agents evaluate product fit, architecture, and token mechanics while preparing launch assets.</p>
            </div>
            <div class="work-step-card">
                <strong>03 — Build & deploy</strong>
                <p>Execute smart contract generation, OKX testnet readiness, and ASP packaging in one AI-guided flow.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-heading">
            <div class="section-label">Core capabilities</div>
            <div class="section-divider"></div>
        </div>
        <div class="feature-row">
            <div class="feature-card card">
                <div class="feature-card-icon"><i class="ti ti-users"></i></div>
                <h3>AI crew coordination</h3>
                <p>Five focused agents align research, creation, execution, and analysis for a smooth launch.</p>
            </div>
            <div class="feature-card card">
                <div class="feature-card-icon"><i class="ti ti-cube"></i></div>
                <h3>OKX-native readiness</h3>
                <p>Generate OKC-compatible deployment plans and simulated transactions for lower friction launches.</p>
            </div>
            <div class="feature-card card">
                <div class="feature-card-icon"><i class="ti ti-currency-dollar"></i></div>
                <h3>ASP marketplace flow</h3>
                <p>Build path-to-market assets and packaging for OKX.AI listing readiness.</p>
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

        <div class="cta-banner card">
            <div>
                <h2>Launch with the OKX AI design system</h2>
                <p>From ideation to ASP-ready launch assets, BuilderForge keeps your workflow aligned and deployment-ready for the next generation of Web3 products.</p>
            </div>
            <div class="cta-actions">
                <a href="/New_Project" class="btn btn-primary">Launch Your Idea</a>
                <a href="/Dashboard" class="btn btn-secondary">View Dashboard</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="home-footer">
            <p>BuilderForge &middot; AI Genesis Hackathon 2026 &nbsp;&nbsp; &bull; &nbsp;&nbsp; <a href="#">Documentation</a> &nbsp;&nbsp; <a href="#">GitHub</a></p>
        </div>
        """,
        unsafe_allow_html=True,
    )
