"""
styles.py

Global visual system for Olist Intelligence.

Design direction:
    - Deep navy / charcoal background
    - High-contrast typography
    - Minimal accent usage
    - Compact spacing
    - Premium analytics-dashboard appearance
    - No visible raw HTML UI components
"""

from __future__ import annotations

import streamlit as st


def load_styles() -> None:
    """Apply global application styles."""

    st.markdown(
        """
        <style>

        /* =====================================================
           ROOT
        ===================================================== */

        :root {
            --bg: #0b1120;
            --bg-secondary: #111827;
            --surface: #151e2e;
            --surface-soft: #182235;
            --surface-hover: #1d293d;

            --border: rgba(148, 163, 184, 0.16);

            --text-primary: #f8fafc;
            --text-secondary: #a7b1c2;
            --text-muted: #718096;

            --accent: #8b7cff;
            --accent-soft: rgba(139, 124, 255, 0.12);

            --success: #4ade80;
            --danger: #fb7185;

            --radius: 14px;
        }


        /* =====================================================
           MAIN APPLICATION
        ===================================================== */

        .stApp {

            background:
                #0b1120;

            color: var(--text-primary);
        }


        /* =====================================================
           REMOVE EXCESSIVE TOP SPACE
        ===================================================== */

        .main .block-container {

            max-width: 1380px;

            padding-top: 1.25rem;
            padding-bottom: 3rem;
            padding-left: 2.5rem;
            padding-right: 2.5rem;
        }


        /* =====================================================
           GLOBAL TYPOGRAPHY
        ===================================================== */

        html,
        body,
        [class*="css"] {

            font-family:
                Inter,
                ui-sans-serif,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }


        p {

            color: var(--text-secondary);

            font-size: 0.94rem;

            line-height: 1.65;
        }


        /* =====================================================
           HEADINGS
        ===================================================== */

        h1 {

            color: #ffffff !important;

            font-size: 3.4rem !important;

            font-weight: 800 !important;

            letter-spacing: -0.055em !important;

            line-height: 1.05 !important;

            margin-top: 0.4rem !important;

            margin-bottom: 0.35rem !important;
        }


        h2 {

            color: #f8fafc !important;

            font-size: 1.65rem !important;

            font-weight: 750 !important;

            letter-spacing: -0.025em !important;

            margin-top: 1.8rem !important;

            margin-bottom: 0.35rem !important;
        }


        h3 {

            color: #e8edf5 !important;

            font-size: 1.05rem !important;

            font-weight: 650 !important;

            letter-spacing: -0.01em !important;
        }


        h4 {

            color: #dbe3ef !important;

            font-size: 0.95rem !important;

            font-weight: 650 !important;
        }


        /* =====================================================
           HERO
        ===================================================== */

        .main .block-container > div:first-child {

            margin-top: 0;
        }


        /* =====================================================
           SMALL LABELS / EYEBROWS
        ===================================================== */

        .stCaption {

            color: var(--text-muted) !important;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        section[data-testid="stSidebar"] {

            background: #080e1b !important;

            border-right:
                1px solid rgba(148, 163, 184, 0.10);
        }


        section[data-testid="stSidebar"]
        .block-container {

            padding-top: 1.4rem;

            padding-left: 1rem;

            padding-right: 1rem;
        }


        section[data-testid="stSidebar"] h2 {

            font-size: 1.15rem !important;

            margin-top: 0.4rem !important;
        }


        section[data-testid="stSidebar"] p {

            font-size: 0.78rem;

            line-height: 1.5;
        }


        section[data-testid="stSidebar"] hr {

            border-color:
                rgba(148, 163, 184, 0.10);
        }


        /* =====================================================
           SELECTBOX
        ===================================================== */

        div[data-baseweb="select"] > div {

            background: #101827 !important;

            border:
                1px solid rgba(148, 163, 184, 0.13) !important;

            border-radius: 9px !important;

            min-height: 38px !important;

            box-shadow: none !important;
        }


        div[data-baseweb="select"] > div:hover {

            border-color:
                rgba(139, 124, 255, 0.35) !important;
        }


        div[data-baseweb="select"] span {

            color: #d9e1ec !important;

            font-size: 0.82rem !important;
        }


        /* =====================================================
           TEXT AREA
        ===================================================== */

        textarea {

            background: #111827 !important;

            color: #f8fafc !important;

            border:
                1px solid rgba(148, 163, 184, 0.20) !important;

            border-radius: 12px !important;

            font-size: 0.95rem !important;

            line-height: 1.6 !important;

            padding: 1rem !important;

            box-shadow: none !important;
        }


        textarea:focus {

            border-color:
                rgba(139, 124, 255, 0.70) !important;

            box-shadow:
                0 0 0 2px
                rgba(139, 124, 255, 0.10) !important;
        }


        textarea::placeholder {

            color: #64748b !important;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {

            border-radius: 9px !important;

            border:
                1px solid rgba(148, 163, 184, 0.15) !important;

            background: #151e2e !important;

            color: #dce4ef !important;

            font-size: 0.82rem !important;

            font-weight: 600 !important;

            min-height: 38px !important;

            transition:
                all 0.18s ease !important;
        }


        .stButton > button:hover {

            background: #1c283a !important;

            border-color:
                rgba(139, 124, 255, 0.38) !important;

            color: #ffffff !important;
        }


        /* PRIMARY BUTTON */

        .stButton > button[kind="primary"] {

            background:
                linear-gradient(
                    135deg,
                    #7567ee,
                    #6355dc
                ) !important;

            border: none !important;

            color: #ffffff !important;

            box-shadow:
                0 8px 22px
                rgba(99, 85, 220, 0.22);
        }


        .stButton > button[kind="primary"]:hover {

            background:
                linear-gradient(
                    135deg,
                    #8275f5,
                    #6d5fe8
                ) !important;

            transform: translateY(-1px);
        }


        /* =====================================================
           TOGGLE
        ===================================================== */

        div[data-testid="stToggle"] label {

            color: #9ca8ba !important;

            font-size: 0.75rem !important;
        }


        /* =====================================================
           METRIC CARDS
        ===================================================== */

        div[data-testid="stMetric"] {

            background: #121b2a;

            border:
                1px solid rgba(148, 163, 184, 0.12);

            border-radius: 13px;

            padding:
                1rem 1.15rem;

            min-height: 100px;
        }


        div[data-testid="stMetricLabel"] {

            color: #7f8ca1 !important;

            font-size: 0.72rem !important;

            font-weight: 600 !important;

            text-transform: uppercase;

            letter-spacing: 0.08em;
        }


        div[data-testid="stMetricValue"] {

            color: #f8fafc !important;

            font-size: 1.55rem !important;

            font-weight: 750 !important;
        }


        /* =====================================================
           ALERTS
        ===================================================== */

        div[data-testid="stAlert"] {

            border-radius: 10px !important;

            border-width: 1px !important;

            font-size: 0.84rem !important;
        }


        /* =====================================================
           EXPANDERS
        ===================================================== */

        details {

            background: #111a29 !important;

            border:
                1px solid rgba(148, 163, 184, 0.12) !important;

            border-radius: 11px !important;
        }


        details summary {

            color: #cbd5e1 !important;

            font-size: 0.82rem !important;

            font-weight: 600 !important;
        }


        /* =====================================================
           DATAFRAME
        ===================================================== */

        div[data-testid="stDataFrame"] {

            border:
                1px solid rgba(148, 163, 184, 0.12);

            border-radius: 12px;

            overflow: hidden;
        }


        /* =====================================================
           CODE BLOCKS
        ===================================================== */

        pre {

            background: #080d17 !important;

            border:
                1px solid rgba(148, 163, 184, 0.12) !important;

            border-radius: 11px !important;

            padding: 1rem !important;
        }


        code {

            font-family:
                "JetBrains Mono",
                "Cascadia Code",
                Consolas,
                monospace !important;

            font-size: 0.78rem !important;
        }


        /* =====================================================
           DIVIDERS
        ===================================================== */

        hr {

            border-color:
                rgba(148, 163, 184, 0.10) !important;

            margin-top: 1.5rem !important;

            margin-bottom: 1.5rem !important;
        }


        /* =====================================================
           DOWNLOAD BUTTON
        ===================================================== */

        .stDownloadButton > button {

            background: #151e2e !important;

            color: #cbd5e1 !important;

            border:
                1px solid rgba(148, 163, 184, 0.15) !important;

            border-radius: 9px !important;

            font-size: 0.8rem !important;
        }


        .stDownloadButton > button:hover {

            border-color:
                rgba(139, 124, 255, 0.4) !important;

            color: white !important;
        }


        /* =====================================================
           SUCCESS / ERROR
        ===================================================== */

        div[data-testid="stAlert"][kind="success"] {

            background:
                rgba(34, 197, 94, 0.07) !important;
        }


        /* =====================================================
           MOBILE
        ===================================================== */

        @media (max-width: 900px) {

            .main .block-container {

                padding-left: 1rem;

                padding-right: 1rem;

                padding-top: 1rem;
            }


            h1 {

                font-size: 2.4rem !important;
            }


            h2 {

                font-size: 1.4rem !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

apply_styles = load_styles