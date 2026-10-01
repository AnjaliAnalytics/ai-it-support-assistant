import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/api/v1"


def render_ai_analysis():
    st.title("⚡ AI Resolution Workbench")
    st.write("Grounded Gemini LLM Incident Analysis with RAG Context Retrieval")

    title = st.text_input("Incident Title", "High CPU usage on Core Database Cluster")
    cat = st.selectbox("Category", ["Database", "Network", "Software", "Hardware", "Authentication"])
    crit = st.selectbox("System Criticality", ["Critical", "High", "Medium", "Low"])
    users = st.number_input("Affected Users", value=150)
    desc = st.text_area("Description", "PostgreSQL database CPU utilization reached 98% with query thread locks.")

    if st.button("Run Full Resolution Engine", type="primary"):
        with st.spinner("Processing RAG context & querying Gemini..."):
            res = requests.post(
                f"{BACKEND_URL}/analysis/resolve",
                json={"title": title, "description": desc, "category": cat, "system_criticality": crit, "affected_users": users}
            )
            if res.status_code == 200:
                data = res.json()
                st.subheader("📋 Executive Summary")
                st.write(data["summary"])
                st.info(f"**Root Cause:** {data['possible_cause']}")

                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("🔧 Troubleshooting Steps")
                    for s in data["recommended_steps"]:
                        st.write(f"1. {s}")
                with c2:
                    st.subheader("📚 Grounded Evidence")
                    for e in data["evidence_used"]:
                        st.write(f"- {e}")
            else:
                st.error("Analysis failed.")