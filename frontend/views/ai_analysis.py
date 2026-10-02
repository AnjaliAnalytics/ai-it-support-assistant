import requests
import streamlit as st

# Retrieve global dynamic URL set in app.py
BASE_URL = st.session_state.get(
    "BACKEND_URL", "https://ai-it-support-backend.onrender.com"
).rstrip("/")

# Append API version path
BACKEND_URL = f"{BASE_URL}/api/v1"


def render_ai_analysis():
    st.markdown(
        '<div class="header-title">🤖 AI-Powered Incident Diagnosis</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="header-subtitle">Analyze issue telemetry with Gemini AI for'
        " automated root-cause analysis and mitigation plans.</div>",
        unsafe_allow_html=True,
    )

    incident_text = st.text_area(
        "Paste Incident Logs / User Query",
        height=150,
        placeholder="e.g., PostgreSQL connection pool exhausted with FATAL: too many connections...",
    )

    if st.button("Run AI Diagnosis", type="primary"):
        if not incident_text.strip():
            st.warning("Please enter incident details to analyze.")
        else:
            with st.spinner("Gemini AI is analyzing telemetry and knowledge base..."):
                try:
                    res = requests.post(
                        f"{BACKEND_URL}/analysis/diagnose",
                        json={"query": incident_text},
                        timeout=15,
                    )
                    if res.status_code == 200:
                        analysis = res.json()
                        st.subheader("💡 Root Cause Analysis & Remediation")
                        st.markdown(analysis.get("recommendation", "No output generated."))
                    else:
                        st.error(f"Analysis failed (Status {res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Failed to communicate with AI Backend: {e}")