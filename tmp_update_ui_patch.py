from pathlib import Path

app_path = Path('app.py')
styles_path = Path('ui/styles.py')
app_text = app_path.read_text(encoding='utf-8')
start_marker = '    # Hero\n'
end_marker = '    st.markdown("<div class=\'home-footer-space\'></div>", unsafe_allow_html=True)\n'
start = app_text.find(start_marker)
end = app_text.find(end_marker, start)
if start == -1 or end == -1:
    raise SystemExit('Homepage block markers not found in app.py')
end += len(end_marker)
new_home = '''    # Hero
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
'''
app_path.write_text(app_text[:start] + new_home + app_text[end:], encoding='utf-8')

styles_text = styles_path.read_text(encoding='utf-8')
css_start = styles_text.find('COMMAND_DECK_CSS = """')
if css_start == -1:
    raise SystemExit('COMMAND_DECK_CSS start not found in ui/styles.py')
css_end = styles_text.find('"""\n\n\ndef apply_theme()', css_start)
if css_end == -1:
    raise SystemExit('COMMAND_DECK_CSS end not found in ui/styles.py')
css_end += len('"""')
new_css = '''COMMAND_DECK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont/tabler-icons.min.css');

    * {
        box-sizing: border-box;
    }

    html, body {
        margin: 0;
        min-height: 100%;
        background: #070B17 !important;
        color: #F8FAFC !important;
        font-family: 'Inter', sans-serif !important;
    }

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMainBlockContainer"],
    .block-container,
    .main {
        background: #070B17 !important;
        color: #F8FAFC !important;
    }

    .stApp::before {
        content: '' !important;
        position: fixed !important;
        inset: 0 !important;
        background: radial-gradient(circle at top left, rgba(255, 77, 0, 0.16), transparent 26%), radial-gradient(circle at bottom right, rgba(56, 189, 248, 0.12), transparent 24%), #070B17 !important;
        z-index: -1 !important;
        pointer-events: none !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        margin: 0;
    }

    p, span, li, td, th, label, input, textarea, button, a {
        color: #CBD5E1 !important;
    }

    a {
        color: inherit !important;
        text-decoration: none !important;
    }

    .card {
        background: rgba(15, 23, 42, 0.82) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.25) !important;
    }

    .card-header {
        padding: 1.75rem 1.75rem 0 1.75rem !important;
    }

    .card-title {
        font-size: 1rem !important;
        font-weight: 700 !important;
        margin-top: 0.75rem !important;
        color: #F8FAFC !important;
    }

    .badge {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0.45rem 0.85rem !important;
        border-radius: 999px !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
    }

    .badge-secondary {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    .btn {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 700 !important;
        padding: 0.95rem 1.6rem !important;
        border-radius: 14px !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease !important;
        min-width: 170px !important;
        text-decoration: none !important;
    }

    .btn-primary {
        background: #FF4D00 !important;
        color: #FFFFFF !important;
        box-shadow: 0 18px 40px rgba(255, 77, 0, 0.28) !important;
    }

    .btn-primary:hover {
        background: #ff5e1f !important;
        transform: translateY(-1px) !important;
    }

    .btn-secondary {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #FFFFFF !important;
        border-color: rgba(255, 255, 255, 0.14) !important;
    }

    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }

    .hero-grid {
        display: grid !important;
        grid-template-columns: 1.25fr 1fr !important;
        gap: 2rem !important;
        align-items: center !important;
        margin: 1.5rem auto 0 auto !important;
        max-width: 1180px !important;
    }

    .hero-copy {
        display: flex !important;
        flex-direction: column !important;
        gap: 1.35rem !important;
    }

    .hero-badge {
        display: inline-flex !important;
        padding: 0.65rem 1.2rem !important;
        border-radius: 999px !important;
        background: rgba(255, 77, 0, 0.14) !important;
        color: #FFB380 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
    }

    .hero-title {
        font-size: clamp(3rem, 5vw, 4.8rem) !important;
        line-height: 0.95 !important;
        letter-spacing: -0.06em !important;
        color: #FFFFFF !important;
    }

    .hero-text {
        max-width: 680px !important;
        font-size: 1.05rem !important;
        line-height: 1.9 !important;
        color: #CBD5E1 !important;
    }

    .hero-actions {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 1rem !important;
    }

    .hero-metrics {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 0.85rem !important;
    }

    .metric-pill {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 1rem 1rem !important;
        color: #CBD5E1 !important;
        font-size: 0.87rem !important;
    }

    .metric-pill strong {
        display: block !important;
        color: #FFFFFF !important;
        font-size: 1.15rem !important;
        margin-bottom: 0.25rem !important;
    }

    .hero-panel {
        display: flex !important;
        flex-direction: column !important;
        gap: 1.5rem !important;
        padding: 1.8rem !important;
    }

    .pipeline-preview {
        display: grid !important;
        grid-template-columns: repeat(5, minmax(0, 1fr)) !important;
        gap: 0.9rem !important;
    }

    .pipeline-step {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        text-align: center !important;
        font-size: 0.85rem !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
    }

    .pipeline-step.active {
        background: #FF4D00 !important;
        color: #0B1225 !important;
        border-color: rgba(255, 77, 0, 0.28) !important;
    }

    .pipeline-copy {
        color: #CBD5E1 !important;
        font-size: 0.95rem !important;
        line-height: 1.8 !important;
    }

    .section-spacer {
        height: 3rem !important;
    }

    .stats-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)) !important;
        gap: 1rem !important;
        margin: 2rem 0 !important;
        max-width: 1180px !important;
        width: 100% !important;
    }

    .stats-card {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 22px !important;
        padding: 1.4rem 1.5rem !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 0.55rem !important;
    }

    .stats-number {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }

    .stats-label {
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
    }

    .section-heading {
        margin-top: 3.25rem !important;
        margin-bottom: 1.25rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 1rem !important;
        flex-wrap: wrap !important;
    }

    .section-label {
        background: rgba(255, 77, 0, 0.14) !important;
        color: #FFB380 !important;
        padding: 0.55rem 0.9rem !important;
        border-radius: 999px !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.16em !important;
        text-transform: uppercase !important;
    }

    .section-divider {
        flex: 1 1 auto !important;
        height: 1px !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }

    .work-grid {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)) !important;
        gap: 1rem !important;
    }

    .work-step-card {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        padding: 1.6rem !important;
        transition: transform 0.25s ease !important;
    }

    .work-step-card:hover {
        transform: translateY(-4px) !important;
    }

    .work-step-card strong {
        display: block !important;
        margin-bottom: 0.75rem !important;
        color: #FFFFFF !important;
        font-size: 0.95rem !important;
    }

    .work-step-card p {
        margin: 0 !important;
        color: #CBD5E1 !important;
        line-height: 1.75 !important;
    }

    .feature-row {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)) !important;
        gap: 1rem !important;
        margin-top: 1.75rem !important;
    }

    .feature-card {
        padding: 1.8rem !important;
        border-radius: 24px !important;
        background: rgba(15, 23, 42, 0.78) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        min-height: 240px !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 1rem !important;
    }

    .feature-card-icon {
        width: 46px !important;
        height: 46px !important;
        border-radius: 16px !important;
        display: grid !important;
        place-items: center !important;
        background: rgba(255, 255, 255, 0.06) !important;
        color: #FFB380 !important;
        font-size: 1.1rem !important;
    }

    .feature-card h3 {
        margin: 0 !important;
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
    }

    .feature-card p {
        margin: 0 !important;
        color: #CBD5E1 !important;
        line-height: 1.75 !important;
        font-size: 0.95rem !important;
    }

    .tech-bar {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.85rem !important;
        margin-top: 1.75rem !important;
        padding-top: 1.5rem !important;
        border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .tech-pill {
        padding: 0.55rem 0.9rem !important;
        border-radius: 999px !important;
        background: rgba(255, 255, 255, 0.04) !important;
        color: #94A3B8 !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
    }

    .cta-banner {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: space-between !important;
        align-items: center !important;
        gap: 1rem !important;
        padding: 1.8rem !important;
        margin-top: 2rem !important;
        border-radius: 24px !important;
        background: rgba(255, 77, 0, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    .cta-banner h2 {
        margin: 0 !important;
        font-size: 1.55rem !important;
        color: #FFFFFF !important;
    }

    .cta-banner p {
        margin: 0.85rem 0 0 !important;
        color: #CBD5E1 !important;
        max-width: 720px !important;
        line-height: 1.75 !important;
    }

    .cta-actions {
        display: flex !important;
        gap: 1rem !important;
        flex-wrap: wrap !important;
    }

    .footer-row {
        margin-top: 3rem !important;
        padding-bottom: 2rem !important;
        color: #94A3B8 !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.16em !important;
    }

    .footer-row a {
        color: #E2E8F0 !important;
    }

    .bf-stepper {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)) !important;
        gap: 0.95rem !important;
        margin-top: 1rem !important;
    }

    .bf-step {
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background: rgba(255, 255, 255, 0.04) !important;
        padding: 1rem !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 0.85rem !important;
        min-height: 120px !important;
    }

    .bf-step-active {
        background: rgba(255, 77, 0, 0.2) !important;
        border-color: rgba(255, 77, 0, 0.3) !important;
    }

    .bf-step-done {
        background: rgba(16, 185, 129, 0.12) !important;
        border-color: rgba(16, 185, 129, 0.22) !important;
    }

    .bf-step-circle {
        width: 48px !important;
        height: 48px !important;
        border-radius: 999px !important;
        background: rgba(255, 255, 255, 0.08) !important;
        display: grid !important;
        place-items: center !important;
        color: #FFFFFF !important;
    }

    .bf-step-label {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        text-align: center !important;
        font-size: 0.95rem !important;
    }

    @media (max-width: 1024px) {
        .hero-grid {
            grid-template-columns: 1fr !important;
        }

        .hero-metrics {
            grid-template-columns: 1fr 1fr !important;
        }

        .pipeline-preview {
            grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        }
    }

    @media (max-width: 720px) {
        .hero-actions, .cta-actions {
            flex-direction: column !important;
            width: 100% !important;
        }

        .hero-metrics, .stats-grid, .feature-row, .work-grid {
            grid-template-columns: 1fr !important;
        }

        .btn {
            width: 100% !important;
        }
    }
</style>
"""
'''
styles_path.write_text(styles_text[:css_start] + new_css + styles_text[css_end:], encoding='utf-8')
print('Updated app.py and ui/styles.py successfully.')
