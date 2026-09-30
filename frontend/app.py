import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="AI IT Support Assistant",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ AI-Powered IT Support & Incident Resolution Assistant")
st.subheader("Automated Incident Classification, RAG Knowledge Retrieval & AI Recommendations")

# Sidebar Navigation
navigation = st.sidebar.radio(
    "Navigation",
    ["System Health", "AI Analysis Page", "Knowledge Base Search", "Predict Priority"]
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

elif navigation == "AI Analysis Page":
    st.header("⚡ Full AI Incident Resolution Workbench")
    st.write("Submit an incident to run Priority Classification, RAG Evidence Retrieval, and Grounded AI Resolution.")

    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Incident Title", "Cannot connect to Cisco VPN")
        cat = st.selectbox("Category", ["Network", "Software", "Hardware", "Database", "Authentication"])
        users = st.number_input("Affected Users", min_value=1, max_value=5000, value=25)
    with col2:
        crit = st.selectbox("System Criticality", ["Low", "Medium", "High", "Critical"])
        desc = st.text_area("Detailed Description", "User receives timeout error when connecting to Mumbai VPN gateway.")

    if st.button("Run AI Resolution Pipeline", type="primary"):
        with st.spinner("Processing ML prediction, retrieving KB context, and querying Gemini AI..."):
            payload = {
                "title": title,
                "description": desc,
                "category": cat,
                "system_criticality": crit,
                "affected_users": users
            }
            try:
                res = requests.post(f"{BACKEND_URL}/analysis/resolve", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.markdown("---")
                    
                    # Top Metric Row
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Predicted Priority", data["predicted_priority"])
                    m2.metric("ML Confidence", f"{int(data['ml_confidence']*100)}%")
                    m3.metric("Escalation Needed", "YES" if data["escalation_needed"] else "NO")
                    m4.metric("LLM Status", "Fallback Mode" if data["fallback_used"] else "Live Gemini 2.5")

                    # Explanations
                    st.subheader("📋 Executive Summary & Diagnosis")
                    st.write(data["summary"])
                    st.info(f"**Possible Cause:** {data['possible_cause']}")

                    col_left, col_right = st.columns(2)
                    with col_left:
                        st.subheader("🔧 Recommended Troubleshooting Steps")
                        for idx, step in enumerate(data["recommended_steps"], 1):
                            st.write(f"**{idx}.** {step}")
                    
                    with col_right:
                        st.subheader("📚 Grounded Evidence Used (RAG)")
                        for ev in data["evidence_used"]:
                            st.write(f"- {ev}")
                            
                        st.subheader("⚠️ Limitations")
                        st.caption(data["limitations"])
                else:
                    st.error("Analysis request failed.")
            except Exception as e:
                st.error(f"Failed to reach backend API: {e}")

elif navigation == "Knowledge Base Search":
    st.header("📚 Semantic Knowledge Base Search (RAG)")
    query = st.text_input("Enter incident issue or keywords:", "Cannot connect to VPN network")
    if st.button("Search Knowledge Base"):
        res = requests.post(f"{BACKEND_URL}/knowledge/search", json={"query": query, "top_k": 3})
        if res.status_code == 200:
            data = res.json()
            for article in data['articles']:
                with st.expander(f"📖 {article['title']} (Relevance: {int(article['relevance_score']*100)}%)"):
                    st.write(f"**Content Preview:** {article['content']}")

elif navigation == "Predict Priority":
    st.header("🤖 ML Incident Priority Prediction")
    desc = st.text_area("Incident Description", "Core database server high memory usage causing timeout.")
    if st.button("Predict Priority"):
        res = requests.post(
            f"{BACKEND_URL}/ml/predict-priority",
            json={"description": desc, "category": "Database", "system_criticality": "High", "affected_users": 50}
        )
        if res.status_code == 200:
            st.json(res.json())