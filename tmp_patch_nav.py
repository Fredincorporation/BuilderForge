from pathlib import Path

root = Path('c:/Users/fred/Documents/GitHub/BuilderForge')

# 1) ui/components.py
comp = root / 'ui' / 'components.py'
text = comp.read_text(encoding='utf-8')
if 'def render_app_nav' not in text:
    append = '''

def render_app_nav(current_page: str):
    """Render the custom BuilderForge sidebar navigation panel."""
    pages = [
        ("Home", "app.py", "🏠"),
        ("New Project", "pages/1_New_Project.py", "➕"),
        ("Dashboard", "pages/2_Dashboard.py", "📊"),
        ("DealFlow", "pages/3_DealFlow.py", "💼"),
        ("LaunchPad", "pages/4_LaunchPad.py", "🚀"),
        ("OKX ASP Listing", "pages/5_OKX_ASP_Listing.py", "🔗"),
    ]

    nav_col, main_col = st.columns([0.18, 0.82], gap="small")
    with nav_col:
        st.markdown(
            """
            <div class="homepage-sidebar">
                <div class="sidebar-brand">
                    <div class="sidebar-logo"><i class="ti ti-hammer"></i></div>
                    <div>
                        <div class="sidebar-brand-name">BuilderForge</div>
                        <div class="sidebar-brand-sub">AI launch platform for OKX ecosystem services</div>
                    </div>
                </div>
                <div class="sidebar-nav-label">Navigation</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for label, path, icon in pages:
            if current_page == path:
                st.markdown(
                    f"""
                    <div class="sidebar-nav-item sidebar-nav-active">
                        <span class="sidebar-nav-icon">{icon}</span>
                        <span>{label}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.page_link(path, label=label, icon=icon, use_container_width=True)

    return main_col
'''
    text = text.rstrip() + '\n' + append
    comp.write_text(text, encoding='utf-8')

# 2) ui/styles.py
styles = root / 'ui' / 'styles.py'
text = styles.read_text(encoding='utf-8')
if '/* ===== CUSTOM BUILDERFORGE SIDEBAR NAV ===== */' not in text:
    css = """
    /* ===== CUSTOM BUILDERFORGE SIDEBAR NAV ===== */
    section[data-testid="stSidebar"] {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        min-width: 0 !important;
        overflow: hidden !important;
    }

    .homepage-sidebar {
        background: #060b18 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 28px !important;
        padding: 2rem 1.5rem !important;
        min-height: calc(100vh - 3rem) !important;
        position: sticky !important;
        top: 1.5rem !important;
        display: flex !important;
        flex-direction: column !important;
        gap: 1.3rem !important;
        box-shadow: 0 24px 80px rgba(0, 0, 0, 0.22) !important;
    }

    .sidebar-brand {
        display: flex !important;
        align-items: flex-start !important;
        gap: 0.9rem !important;
    }

    .sidebar-logo {
        width: 44px !important;
        height: 44px !important;
        border-radius: 16px !important;
        background: #FF4D00 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
    }

    .sidebar-brand-name {
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
    }

    .sidebar-brand-sub {
        color: #94A3B8 !important;
        font-size: 0.78rem !important;
        margin-top: 0.25rem !important;
        max-width: 220px !important;
    }

    .sidebar-nav-label {
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.22em !important;
        text-transform: uppercase !important;
        color: #64748B !important;
        margin-bottom: 0.6rem !important;
    }

    .sidebar-nav-icon {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 28px !important;
        height: 28px !important;
        margin-right: 0.85rem !important;
        font-size: 1rem !important;
    }

    .sidebar-nav-item,
    .homepage-sidebar .stButton > button,
    .homepage-sidebar .stPageLink > button {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        text-align: left !important;
        padding: 0.95rem 1rem !important;
        border-radius: 16px !important;
        color: #94A3B8 !important;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        gap: 0.85rem !important;
        transition: all 0.2s ease !important;
    }

    .sidebar-nav-item:hover:not(.sidebar-nav-active) {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #ffffff !important;
    }

    .sidebar-nav-item.sidebar-nav-active,
    .homepage-sidebar .stButton > button:hover,
    .homepage-sidebar .stPageLink > button:hover {
        background: rgba(255, 77, 0, 0.18) !important;
        color: #ffffff !important;
        border-color: rgba(255, 77, 0, 0.28) !important;
    }

    .homepage-sidebar .stButton > button {
        justify-content: flex-start !important;
    }

    .homepage-sidebar .stButton > button:focus,
    .homepage-sidebar .stPageLink > button:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(255, 77, 0, 0.18) !important;
    }

    .homepage-sidebar .stButton > button:disabled,
    .homepage-sidebar .stPageLink > button:disabled {
        opacity: 1 !important;
        cursor: default !important;
    }
    """
    text = text.replace('</style>', css + '\n</style>', 1)
    styles.write_text(text, encoding='utf-8')

# 3) page files
page_files = {
    'app.py': 'app.py',
    'pages/1_New_Project.py': 'pages/1_New_Project.py',
    'pages/2_Dashboard.py': 'pages/2_Dashboard.py',
    'pages/3_DealFlow.py': 'pages/3_DealFlow.py',
    'pages/4_LaunchPad.py': 'pages/4_LaunchPad.py',
    'pages/5_OKX_ASP_Listing.py': 'pages/5_OKX_ASP_Listing.py',
}
for rel, page_id in page_files.items():
    path = root / rel
    text = path.read_text(encoding='utf-8')
    if 'render_app_nav' not in text:
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith('from ui.components import') and 'render_app_nav' not in line:
                lines[idx] = line.rstrip() + ', render_app_nav'
        inserted = False
        for i, line in enumerate(lines):
            if 'init_session_state()' in line and not inserted:
                indent = line[:len(line) - len(line.lstrip())]
                insert_lines = [f'{indent}main_col = render_app_nav("{page_id}")', f'{indent}with main_col:']
                lines = lines[:i+1] + insert_lines + lines[i+1:]
                for j in range(i+3, len(lines)):
                    if lines[j].strip() != '':
                        lines[j] = '    ' + lines[j]
                inserted = True
                break
        if not inserted:
            raise SystemExit(f'Could not insert render_app_nav into {path}')
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')

print('Updated navigation helper, styles, and page wrappers.')
