import os
import streamlit as st

# Set page config as the very first Streamlit command
st.set_page_config(
    page_title="IT Support SaaS",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------------
# Global Backend URL Resolution
# ------------------------------------------------------------------------------
if "BACKEND_URL" in st.secrets:
    BACKEND_URL = st.secrets["BACKEND_URL"].rstrip("/")
else:
    BACKEND_URL = os.getenv(
        "BACKEND_URL", "https://ai-it-support-backend.onrender.com"
    ).rstrip("/")

# Store in session state so all imported view functions can access it globally
st.session_state["BACKEND_URL"] = BACKEND_URL

# Import view components after setting session state
from views.agent_view import render_agent
from views.ai_analysis import render_ai_analysis
from views.new_incident import render_new_incident
from views.overview import render_overview
from views.styles import apply_custom_theme

# Apply global CSS styling
apply_custom_theme()

# ------------------------------------------------------------------------------
# Sidebar Navigation
# ------------------------------------------------------------------------------
st.sidebar.title("🛠️ IT Support SaaS")
st.sidebar.markdown("---")

selected_page = st.sidebar.radio(
    "Navigation Menu",
    [
        "Overview",
        "New Incident",
        "AI Analysis",
        "Troubleshooting Agent",
        "Knowledge Base",
        "Incident History",
        "System Health",
        "About Project",
    ],
)

# ------------------------------------------------------------------------------
# Page Router
# ------------------------------------------------------------------------------
if selected_page == "Overview":
    render_overview()
elif selected_page == "New Incident":
    render_new_incident()
elif selected_page == "AI Analysis":
    render_ai_analysis()
elif selected_page == "Troubleshooting Agent":
    render_agent()
elif selected_page == "System Health":
    st.title("🖥️ System Health & Monitoring")
    st.caption("Live operational status checks for application components.")

    import requests

    try:
        # Corrected FastAPI health check route under /api/v1/health
        res = requests.get(f"{BACKEND_URL}/api/v1/health", timeout=5)
        if res.status_code == 200:
            st.success(f"FastAPI Backend: Online ({BACKEND_URL})")
        else:
            st.error(f"FastAPI Backend returned status {res.status_code}")
    except Exception as e:
        st.error(f"FastAPI Backend: Offline ({e})")