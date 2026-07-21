"""BuilderForge - DealFlow Page.

Opportunity discovery and market research deep-dive.
Shows grants, competitors, trends, and audience insights.
"""

import streamlit as st
import json

from utils.state import init_session_state, get_current_project
from ui.styles import apply_theme, status_badge
from ui.components import render_header, render_phase_output, render_action_button, render_metric_card, render_app_nav
from tools.research_tools import search_web_for_opportunities, find_applicable_grants, analyze_competitors

st.set_page_config(page_title="BuilderForge - DealFlow", page_icon="💼", layout="wide")
apply_theme()
init_session_state()
main_col = render_app_nav("pages/3_DealFlow.py")
with main_col:

    # ---------------------------------------------------------------------------
    # Main Content
    # ---------------------------------------------------------------------------

    render_header("DealFlow", "Opportunity discovery & market intelligence engine")

    project = get_current_project()

    if not project:
        st.warning("No project selected. Create one first!")
        st.page_link("pages/1_New_Project.py", label="→ Create a New Project", icon="🚀")
        st.stop()

    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # ---------------------------------------------------------------------------
    # Tabbed DealFlow View
    # ---------------------------------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 Market Research",
        "🏆 Grant Opportunities",
        "⚔️ Competitor Analysis",
        "👥 Target Audiences",
    ])

    with tab1:
        st.markdown("## Market Research")
        st.caption(f"Analysing market for: **{project.title}**")

        if st.button("🔍 RUN MARKET RESEARCH", key="run_research", use_container_width=True):
            with st.spinner("Researcher agent scanning markets..."):
                result = search_web_for_opportunities(project.description)
                data = json.loads(result)
                project.opportunity_report["market_research"] = data
                from utils.state import save_project
                save_project(project)
                st.success("Market research complete!")

        # Show cached results
        mr = project.opportunity_report.get("market_research", {})
        if mr and isinstance(mr, dict):
            for r in mr.get("results", []):
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                            <div style="font-weight: 700; color: #ffffff;">{r.get('source')} — {r.get('title')}</div>
                            <div style="font-size: 0.65rem; color: #FF4D00; font-weight: 700; letter-spacing: 0.05em;">RELEVANCE: {r.get('relevance', 0)*100:.0f}%</div>
                        </div>
                        <div style="color: #94A3B8; font-size: 0.85rem; line-height: 1.6;">{r.get('snippet')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab2:
        st.markdown("## Grant & Funding Opportunities")
        st.caption("Discover grants, subsidies, and hackathon prizes for your project")

        if st.button("💰 FIND GRANTS", key="find_grants", use_container_width=True):
            with st.spinner("Searching grant databases..."):
                result = find_applicable_grants(project.description, project.category)
                data = json.loads(result)
                project.opportunity_report["grants"] = data
                from utils.state import save_project
                save_project(project)
                st.success(f"Found {len(data.get('opportunities', []))} grant opportunities!")

        grants = project.opportunity_report.get("grants", {})
        if grants and isinstance(grants, dict):
            total = grants.get("total_funding_available", 0)
            if total:
                render_metric_card("Total Funding Available", f"${total:,}")

            st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

            for opp in grants.get("opportunities", []):
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; color: #ffffff;">{opp.get('name')}</div>
                            <div style="font-size: 0.75rem; color: #64748B; margin-top: 0.25rem;">Focus: {opp.get('focus', 'N/A')} | Deadline: {opp.get('deadline', 'Open')}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: 700; color: #FF4D00; font-size: 1.1rem;">{opp.get('amount', 'N/A')}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
            rec = grants.get("recommendation")
            if rec:
                st.markdown(
                    f"""
                    <div style="background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.1); border-radius: 12px; padding: 1.5rem; margin-top: 2rem;">
                        <div style="font-size: 0.7rem; font-weight: 700; color: #10B981; text-transform: uppercase; margin-bottom: 0.5rem;">Recommendation</div>
                        <div style="color: #E2E8F0; font-size: 0.9rem; line-height: 1.6;">{rec}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with tab3:
        st.markdown("## Competitor Analysis")
        st.caption("Understand the competitive landscape")

        if st.button("⚔️ ANALYSE COMPETITORS", key="run_competitors", use_container_width=True):
            with st.spinner("Analysing competitive landscape..."):
                result = analyze_competitors(project.category)
                data = json.loads(result)
                project.opportunity_report["competitors"] = data
                from utils.state import save_project
                save_project(project)
                st.success("Competitor analysis complete!")

        comp = project.opportunity_report.get("competitors", {})
        if comp and isinstance(comp, dict):
            st.info(f"**TAM:** {comp.get('total_addressable_market', 'N/A')}")
        
            for c in comp.get("competitors", []):
                with st.expander(f"{c.get('name')} — {c.get('type', '')}"):
                    st.markdown("**Strengths:**")
                    for s in c.get("strengths", []):
                        st.markdown(f"✅ {s}")
                    st.markdown("**Weaknesses:**")
                    for w in c.get("weaknesses", []):
                        st.markdown(f"❌ {w}")

    with tab4:
        st.markdown("## Target Audiences")
        st.caption("Who should you build for?")

        if st.button("👥 FIND AUDIENCES", key="find_audience", use_container_width=True):
            with st.spinner("Profiling target audiences..."):
                from tools.research_tools import find_target_audience
                result = find_target_audience(project.title)
                data = json.loads(result)
                project.opportunity_report["target_audience"] = data
                from utils.state import save_project
                save_project(project)
                st.success("Audience profiles generated!")

        audience = project.opportunity_report.get("target_audience", {})
        if audience and isinstance(audience, dict):
            for seg in audience.get("audiences", []):
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                        <h3 style="margin-top: 0 !important;">{seg.get('segment')}</h3>
                        <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.6;">
                            <strong>Pain Point:</strong> {seg.get('pain_point', 'N/A')}<br>
                            <strong>Size:</strong> {seg.get('size', 'N/A')}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
            gtm = audience.get("go_to_market")
            if gtm:
                st.markdown(
                    f"""
                    <div style="background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 12px; padding: 1.5rem; margin-top: 2rem;">
                        <div style="font-size: 0.7rem; font-weight: 700; color: #38BDF8; text-transform: uppercase; margin-bottom: 0.5rem;">Go-to-Market Strategy</div>
                        <div style="color: #E2E8F0; font-size: 0.9rem; line-height: 1.6;">{gtm}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #334155; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; padding-bottom: 2rem;">
            BuilderForge — AI Genesis Hackathon 2026
        </div>
        """,
        unsafe_allow_html=True,
    )
