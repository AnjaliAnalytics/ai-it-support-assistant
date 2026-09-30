import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="AI IT Support Assistant",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ AI-Powered IT Support & Incident Resolution Assistant")
st.subheader("Automated Incident Classification, RAG Knowledge Retrieval & Controlled AI Agent")

# Sidebar Navigation
navigation = st.sidebar.radio(
    "Navigation",
    ["System Health", "Interactive AI Agent Workflow", "AI Analysis Page", "Knowledge Base Search", "Predict Priority"]
)

if navigation == "System Health":
    st.header("System Operational Status")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("✅ Backend API is Operational")
            st.json(response.json())
        else:
            st.error("❌ Backend API Returned Error")
    except Exception as e:
        st.error(f"❌ Failed to connect to Backend API: {e}")

elif navigation == "Interactive AI Agent Workflow":
    st.header("🤖 Controlled Multi-Step AI Troubleshooting Agent")
    st.write("The AI agent uses grounded application tools to guide you through interactive troubleshooting step-by-step.")

    # Initialize Session State
    if "agent_history" not in st.session_state:
        st.session_state.agent_history = []
    if "agent_step_data" not in st.session_state:
        st.session_state.agent_step_data = None

    col_reset, _ = st.columns([1, 4])
    with col_reset:
        if st.button("🔄 Start New Incident Session"):
            st.session_state.agent_history = []
            st.session_state.agent_step_data = None
            st.rerun()

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        inc_title = st.text_input("Incident Title", "VPN connects but internal apps fail")
        inc_cat = st.selectbox("Category", ["Network", "Software", "Hardware", "Database", "Authentication"])
    with col2:
        inc_desc = st.text_area("Initial Symptom Description", "VPN connects successfully, but internal web portals time out.")

    # Step Feedback Section
    user_feedback = ""
    if st.session_state.agent_step_data:
        st.info(f"**Current Troubleshooting Step #{st.session_state.agent_step_data['current_step']}**")
        st.warning(f"👉 **Action to Perform:** {st.session_state.agent_step_data['recommended_action']}")
        user_feedback = st.text_input("Enter outcome / feedback after trying the action above:", "")

    btn_label = "Begin Agent Diagnostics" if not st.session_state.agent_step_data else "Submit Step Result to Agent"
    
    if st.button(btn_label, type="primary"):
        with st.spinner("Agent running tools & processing reasoning..."):
            payload = {
                "title": inc_title,
                "description": inc_desc,
                "category": inc_cat,
                "user_feedback": user_feedback,
                "conversation_history": st.session_state.agent_history
            }
            try:
                res = requests.post(f"{BACKEND_URL}/agent/step", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.session_state.agent_step_data = data
                    if user_feedback:
                        st.session_state.agent_history.append(f"Step outcome: {user_feedback}")
                    else:
                        st.session_state.agent_history.append(f"Initial diagnostic started for '{inc_title}'")
                    st.rerun()
                else:
                    st.error("Agent failed to process step.")
            except Exception as e:
                st.error(f"Failed to communicate with agent backend: {e}")

    # Display Workflow Metrics & Grounded Evidence
    if st.session_state.agent_step_data:
        step_data = st.session_state.agent_step_data
        st.markdown("---")
        st.subheader("📋 Step Diagnostic Results")

        m1, m2, m3 = st.columns(3)
        m1.metric("Troubleshooting Step", f"Step #{step_data['current_step']}")
        m2.metric("Workflow Status", step_data["status"])
        m3.metric("Escalation Advised", "YES" if step_data["escalation_recommended"] else "NO")

        st.write(f"**AI Diagnosis:** {step_data['ai_summary']}")
        st.info(f"**Suspected Cause:** {step_data['possible_cause']}")

        st.subheader("📚 Grounded Knowledge Base Evidence Used by Agent")
        for ev in step_data["evidence_retrieved"]:
            st.write(f"- 📖 {ev}")

elif navigation == "AI Analysis Page":
    st.header("⚡ Full AI Incident Resolution Workbench")
    title = st.text_input("Incident Title", "Cannot connect to Cisco VPN")
    cat = st.selectbox("Category", ["Network", "Software", "Hardware", "Database", "Authentication"])
    desc = st.text_area("Detailed Description", "User receives timeout error when connecting to VPN.")
    if st.button("Run AI Resolution Pipeline"):
        res = requests.post(f"{BACKEND_URL}/analysis/resolve", json={"title": title, "description": desc, "category": cat, "system_criticality": "High", "affected_users": 25})
        if res.status_code == 200:
            st.json(res.json())

elif navigation == "Knowledge Base Search":
    st.header("📚 Semantic Knowledge Base Search (RAG)")
    query = st.text_input("Enter incident issue:", "Cannot connect to VPN network")
    if st.button("Search Knowledge Base"):
        res = requests.post(f"{BACKEND_URL}/knowledge/search", json={"query": query, "top_k": 3})
        if res.status_code == 200:
            st.json(res.json())

elif navigation == "Predict Priority":
    st.header("🤖 ML Incident Priority Prediction")
    desc = st.text_area("Incident Description", "Core database server high memory usage causing timeout.")
    if st.button("Predict Priority"):
        res = requests.post(f"{BACKEND_URL}/ml/predict-priority", json={"description": desc, "category": "Database", "system_criticality": "High", "affected_users": 50})
        if res.status_code == 200:
            st.json(res.json())