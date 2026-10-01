import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/api/v1"


def render_agent():
    st.title("🤖 Controlled Multi-Step Troubleshooting Agent")
    st.write("A stateful AI assistant utilizing predefined application tools.")

    if "history" not in st.session_state:
        st.session_state.history = []
    if "agent_data" not in st.session_state:
        st.session_state.agent_data = None

    if st.button("🔄 Start New Troubleshooting Session"):
        st.session_state.history = []
        st.session_state.agent_data = None
        st.rerun()

    inc_title = st.text_input("Incident Title", "VPN connects but internal website times out")
    inc_cat = st.selectbox("Category", ["Network", "Software", "Hardware", "Database", "Authentication"])
    inc_desc = st.text_area("Initial Symptom", "User connects to Cisco VPN successfully but cannot load internal portal.")

    feedback = ""
    if st.session_state.agent_data:
        st.info(f"👉 **Suggested Action:** {st.session_state.agent_data['recommended_action']}")
        feedback = st.text_input("User Feedback / Step Outcome:", "")

    if st.button("Submit to Agent"):
        payload = {
            "title": inc_title,
            "description": inc_desc,
            "category": inc_cat,
            "user_feedback": feedback,
            "conversation_history": st.session_state.history
        }
        res = requests.post(f"{BACKEND_URL}/agent/step", json=payload)
        if res.status_code == 200:
            st.session_state.agent_data = res.json()
            if feedback:
                st.session_state.history.append(f"Outcome: {feedback}")
            st.rerun()

    if st.session_state.agent_data:
        data = st.session_state.agent_data
        st.markdown("---")
        st.subheader("📚 Evidence Retrieved")
        for ev in data["evidence_retrieved"]:
            st.write(f"- 📖 {ev}")