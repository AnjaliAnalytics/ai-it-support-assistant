import os
import requests
import streamlit as st

# 1. Page Config (Must be first Streamlit command)
st.set_page_config(
    page_title="IT Support SaaS",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------------------
# 2. Global Backend URL Resolution
# ------------------------------------------------------------------------------
if "BACKEND_URL" in st.secrets:
    BACKEND_URL = st.secrets["BACKEND_URL"].rstrip("/")
else:
    BACKEND_URL = os.getenv(
        "BACKEND_URL", "https://ai-it-support-backend.onrender.com"
    ).rstrip("/")

# Store in session state for all view modules
st.session_state["BACKEND_URL"] = BACKEND_URL

# ------------------------------------------------------------------------------
# 3. View Imports
# ------------------------------------------------------------------------------
from views.agent_view import render_agent
from views.ai_analysis import render_ai_analysis
from views.incident_history import render_incident_history
from views.new_incident import render_new_incident
from views.overview import render_overview
from views.styles import apply_custom_theme

# Apply CSS
apply_custom_theme()

# ------------------------------------------------------------------------------
# 4. Sidebar Menu
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
# 5. Page Router Execution
# ------------------------------------------------------------------------------
if selected_page == "Overview":
    render_overview()

elif selected_page == "New Incident":
    render_new_incident()

elif selected_page == "AI Analysis":
    render_ai_analysis()

elif selected_page == "Troubleshooting Agent":
    render_agent()

elif selected_page == "Knowledge Base":
    st.markdown('<div class="header-title">📚 Knowledge Base & RAG Telemetry</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">Vectorized IT documentation for automated resolution support.</div>', unsafe_allow_html=True)
    
    api_url = f"{BACKEND_URL}/api/v1/knowledge"
    try:
        res = requests.get(api_url, timeout=5)
        if res.status_code == 200:
            articles = res.json()
            if articles:
                st.dataframe(articles, use_container_width=True)
            else:
                st.info("No knowledge base articles stored in vector database.")
        else:
            st.warning(f"Could not load knowledge articles (Status {res.status_code}).")
    except Exception as e:
        st.error(f"Error connecting to Knowledge Base API: {e}")

elif selected_page == "Incident History":
    render_incident_history()

elif selected_page == "System Health":
    st.title("🖥️ System Health & Monitoring")
    st.caption("Live operational status checks for application components.")
    
    try:
        res = requests.get(f"{BACKEND_URL}/api/v1/health", timeout=5)
        if res.status_code == 200:
            st.success(f"FastAPI Backend: Online ({BACKEND_URL})")
        else:
            st.error(f"FastAPI Backend returned status {res.status_code}")
    except Exception as e:
        st.error(f"FastAPI Backend: Offline ({e})")

elif selected_page == "About Project":
    st.title("ℹ️ About AI IT Support Assistant")
    st.markdown("""
    ### Enterprise AI IT Operations Platform
    
    * **Backend**: FastAPI REST Service hosted on Render
    * **Database**: PostgreSQL hosted on Supabase
    * **Machine Learning & AI**: Scikit-learn priority prediction & Google Gemini AI diagnosis
    * **Frontend**: Streamlit Community Cloud
    
    ---
    Developed as an end-to-end full-stack AI SaaS pipeline.
    """)