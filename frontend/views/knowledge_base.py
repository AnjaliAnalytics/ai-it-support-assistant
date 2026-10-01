import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/api/v1"


def render_knowledge_base():
    st.title("📚 Semantic Knowledge Base (RAG Search)")
    st.write("TF-IDF Vector Retrieval over IT Knowledge Articles")

    query = st.text_input("Enter search keywords or symptoms:", "VPN connection failure")
    top_k = st.slider("Results to return", 1, 5, 3)

    if st.button("Search Knowledge Base", type="primary"):
        res = requests.post(f"{BACKEND_URL}/knowledge/search", json={"query": query, "top_k": top_k})
        if res.status_code == 200:
            data = res.json()
            st.success(f"Found {data['total_results']} matching articles.")
            for article in data["articles"]:
                with st.expander(f"📖 {article['title']} (Relevance: {int(article['relevance_score']*100)}%)"):
                    st.write(f"**Category:** {article['category']}")
                    st.write(f"**Content:** {article['content']}")
        else:
            st.error("Search query failed.")