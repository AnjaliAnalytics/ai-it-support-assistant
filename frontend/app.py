import streamlit as st
from views.styles import apply_custom_theme
from views.overview import render_overview
from views.new_incident import render_new_incident
from views.ai_analysis import render_ai_analysis
from views.agent_view import render_agent
from views.knowledge_base import render_knowledge_base
from views.incident_history import render_incident_history
from views.system_health import render_system_health
from views.about import render_about

st.set_page_config(
    page_title="AI-Powered IT Support Assistant",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply CSS Styling
apply_custom_theme()

# Sidebar Navigation
st.sidebar.title("🛠️ IT Support SaaS")
navigation = st.sidebar.radio(
    "Navigation Menu",
    [
        "Overview",
        "New Incident",
        "AI Analysis",
        "Troubleshooting Agent",
        "Knowledge Base",
        "Incident History",
        "System Health",
        "About Project"
    ]
)

# Router
if navigation == "Overview":
    render_overview()
elif navigation == "New Incident":
    render_new_incident()
elif navigation == "AI Analysis":
    render_ai_analysis()
elif navigation == "Troubleshooting Agent":
    render_agent()
elif navigation == "Knowledge Base":
    render_knowledge_base()
elif navigation == "Incident History":
    render_incident_history()
elif navigation == "System Health":
    render_system_health()
elif navigation == "About Project":
    render_about()