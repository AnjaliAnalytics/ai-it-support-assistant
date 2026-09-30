import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(
    page_title="AI IT Support Assistant",
    page_icon="🛠️",
    layout="wide"
)

st.title("🛠️ AI-Powered IT Support & Incident Resolution Assistant")
st.subheader("Automated Incident Classification, RAG Knowledge Retrieval & AI Recommendations")

# Sidebar Navigation
navigation = st.sidebar.radio("Navigation", ["System Health", "Knowledge Base Search", "Predict Priority"])

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

elif navigation == "Knowledge Base Search":
    st.header("📚 Semantic Knowledge Base Search (RAG)")
    st.write("Search IT documentation, guides, and resolution workflows grounded in database articles.")
    
    query = st.text_input("Enter incident issue or keywords:", "Cannot connect to VPN network")
    
    if st.button("Search Knowledge Base"):
        with st.spinner("Retrieving relevant articles..."):
            try:
                res = requests.post(f"{BACKEND_URL}/knowledge/search", json={"query": query, "top_k": 3})
                if res.status_code == 200:
                    data = res.json()
                    st.success(f"Found {data['total_results']} relevant knowledge articles.")
                    for article in data['articles']:
                        with st.expander(f"📖 {article['title']} (Relevance: {int(article['relevance_score']*100)}%)"):
                            st.write(f"**Category:** {article['category']}")
                            st.write(f"**Article ID:** `{article['id']}`")
                            st.write(f"**Content Preview:** {article['content']}")
                else:
                    st.error("Error retrieving knowledge articles.")
            except Exception as e:
                st.error(f"Backend request failed: {e}")

elif navigation == "Predict Priority":
    st.header("🤖 ML Incident Priority Prediction")
    desc = st.text_area("Incident Description", "Core database server high memory usage causing timeout.")
    cat = st.selectbox("Category", ["Network", "Software", "Hardware", "Database", "Authentication"])
    crit = st.selectbox("System Criticality", ["Low", "Medium", "High", "Critical"])
    users = st.number_input("Affected Users", min_value=1, max_value=5000, value=50)

    if st.button("Predict Priority"):
        payload = {
            "description": desc,
            "category": cat,
            "system_criticality": crit,
            "affected_users": users
        }
        res = requests.post(f"{BACKEND_URL}/ml/predict-priority", json=payload)
        if res.status_code == 200:
            st.json(res.json())
        else:
            st.error("Prediction failed.")