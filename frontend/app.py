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
    ["System Health", "Analytics Dashboard", "Interactive AI Agent Workflow", "AI Analysis Page", "Knowledge Base Search", "Predict Priority"]
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

elif navigation == "Analytics Dashboard":
    st.header("📊 Operational Analytics & Metrics")
    try:
        res = requests.get(f"{BACKEND_URL}/analytics/summary", timeout=5)
        if res.status_code == 200:
            data = res.json()
            c1, c2 = st.columns(2)
            c1.metric("Total Recorded Incidents", data["total_incidents"])
            c2.metric("Knowledge Base Articles", data["total_knowledge_articles"])

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Incidents by Priority")
                st.json(data["incidents_by_priority"])
            with col_b:
                st.subheader("Incidents by Status")
                st.json(data["incidents_by_status"])
        else:
            st.error("Failed to fetch analytics metrics.")
    except Exception as e:
        st.error(f"Backend API connection error: {e}")

elif navigation == "Interactive AI Agent Workflow":
    st.header("🤖 Controlled Multi-Step AI Troubleshooting Agent")
    if "agent_history" not in st.session_state:
        st.session_state.agent_history = []
    if "agent_step_data" not in st.session_state:
        st.session_state.agent_step_data = None

    if st.button("🔄 Reset Session"):
        st.session_state.agent_history = []
        st.session_state.agent_step_data = None
        st.rerun()

    inc_title = st.text_input("Incident Title", "VPN connects but internal apps fail")
    inc_cat = st.selectbox("Category", ["Network", "Software", "Hardware", "Database", "Authentication"])
    inc_desc = st.text_area("Symptom Description", "VPN connects successfully, but web portals time out.")

    user_feedback = ""
    if st.session_state.agent_step_data:
        st.info(f"**Action:** {st.session_state.agent_step_data['recommended_action']}")
        user_feedback = st.text_input("Feedback / Step Result:", "")

    if st.button("Submit to Agent"):
        payload = {
            "title": inc_title,
            "description": inc_desc,
            "category": inc_cat,
            "user_feedback": user_feedback,
            "conversation_history": st.session_state.agent_history
        }
        res = requests.post(f"{BACKEND_URL}/agent/step", json=payload)
        if res.status_code == 200:
            st.session_state.agent_step_data = res.json()
            st.rerun()

elif navigation == "AI Analysis Page":
    st.header("⚡ Full AI Incident Resolution Workbench")
    title = st.text_input("Incident Title", "Cannot connect to Cisco VPN")
    desc = st.text_area("Detailed Description", "User receives timeout error when connecting to VPN.")
    if st.button("Run AI Resolution Pipeline"):
        res = requests.post(f"{BACKEND_URL}/analysis/resolve", json={"title": title, "description": desc, "category": "Network", "system_criticality": "High", "affected_users": 25})
        if res.status_code == 200:
            st.json(res.json())

elif navigation == "Knowledge Base Search":
    st.header("📚 Semantic Knowledge Base Search (RAG)")
    query = st.text_input("Enter query:", "Cannot connect to VPN network")
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