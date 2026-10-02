import requests
import streamlit as st

# Retrieve global dynamic URL set in app.py
BASE_URL = st.session_state.get(
    "BACKEND_URL", "https://ai-it-support-backend.onrender.com"
).rstrip("/")

# Append API version path
BACKEND_URL = f"{BASE_URL}/api/v1"


def render_new_incident():
    st.markdown(
        '<div class="header-title">➕ Submit New IT Ticket</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="header-subtitle">Create an incident ticket for automated ML'
        " priority assessment and resolution.</div>",
        unsafe_allow_html=True,
    )

    with st.form("new_incident_form", clear_on_submit=True):
        title = st.text_input("Incident Title", placeholder="e.g., VPN connection fails repeatedly")
        description = st.text_area(
            "Detailed Description",
            placeholder="Describe the issue, error messages, and affected systems...",
        )
        category = st.selectbox(
            "Category",
            ["Hardware", "Software", "Network", "Access/Identity", "Database", "Other"],
        )
        submitted_by = st.text_input("Submitted By (Email/Name)", value="employee@company.com")

        submit_btn = st.form_submit_button("Submit Ticket")

    if submit_btn:
        if not title or not description:
            st.warning("Please provide both a title and description.")
        else:
            payload = {
                "title": title,
                "description": description,
                "category": category,
                "submitted_by": submitted_by,
            }
            try:
                res = requests.post(f"{BACKEND_URL}/incidents", json=payload, timeout=10)
                if res.status_code in (200, 201):
                    ticket = res.json()
                    st.success(f"Ticket #{ticket.get('id', 'N/A')} created successfully!")
                    st.json(ticket)
                else:
                    st.error(f"Failed to create ticket: {res.text}")
            except Exception as e:
                st.error(f"Error submitting ticket to backend: {e}")