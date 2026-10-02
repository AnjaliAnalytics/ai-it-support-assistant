import requests
import streamlit as st

# Retrieve global dynamic URL set in app.py
BASE_URL = st.session_state.get(
    "BACKEND_URL", "https://ai-it-support-backend.onrender.com"
).rstrip("/")

# Append API version path
BACKEND_URL = f"{BASE_URL}/api/v1"


def render_incident_history():
    st.markdown(
        '<div class="header-title">📜 Incident History Log</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="header-subtitle">Complete audit log of tickets saved in'
        " PostgreSQL.</div>",
        unsafe_allow_html=True,
    )

    try:
        res = requests.get(f"{BACKEND_URL}/incidents", timeout=5)
        if res.status_code == 200:
            incidents = res.json()
            if incidents:
                st.dataframe(
                    incidents,
                    use_container_width=True,
                    column_config={
                        "created_at": st.column_config.DatetimeColumn(
                            "Created At", format="YYYY-MM-DD HH:mm"
                        ),
                        "priority": st.column_config.SelectboxColumn(
                            "Priority", options=["P1", "P2", "P3", "P4"]
                        ),
                        "status": st.column_config.SelectboxColumn(
                            "Status", options=["Open", "In Progress", "Resolved", "Closed"]
                        ),
                    },
                )
            else:
                st.info("No incidents logged in the database yet.")
        else:
            st.error(f"Failed to fetch incident history (Status {res.status_code}).")
    except Exception as e:
        st.error(f"Backend offline: {e}")