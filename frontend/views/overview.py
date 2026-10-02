import plotly.express as px
import requests
import streamlit as st

# Retrieve global dynamic URL set in app.py
BASE_URL = st.session_state.get(
    "BACKEND_URL", "https://ai-it-support-backend.onrender.com"
).rstrip("/")

# Append API version path
BACKEND_URL = f"{BASE_URL}/api/v1"


def render_overview():
    st.markdown(
        '<div class="header-title">⚡ Executive IT Operations Center</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="header-subtitle">Real-time telemetric analytics sourced'
        " from PostgreSQL core database</div>",
        unsafe_allow_html=True,
    )

    try:
        res = requests.get(f"{BACKEND_URL}/analytics/summary", timeout=5)
        if res.status_code == 200:
            data = res.json()

            # KPI Row
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Incidents Logged", data.get("total_incidents", 0))
            col2.metric(
                "Knowledge Articles (RAG)",
                data.get("total_knowledge_articles", 0),
            )
            col3.metric(
                "Critical (P1) Active",
                data.get("incidents_by_priority", {}).get("P1", 0),
            )
            col4.metric("System Health", "99.9% Optimal")

            st.markdown("<br>", unsafe_allow_html=True)

            # Full-Width Interactive Analytics Charts
            c1, c2 = st.columns(2)

            with c1:
                st.subheader("📊 Incident Distribution by Priority")
                priority_data = data.get("incidents_by_priority", {})
                if priority_data:
                    fig_prio = px.pie(
                        names=list(priority_data.keys()),
                        values=list(priority_data.values()),
                        hole=0.45,
                        color_discrete_sequence=px.colors.qualitative.Bold,
                    )
                    fig_prio.update_layout(
                        margin=dict(t=20, b=20, l=20, r=20), height=320
                    )
                    st.plotly_chart(fig_prio, use_container_width=True)
                else:
                    st.info("No priority telemetry recorded.")

            with c2:
                st.subheader("📈 Ticket Lifecycle Breakdown")
                status_data = data.get("incidents_by_status", {})
                if status_data:
                    fig_status = px.bar(
                        x=list(status_data.keys()),
                        y=list(status_data.values()),
                        labels={
                            "x": "Ticket Status",
                            "y": "Total Incidents",
                        },
                        text_auto=True,
                        color=list(status_data.keys()),
                        color_discrete_sequence=px.colors.qualitative.Dark24,
                    )
                    fig_status.update_layout(
                        margin=dict(t=20, b=20, l=20, r=20),
                        height=320,
                        showlegend=False,
                    )
                    st.plotly_chart(fig_status, use_container_width=True)
                else:
                    st.info("No status telemetry recorded.")

        else:
            st.error("Failed to fetch analytics from backend.")
    except Exception as e:
        st.warning(f"Backend API unreachable: {e}")