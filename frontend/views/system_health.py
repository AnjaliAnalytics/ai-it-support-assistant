import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/api/v1"


def render_system_health():
    st.title("🖥️ System Health & Monitoring")
    st.write("Live operational status checks for application components.")

    col1, col2, col3 = st.columns(3)

    # API Health Check
    try:
        res = requests.get(f"{BACKEND_URL}/health", timeout=3)
        if res.status_code == 200:
            col1.success("FastAPI Backend: Operational")
            col2.success("PostgreSQL Database: Connected")
        else:
            col1.error("FastAPI Backend: Degraded")
    except Exception:
        col1.error("FastAPI Backend: Offline")

    # Gemini LLM Check