import streamlit as st


def apply_custom_theme():
    """Injects full-width enterprise SaaS dashboard CSS rules."""
    st.markdown("""
        <style>
        /* Force Full-Width Screen Expansion */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
        }

        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Typography & Titles */
        .header-title {
            font-size: 2.2rem !important;
            font-weight: 800 !important;
            color: #0f172a !important;
            letter-spacing: -0.02em;
        }
        .header-subtitle {
            font-size: 1rem !important;
            color: #64748b !important;
            margin-bottom: 1.5rem !important;
        }

        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
        }
        div[data-testid="stMetricValue"] {
            color: #2563eb !important;
            font-size: 2.2rem !important;
            font-weight: 800 !important;
        }

        /* Dark Sidebar Override */
        section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
        }
        section[data-testid="stSidebar"] * {
            color: #f8fafc !important;
        }
        </style>
    """, unsafe_allow_html=True)