"""BuilderForge UI Theme & Styles.

Premium SaaS design - sleek navy backgrounds, molten orange accents,
refined typography, and subtle glassmorphism.
"""

import streamlit as st
from typing import Dict, Optional


COMMAND_DECK_CSS = """
<style>
    /* ===== GLOBAL RESET & BASE ===== */
    @import url('https://fonts.googleapis.com/css2?family=Epilogue:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont/tabler-icons.min.css');

    * {
        box-sizing: border-box;
    }

    /* ===== HIDE DEFAULT STREAMLIT NAV ===== */
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarHeader"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavSeparator"],
    [data-testid="stSidebarContent"] > [data-testid="stSidebarHeader"],
    [data-testid="stSidebarContent"] > [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] [data-testid="stSidebarHeader"],
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavItems"] {
        display: none !important;
        visibility: hidden !important;
        max-height: 0 !important;
        overflow: hidden !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* ===== MAIN CONTAINER ===== */
    .stApp {
        background-color: #0A0F1C !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ===== TYPOGRAPHY ===== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Epilogue', sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 3.5rem !important;
        margin: 2rem 0 !important;
        line-height: 1.1 !important;
    }

    h2 {
        font-size: 2rem !important;
        margin-top: 3rem !important;
        margin-bottom: 1.5rem !important;
        font-weight: 600 !important;
    }

    h3 {
        font-size: 1.25rem !important;
        margin-top: 1.5rem !important;
    }

    p, li, div, span {
        color: #94A3B8 !important;
        line-height: 1.6;
    }

    .stMarkdown b, .stMarkdown strong {
        color: #ffffff !important;
    }

    /* ===== CARDS (Glassmorphism) ===== */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="column"] {
        background: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        backdrop-filter: blur(8px) !important;
        box-shadow: none !important;
        margin-bottom: 0 !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stVerticalBlock"] > div > div[data-testid="column"]:hover {
        border-color: rgba(255, 77, 0, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5) !important;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        background-color: #FF4D00 !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 14px 0 rgba(255, 77, 0, 0.39) !important;
        transition: all 0.2s ease !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
    }

    .stButton > button:hover {
        background-color: #E64500 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(255, 77, 0, 0.23) !important;
        color: #ffffff !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .hero-section {
        text-align: center;
        padding: 5.5rem 0 1.5rem;
        margin: 0 auto 1.25rem auto;
        max-width: 860px;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.72rem 1.2rem;
        border-radius: 999px;
        background: rgba(255, 77, 0, 0.12);
        color: #FF4D00;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 5rem !important;
        line-height: 1.02 !important;
        letter-spacing: -0.04em;
        margin: 0 !important;
        color: #ffffff !important;
    }

    .hero-copy {
        font-size: 1.1rem !important;
        color: #94A3B8 !important;
        max-width: 680px;
        margin: 1.25rem auto 0 auto !important;
        line-height: 1.7 !important;
    }

    .hero-btn-row {
        display: inline-flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 2.2rem;
    }

    .hero-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 190px;
        padding: 0.95rem 2rem;
        border-radius: 999px;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 0.95rem;
        text-decoration: none;
        letter-spacing: 0.02em;
        transition: all 0.2s ease;
    }

    .hero-btn-primary {
        background: #FF4D00;
        color: #ffffff;
        box-shadow: 0 18px 48px rgba(255, 77, 0, 0.22);
        border: none;
    }

    .hero-btn-primary:hover {
        background: #ff5e1f;
    }

    .hero-btn-secondary {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #ffffff;
    }

    .hero-btn-secondary:hover {
        background: rgba(255, 255, 255, 0.08);
    }

    .home-pipeline-space {
        height: 2rem;
    }

    .home-footer-space {
        height: 3rem;
    }

    .section-heading {
        text-align: center;
        margin-bottom: 1.25rem;
    }

    .section-divider {
        width: 68px;
        margin: 0.75rem auto 0;
    }

    .stApp:has(.hero-section) .stButton > button {
        min-height: 52px !important;
        padding: 0.95rem 1.6rem !important;
        border-radius: 12px !important;
        font-size: 0.95rem !important;
        box-shadow: 0 16px 40px rgba(255, 77, 0, 0.22) !important;
    }

    .stApp:has(.hero-section) .stButton > button:not([type="primary"]) {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.16) !important;
        color: #ffffff !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04) !important;
    }

    .stApp:has(.hero-section) .stButton > button:hover {
        transform: translateY(-1px) !important;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-top: 2.5rem;
    }

    .hero-action-col {
        flex: 1 1 220px;
    }

    .hero-actions .stButton > button {
        width: 100% !important;
        min-height: 56px !important;
        border-radius: 14px !important;
        padding: 0.95rem 1.2rem !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.01em !important;
    }

    .hero-actions .stButton > button[type="primary"] {
        background: #FF4D00 !important;
        color: #ffffff !important;
        box-shadow: 0 16px 45px rgba(255, 77, 0, 0.24) !important;
        border: none !important;
    }

    .hero-actions .stButton > button:not([type="primary"]) {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
    }

    .hero-actions .stButton > button:not([type="primary"]):hover {
        background: rgba(255, 255, 255, 0.08) !important;
    }

    .homepage-sidebar {
        background: rgba(12, 17, 30, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 2rem 1.7rem;
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        position: sticky;
        top: 86px;
        min-height: calc(100vh - 100px);
    }

    .homepage-sidebar .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-align: left !important;
        background: rgba(255, 255, 255, 0.04) !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 16px !important;
        box-shadow: none !important;
        padding: 0.95rem 1rem !important;
        margin-bottom: 0.75rem !important;
        transition: all 0.2s ease !important;
    }

    .homepage-sidebar .stButton > button:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        transform: translateX(1px) !important;
    }

    .homepage-sidebar .stButton > button[disabled] {
        background: rgba(255, 77, 0, 0.18) !important;
        border-color: rgba(255, 77, 0, 0.28) !important;
        color: #ffffff !important;
        cursor: default !important;
    }

    .homepage-sidebar .stButton > button[disabled]:hover {
        background: rgba(255, 77, 0, 0.18) !important;
    }

    .sidebar-brand {
        display: flex;
        align-items: flex-start;
        gap: 0.9rem;
    }

    .sidebar-logo {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: #FF4D00;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 1.1rem;
        box-shadow: 0 18px 40px rgba(255, 77, 0, 0.18);
    }

    .sidebar-brand-name {
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.15;
    }

    .sidebar-brand-sub {
        color: #94A3B8;
        font-size: 0.78rem;
        margin-top: 0.25rem;
        max-width: 180px;
    }

    .sidebar-nav-label {
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #64748B;
        margin-bottom: 0.5rem;
    }

    .sidebar-status {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 1rem;
        margin-top: auto;
    }

    .sidebar-status-line {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.78rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.35rem;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.25);
    }

    .sidebar-status-meta {
        font-size: 0.72rem;
        color: #94A3B8;
    }

    .hero-actions {
        justify-content: flex-start;
    }

    .hero-copy {
        max-width: 700px;
    }

    .feature-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
        margin-top: 2.5rem;
    }

    .feature-card {
        padding: 2rem;
        border-radius: 20px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 18px 60px rgba(0, 0, 0, 0.12);
        min-height: 240px;
    }

    .feature-card-icon {
        width: 46px;
        height: 46px;
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.05);
        color: #FFB380;
        font-size: 1.05rem;
        margin-bottom: 1rem;
    }

    .feature-card h3 {
        color: #ffffff !important;
        margin-top: 0 !important;
        margin-bottom: 0.85rem !important;
        font-size: 1.05rem !important;
    }

    .feature-card p {
        color: #94A3B8 !important;
        font-size: 0.95rem !important;
        line-height: 1.75 !important;
        margin: 0 !important;
    }

    .tech-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.85rem;
        margin-top: 2.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        opacity: 0.78;
    }

    .tech-pill {
        padding: 0.55rem 0.95rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.04);
        color: #94A3B8;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .home-footer {
        text-align: center;
        padding: 2.5rem 0 0;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        margin-top: 2rem;
    }

    .home-footer p {
        font-size: 0.75rem;
        color: #64748B !important;
        letter-spacing: 0.18em;
        margin: 0;
    }

    .sidebar-logo {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: #FF4D00;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        font-size: 1.1rem;
    }

    .sidebar-brand-name {
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 700;
    }

    .sidebar-brand-sub {
        color: #94A3B8;
        font-size: 0.82rem;
        margin-top: 0.15rem;
    }

    .sidebar-nav-label {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #64748B;
        margin-bottom: 0.5rem;
    }

    .sidebar-nav-item {
        width: 100%;
        text-align: left;
        padding: 0.95rem 1rem;
        margin-bottom: 0.6rem;
        border-radius: 14px;
        font-size: 0.95rem;
        font-weight: 600;
        color: #94A3B8;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.06);
        cursor: pointer;
        transition: all 0.2s ease;
    }

    .sidebar-nav-item:hover:not(:disabled) {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.08);
    }

    .sidebar-nav-item:disabled,
    .sidebar-nav-active {
        color: #ffffff;
        background: rgba(255, 77, 0, 0.18);
        border-color: rgba(255, 77, 0, 0.28);
    }

    .sidebar-status {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 18px;
        padding: 1rem;
    }

    .sidebar-status-line {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 0.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.35rem;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10B981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.25);
        flex-shrink: 0;
    }

    .sidebar-status-meta {
        font-size: 0.75rem;
        color: #94A3B8;
    }

    .hero-homepage {
        text-align: left;
        padding: 3rem 0 0;
    }

    .hero-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-top: 2rem;
    }

    .hero-action-col {
        flex: 1 1 260px;
    }

    .feature-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }

    .feature-card {
        padding: 2rem;
        border-radius: 20px;
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.06);
        box-shadow: 0 20px 80px rgba(0, 0, 0, 0.12);
        min-height: 240px;
    }

    .feature-card-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.05);
        color: #FF4D00;
        font-size: 1.1rem;
        margin-bottom: 1.25rem;
    }

    .feature-card h3 {
        margin-bottom: 0.75rem !important;
        font-size: 1.1rem !important;
    }

    .tech-bar {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 0.75rem;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        opacity: 0.8;
    }

    .tech-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.55rem 0.95rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.04);
        color: #94A3B8;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
    }

    .home-footer p {
        font-size: 0.8rem;
        color: #64748B !important;
        letter-spacing: 0.16em;
    }

    .section-heading {
        text-align: left;
        margin-bottom: 1.5rem;
    }

    .section-label {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.45rem 0.85rem;
        border-radius: 999px;
        background: rgba(255, 77, 0, 0.12);
        color: #FF4D00;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.18em;
    }

    .section-divider {
        width: 72px;
        height: 1px;
        background: #FF4D00;
        margin-top: 1rem;
    }

    .hero-copy {
        max-width: 680px;
    }

    .hero-title {
        font-size: 4.5rem !important;
        line-height: 1.02 !important;
    }

    .hero-badge {
        display: inline-flex;
        margin-bottom: 1.5rem;
    }

    .hero-btn {
        width: 100%;
    }

    .hero-btn-primary {
        box-shadow: 0 24px 60px rgba(255, 77, 0, 0.22);
    }

    .hero-btn-secondary {
        border-color: rgba(255, 255, 255, 0.18);
    }

    .hero-btn-secondary:hover {
        background: rgba(255, 255, 255, 0.05);
    }

    .sidebar-nav-item:disabled {
        cursor: default;
    }

    .sidebar-nav-active {
        cursor: default;
    }

    .sidebar-nav-item {
        font-family: 'Inter', sans-serif;
    }

    .feature-card p {
        font-size: 0.95rem !important;
        line-height: 1.75 !important;
    }

    .hero-section {
        padding-top: 0 !important;
    }

    .homepage-sidebar {
        margin-top: 1rem;
    }

    .homepage-sidebar button {
        font-family: 'Inter', sans-serif;
    }

    .home-footer {
        text-align: left;
        padding-top: 2rem;
    }

    .home-footer p {
        margin: 0;
    }

    .hero-actions button {
        min-height: 58px;
    }

    .tech-bar {
        gap: 0.65rem;
    }

    .status-dot {
        width: 9px;
        height: 9px;
    }

    .sidebar-status {
        margin-top: auto;
    }

    .sidebar-status-meta {
        color: #94A3B8;
    }

    .sidebar-nav-item:hover:not([disabled]) {
        transform: translateY(-1px);
    }

    .hero-action-col {
        width: 100%;
    }

    .hero-nav-empty {
        display:none;
    }

    .stButton > button[disabled] {
        background: rgba(255, 77, 0, 0.18) !important;
        border-color: rgba(255, 77, 0, 0.28) !important;
        color: #ffffff !important;
    }

    .stButton > button[disabled]:hover {
        background: rgba(255, 77, 0, 0.18) !important;
    }

    .stButton > button {
        width: 100% !important;
    }

    .stButton > button:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(255, 77, 0, 0.18) !important;
    }

    .feature-card-icon {
        margin-bottom: 1rem;
    }

    .homepage-sidebar {
        padding-bottom: 1.5rem;
    }

    .sidebar-brand-sub {
        max-width: 180px;
        white-space: normal;
    }

    .sidebar-brand {
        align-items:flex-start;
    }

    .sidebar-nav-label {
        margin-top: 1rem;
    }

    .hero-btn {
        min-width: 0;
    }

    .hero-actions {
        justify-content: flex-start;
    }

    .feature-card {
        min-height: 260px;
    }

    .hero-copy {
        margin-bottom: 0;
    }

    .section-label {
        margin-bottom: 0.5rem;
    }

    .feature-row {
        margin-bottom: 0;
    }

    .section-divider {
        margin-top: 1rem;
    }

    .sidebar-logo {
        min-width: 44px;
    }

    .sidebar-status-line {
        margin-bottom: 0.5rem;
    }

    .hero-title {
        margin-top: 0;
    }

    .feature-card-icon {
        font-size: 1.1rem;
    }

    .feature-card h3 {
        font-size: 1.05rem !important;
    }

    .hero-homepage {
        max-width: 760px;
    }

    .hero-section {
        padding-bottom: 0;
    }

    .hero-actions {
        margin-bottom: 1rem;
    }

    .feature-row {
        margin-top: 2.25rem;
    }

    .tech-bar {
        margin-top: 2.5rem;
    }

    .home-footer p {
        color: #64748B !important;
    }

    .sidebar-status {
        background: rgba(255,255,255,0.02);
    }

    .sidebar-status-meta {
        font-size: 0.74rem;
    }

    .sidebar-nav-item {
        transition: all 0.15s ease;
    }

    .sidebar-nav-item:hover:not([disabled]) {
        transform: translateX(2px);
    }

    .homepage-sidebar {
        box-shadow: 0 30px 80px rgba(0,0,0,0.16);
    }

    .stButton > button {
        padding: 0.95rem 1.15rem !important;
    }

    .hero-action-col button {
        font-size: 0.95rem !important;
    }

    .feature-card p {
        opacity: 0.95;
    }

    .feature-row {
        row-gap: 1rem;
    }

    .tech-pill {
        letter-spacing: 0.14em;
    }

    .sidebar-brand-name {
        line-height: 1.1;
    }

    .sidebar-brand-sub {
        color: #94A3B8;
    }

    .sidebar-brand {
        gap: 0.9rem;
    }

    .sidebar-brand-name,
    .sidebar-brand-sub {
        display: inline-block;
    }

    .homepage-sidebar {
        padding-top: 1.5rem;
    }

    .hero-btn-secondary {
        color: #ffffff !important;
    }

    .hero-btn-primary {
        color: #ffffff !important;
    }

    .hero-btn.secondary {
        border-color: rgba(255,255,255,0.14);
    }

    .sidebar-status {
        margin-top: 1rem;
    }

    .sidebar-nav-item {
        border-radius: 16px;
    }

    .sidebar-nav-item[disabled] {
        opacity: 1;
    }

    .feature-row {
        gap: 1.25rem;
    }

    .section-heading {
        margin-bottom: 2rem;
    }

    .section-divider {
        width: 64px;
    }

    .hero-btn-row,
    .hero-actions {
        justify-content: flex-start;
    }

    .hero-section {
        padding-top: 1rem;
    }

    .homepage-sidebar {
        padding-left: 1.7rem;
        padding-right: 1.7rem;
    }

    .hero-action-col:last-child {
        max-width: 220px;
    }

    .hero-badge {
        letter-spacing: 0.25em;
    }

    .feature-card-icon {
        width: 46px;
        height: 46px;
    }

    .tech-bar {
        justify-content: flex-start;
    }

    .hero-copy {
        padding-right: 1rem;
    }

    .hero-title {
        font-size: 4rem !important;
    }

    .feature-card {
        min-height: 240px;
    }

    .home-footer {
        border-top: 1px solid rgba(255,255,255,0.06);
        padding-top: 2rem;
    }

    .home-footer p {
        margin: 0;
    }

    .tech-pill {
        background: rgba(255,255,255,0.03);
    }

    .hero-actions button {
        border-radius: 14px;
    }

    .homepage-sidebar {
        max-width: 300px;
    }

    .sidebar-brand-sub {
        max-width: 220px;
    }

    .stButton > button {
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
    }

    .hero-copy {
        max-width: 700px;
    }

    .section-heading {
        width: fit-content;
    }

    .section-divider {
        margin-top: 0.85rem;
    }

    .feature-card-icon {
        background: rgba(255,255,255,0.05);
    }

    .feature-card h3 {
        margin-bottom: 0.75rem !important;
    }

    .hero-actions {
        align-items: stretch;
    }

    .hero-action-col {
        min-width: 0;
    }

    .hero-btn-primary {
        background-color:#FF4D00 !important;
    }

    .hero-btn-secondary {
        color:#fff !important;
    }

    .sidebar-status-line {
        justify-content: flex-start;
    }

    .sidebar-status-meta {
        margin-top: 0.25rem;
    }

    .feature-card p {
        color: #94A3B8;
    }

    .hero-btn-secondary:hover {
        background-color: rgba(255,255,255,0.08);
    }

    .sidebar-status {
        border-color: rgba(255,255,255,0.04);
    }

    .sidebar-status-meta {
        color: #94A3B8;
    }

    .section-label {
        letter-spacing: 0.22em;
    }

    .sidebar-brand-name {
        font-size: 1.05rem;
    }

    .sidebar-logo {
        box-shadow: 0 12px 30px rgba(255, 77, 0, 0.2);
    }

    .feature-card-icon {
        color: #FFB380;
    }

    .feature-card-icon i {
        font-style: normal;
    }

    .hero-actions button {
        min-height: 56px;
    }

    .feature-row {
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    }

    .hero-homepage {
        max-width: 860px;
    }

    .hero-section {
        padding-bottom: 0;
    }

    .homepage-sidebar {
        padding-bottom: 1rem;
    }

    .sidebar-nav-item {
        min-height: 52px;
    }

    .sidebar-nav-item:hover {
        transform: translateX(1px);
    }

    .sidebar-nav-item:disabled {
        background: rgba(255,77,0,0.18) !important;
    }

    .hero-action-col button {
        width: 100% !important;
    }

    .feature-card p {
        opacity: 0.9;
    }

    .home-footer p {
        letter-spacing: 0.18em;
    }

    .tech-bar {
        padding-top: 1.25rem;
    }

    .section-heading {
        margin-bottom: 1.75rem;
    }

    .sidebar-status {
        margin-top: 1rem;
    }

    .sidebar-nav-item:disabled {
        cursor: default;
    }

    .sidebar-nav-active {
        cursor: default;
    }

    .hero-btn-secondary {
        border-color: rgba(255, 255, 255, 0.16);
    }

    .sidebar-status-line {
        font-size: 0.78rem;
    }

    .sidebar-status-meta {
        font-size: 0.72rem;
    }

    .hero-title {
        font-size: 4.25rem !important;
    }

    .feature-card {
        min-height: 260px;
    }

    .hero-copy {
        font-size: 1.15rem;
    }

    .homepage-sidebar {
        position: sticky;
    }

    .feature-card h3 {
        color: #ffffff !important;
        margin-top: 0 !important;
    }

    .feature-card p {
        color: #94A3B8 !important;
    }

    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        backdrop-filter: blur(12px);
        transition: all 0.3s ease;
        height: 100%;
    }

    .glass-card:hover {
        border-color: rgba(255, 77, 0, 0.25);
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
    }

    .glass-card h3 {
        color: #ffffff !important;
        margin-top: 0 !important;
        margin-bottom: 0.75rem !important;
        font-size: 1.1rem !important;
    }

    .glass-card p {
        color: #94A3B8 !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }

    .tech-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        opacity: 0.75;
    }

    .tech-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #94A3B8;
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* ===== TOP NAVIGATION BAR ===== */
    .top-nav {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        background: rgba(10, 15, 28, 0.92);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        height: 64px;
    }

    .top-nav-inner {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .top-nav-brand {
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }

    .top-nav-logo {
        width: 32px;
        height: 32px;
        background: #FF4D00;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.2rem;
    }

    .top-nav-brand-text {
        font-family: 'Epilogue', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        color: #ffffff;
    }

    .top-nav-links {
        display: flex;
        align-items: center;
        gap: 0.25rem;
    }

    .nav-top-link {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        color: #94A3B8;
        text-decoration: none;
        transition: all 0.2s ease;
    }

    .nav-top-link:hover {
        color: #ffffff;
        background: rgba(255, 255, 255, 0.04);
    }

    .nav-top-link.nav-top-active {
        color: #FF4D00;
        background: rgba(255, 77, 0, 0.1);
        font-weight: 600;
    }

    .top-nav-spacer {
        height: 64px;
    }

    /* ===== TOP NAV PAGE LINKS (invisible click targets over the top bar) ===== */
    .top-nav-spacer + .stPageLink {
        display: none !important;
    }

    /* Hide the entire columns container after top-nav-spacer */
    .top-nav-spacer + div .stPageLink a {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        color: #94A3B8 !important;
        background: transparent !important;
        border: none !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        min-height: 0 !important;
        line-height: 1.4 !important;
        box-shadow: none !important;
    }

    .top-nav-spacer + div .stPageLink a:hover {
        background: rgba(255, 255, 255, 0.04) !important;
        color: #ffffff !important;
        transform: none !important;
    }

    /* Hide the glass card styling on the nav columns */
    .top-nav-spacer + div div[data-testid="column"] {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
        flex: 0 0 auto !important;
        width: auto !important;
        min-height: 0 !important;
        transform: none !important;
    }

    .top-nav-spacer + div div[data-testid="column"]:hover {
        transform: none !important;
        border-color: transparent !important;
        box-shadow: none !important;
    }

    .top-nav-spacer + div div[data-testid="column"] > div {
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    .top-nav-spacer + div[data-testid="stVerticalBlock"] > div {
        gap: 0 !important;
    }

    /* ===== AGENT CARDS (homepage) ===== */
    .agent-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: 1.25rem;
        margin: 2rem 0 3rem;
    }

    .agent-card {
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 16px;
        padding: 1.75rem;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .agent-card:hover {
        border-color: rgba(255, 77, 0, 0.25);
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
    }

    .agent-card-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }

    .agent-card h3 {
        color: #ffffff !important;
        font-size: 1rem !important;
        margin: 0 0 0.4rem 0 !important;
    }

    .agent-card p {
        color: #94A3B8 !important;
        font-size: 0.82rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }

    .agent-card-tag {
        display: inline-block;
        font-size: 0.6rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        padding: 0.2rem 0.55rem;
        border-radius: 4px;
        margin-top: 0.75rem;
    }

    .home-footer {
        text-align: center;
        padding: 2rem 0 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.04);
        margin-top: 3rem;
    }

    .home-footer p {
        font-size: 0.7rem;
        color: #475569 !important;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* Secondary button variant */
    button[kind="secondary"] {
        background-color: transparent !important;
        color: #E2E8F0 !important;
        border: 1px solid #1E293B !important;
        box-shadow: none !important;
    }

    button[kind="secondary"]:hover {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-color: #334155 !important;
        color: #ffffff !important;
    }

    /* ===== TEXT INPUTS ===== */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div {
        font-family: 'Inter', sans-serif !important;
        border: 1px solid #1E293B !important;
        border-radius: 8px !important;
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #ffffff !important;
        padding: 0.75rem !important;
        box-shadow: none !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #FF4D00 !important;
        box-shadow: 0 0 0 2px rgba(255, 77, 0, 0.2) !important;
    }

    /* ===== METRIC CARDS ===== */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
    }

    div[data-testid="stMetric"] label {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.75rem !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-family: 'Epilogue', sans-serif !important;
        font-weight: 700 !important;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background-color: #0A0F1C !important;
        border-right: 1px solid #1E293B !important;
    }

    /* Sidebar nav item wrapper */
    .bf-sidebar-item {
        position: relative;
        padding: 0 0.5rem;
        margin-bottom: 0.25rem;
        border-radius: 8px;
        overflow: hidden;
        transition: background-color 0.2s ease;
    }

    .bf-sidebar-item:hover {
        background-color: rgba(255, 255, 255, 0.04);
    }

    .bf-sidebar-item.nav-active {
        background-color: rgba(255, 77, 0, 0.12);
    }

    .bf-sidebar-content {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.65rem 1rem;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        font-weight: 500;
        color: #94A3B8;
        pointer-events: none;
    }

    .bf-sidebar-content i {
        font-size: 1.1rem;
        color: inherit;
    }

    .bf-sidebar-item.nav-active .bf-sidebar-content {
        color: #FF4D00;
        font-weight: 600;
    }

    /* Invisible overlay button */
    .bf-sidebar-item .stButton {
        position: static !important;
    }

    .bf-sidebar-item .stButton > button {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        min-height: unset !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        border-radius: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        opacity: 0;
        z-index: 2;
        cursor: pointer;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem !important;
        background-color: transparent !important;
        border-bottom: 1px solid #1E293B !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        background-color: transparent !important;
        border: none !important;
        padding: 0.75rem 0 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #FF4D00 !important;
        border-bottom: 2px solid #FF4D00 !important;
    }

    /* ===== STEPPER ===== */
    .bf-stepper {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 2.5rem 0;
        position: relative;
        flex-wrap: wrap;
    }

    pre:has(.bf-stepper),
    pre:has(code:contains('bf-stepper')),
    .stMarkdown pre {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    .bf-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 120px;
        gap: 0.8rem;
    }

    .bf-step-circle {
        width: 62px;
        height: 62px;
        border-radius: 18px;
        border: 1px solid rgba(255, 255, 255, 0.06);
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(15, 23, 42, 0.72);
        color: #94A3B8;
        transition: all 0.3s ease;
        box-shadow: 0 16px 35px rgba(0, 0, 0, 0.14);
    }

    .bf-step-active .bf-step-circle {
        background-color: rgba(255, 77, 0, 0.18);
        color: #ffffff;
        border-color: rgba(255, 77, 0, 0.28);
        box-shadow: 0 20px 40px rgba(255, 77, 0, 0.18);
    }

    .bf-step-done .bf-step-circle {
        background-color: rgba(16, 185, 129, 0.16);
        color: #ffffff;
        border-color: rgba(16, 185, 129, 0.3);
    }

    .bf-step-label {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.82rem;
        color: #94A3B8;
        text-align: center;
        margin: 0;
        letter-spacing: 0.03em;
    }

    .bf-step-active .bf-step-label {
        color: #ffffff;
    }

    .bf-stepper::after {
        content: '';
        position: absolute;
        top: 32px;
        left: 8%;
        right: 8%;
        height: 1px;
        background: rgba(255, 255, 255, 0.06);
        z-index: 0;
    }
        left: 12%;
        width: 76%;
        height: 1px;
        background: #1E293B;
        z-index: 0;
    }

    /* ===== DIVIDER ===== */
    hr {
        border: none !important;
        border-top: 1px solid #1E293B !important;
        margin: 3rem 0 !important;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0A0F1C;
    }
    ::-webkit-scrollbar-thumb {
        background: #1E293B;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #334155;
    }
    /* ===== COMPACT HOME REFERENCE LAYOUT ===== */
    .stApp:has(.hero-homepage) .main .block-container {
        max-width: 760px;
        padding: 1.5rem 2.5rem 2rem;
    }

    .stApp:has(.hero-homepage) div[data-testid="stVerticalBlock"] > div > div[data-testid="column"] {
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
        transform: none !important;
    }

    .hero-homepage {
        max-width: 100% !important;
        padding: 0.15rem 0 0 !important;
        margin: 0 0 0.75rem !important;
        text-align: center;
    }

    .hero-badge {
        padding: 0.18rem 0.55rem;
        border-radius: 4px;
        font-size: 0.42rem;
        letter-spacing: 0.08em;
        margin-bottom: 0.55rem;
    }

    .hero-title {
        font-size: 2rem !important;
        line-height: 1 !important;
        letter-spacing: -0.045em;
    }

    .hero-copy {
        max-width: 390px;
        margin: 0.6rem auto 0 !important;
        padding: 0 !important;
        font-size: 0.61rem !important;
        line-height: 1.45 !important;
    }

    .stApp:has(.hero-homepage) .stButton > button {
        min-height: 0 !important;
        padding: 0.44rem 0.65rem !important;
        border-radius: 3px !important;
        font-size: 0.56rem !important;
        box-shadow: none !important;
    }

    .stApp:has(.hero-homepage) .stButton > button:not([type="primary"]) {
        background: #111827 !important;
        border: 1px solid #253044 !important;
        color: #E2E8F0 !important;
    }

    .home-pipeline-space {
        height: 1.75rem;
    }

    .section-heading {
        margin: 0 0 1.1rem !important;
        text-align: center;
        width: 100%;
    }

    .section-label {
        padding: 0;
        background: transparent;
        border-radius: 0;
        font-size: 0.43rem;
        letter-spacing: 0.22em;
    }

    .section-divider {
        display: none;
    }

    .bf-stepper {
        gap: 0.6rem;
        margin: 0 0 1.65rem;
        flex-wrap: nowrap;
    }

    .bf-step {
        width: 76px;
        gap: 0.38rem;
        position: relative;
        z-index: 1;
    }

    .bf-step-circle {
        width: 25px;
        height: 25px;
        border-radius: 5px;
        background: #111b2b;
        box-shadow: none;
    }

    .bf-step-circle i {
        font-size: 0.62rem !important;
    }

    .bf-step-label {
        font-size: 0.46rem;
        line-height: 1.2;
        white-space: nowrap;
    }

    .bf-stepper::after {
        top: 12px;
        left: 9%;
        right: 9%;
    }

    .feature-row {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.6rem;
        margin-top: 0;
    }

    .feature-card {
        min-height: 108px;
        padding: 0.7rem;
        border-radius: 4px;
        background: #111a2a;
        border-color: #1b283c;
        box-shadow: none;
    }

    .feature-card-icon {
        width: 18px;
        height: 18px;
        border-radius: 3px;
        margin-bottom: 0.45rem;
        font-size: 0.52rem;
        color: #FF4D00;
    }

    .feature-card-icon-testnet { color: #60A5FA; }
    .feature-card-icon-asp { color: #34D399; }

    .feature-card h3 {
        margin: 0 0 0.38rem !important;
        font-size: 0.56rem !important;
        line-height: 1.2 !important;
    }

    .feature-card p {
        font-size: 0.43rem !important;
        line-height: 1.45 !important;
    }

    .tech-bar {
        justify-content: center;
        gap: 1rem;
        margin-top: 1.75rem;
        padding-top: 1rem;
        border-color: #182235;
    }

    .tech-pill {
        padding: 0;
        background: transparent;
        border-radius: 0;
        font-size: 0.4rem;
        letter-spacing: 0.07em;
    }

    .home-footer-space { height: 3rem; }

    .home-footer {
        padding: 0.8rem 0 0;
        margin-top: 0;
        text-align: left;
        border-color: #182235;
    }

    .home-footer p {
        font-size: 0.34rem;
        letter-spacing: 0.08em;
    }

    section[data-testid="stSidebar"] {
        border-right-color: #182235 !important;
    }

    .bf-sidebar-brand {
        padding: 0.65rem 0.35rem 1rem;
        margin-bottom: 0.45rem;
    }

    .bf-sidebar-brand-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .bf-sidebar-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 20px;
        height: 20px;
        border-radius: 4px;
        background: #FF4D00;
        color: #ffffff;
        font-size: 0.68rem;
    }

    .bf-sidebar-name {
        color: #ffffff !important;
        font-family: 'Epilogue', sans-serif;
        font-size: 0.75rem;
        font-weight: 700;
    }

    .bf-sidebar-label {
        padding-left: 0.35rem;
        margin-bottom: 0.35rem;
        color: #64748B !important;
        font-size: 0.4rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
    }

    .bf-sidebar-item {
        padding: 0 0.25rem;
        margin-bottom: 0.08rem;
        border-radius: 3px;
    }

    .bf-sidebar-content {
        gap: 0.45rem;
        padding: 0.38rem 0.55rem;
        font-size: 0.5rem;
    }

    .bf-sidebar-content i { font-size: 0.64rem; }

    .bf-sidebar-divider {
        margin: 0 !important;
        border-color: #182235 !important;
    }

    .bf-system-status {
        padding: 0.65rem;
        margin-top: 1rem;
        background: #0c1423;
        border: 1px solid #182235;
        border-radius: 3px;
    }

    .bf-system-status-heading {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        margin-bottom: 0.25rem;
        color: #64748B !important;
        font-size: 0.4rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .bf-system-status-dot {
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background: #10B981;
    }

    .bf-system-status-version {
        color: #94A3B8 !important;
        font-size: 0.43rem;
    }

    @media (max-width: 720px) {
        .stApp:has(.hero-homepage) .main .block-container { padding: 1.25rem; }
        .feature-row { grid-template-columns: 1fr; }
        .bf-stepper { gap: 0.15rem; }
        .bf-step { width: 20%; }
        .bf-step-label { white-space: normal; }
        .tech-bar { gap: 0.55rem; }
    }
</style>
"""


def apply_theme() -> None:
    """Inject the Command Deck CSS into the Streamlit app."""
    st.markdown(COMMAND_DECK_CSS, unsafe_allow_html=True)


def phase_stepper(current_phase: str, phases: list) -> None:
    """Render a visual phase stepper component."""
    phase_idx = {p: i for i, p in enumerate(phases)}
    current_idx = phase_idx.get(current_phase, 0)

    steps_html = ""
    for i, phase in enumerate(phases):
        cls = "bf-step"
        if i == current_idx:
            cls += " bf-step-active"
        elif i < current_idx:
            cls += " bf-step-done"

        icon_map = {
            "Idea Input": "ti-bulb",
            "Research": "ti-search",
            "Creation": "ti-palette",
            "Execution": "ti-bolt",
            "Analysis": "ti-chart-bar"
        }
        icon = icon_map.get(phase, "ti-circle")

        steps_html += f'<div class="{cls}"><div class="bf-step-circle"><i class="ti {icon}" style="font-size: 1.25rem;"></i></div><div class="bf-step-label">{phase}</div></div>'

    html = f'<div class="bf-stepper">{steps_html}</div>'
    st.markdown(html, unsafe_allow_html=True)


def console_log(messages: list) -> None:
    """Render a terminal-style log console."""
    log_text = "\\n".join(messages) if messages else "> Waiting for agent execution..."
    st.markdown(
        f"""
        <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid #1E293B; border-radius: 12px; padding: 1.5rem; font-family: 'Courier New', monospace; font-size: 0.85rem; color: #38BDF8; max-height: 400px; overflow-y: auto;">
            {log_text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(label: str, status: str = "pending") -> None:
    """Render a status badge."""
    colors = {
        "active": {"bg": "rgba(56, 189, 248, 0.1)", "text": "#38BDF8", "border": "#38BDF8"},
        "pending": {"bg": "rgba(234, 179, 8, 0.1)", "text": "#EAB308", "border": "#EAB308"},
        "done": {"bg": "rgba(16, 185, 129, 0.1)", "text": "#10B981", "border": "#10B981"}
    }
    c = colors.get(status, colors["pending"])
    st.markdown(
        f"""
        <span style="display: inline-block; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.7rem; font-weight: 700; border: 1px solid {c['border']}; background: {c['bg']}; color: {c['text']}; text-transform: uppercase; letter-spacing: 0.05em;">
            {label}
        </span>
        """,
        unsafe_allow_html=True,
    )
