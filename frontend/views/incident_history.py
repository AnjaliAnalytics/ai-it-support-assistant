import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/api/v1"


def render_incident_history():
    st.title("📜 Incident History Log")
    st.write("Complete audit log of tickets saved in PostgreSQL.")

    try:
        res = requests.get(f"{BACKEND_URL}/incidents", timeout=5)
        if res.status_code == 200:
            incidents = res.json()
            if incidents:
                st.dataframe(incidents, use_container_width=True)
            else:
                st.info("No incidents logged in the database yet.")
        else:
            st.error("Failed to load incidents.")
    except Exception as e:
        st.error(f"Backend offline: {e}")