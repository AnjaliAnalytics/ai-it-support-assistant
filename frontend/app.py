import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="AI IT Support Assistant",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API Endpoint Config
BACKEND_HEALTH_URL = "http://127.0.0.1:8000/api/v1/health"

# Sidebar Navigation
st.sidebar.title("🛠️ IT Support Hub")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "New Incident",
        "AI Analysis",
        "Knowledge Base",
        "Incident History",
        "System Health",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Version: 1.0.0 Phase 2 Prototype")

# Navigation Routing
if page == "Overview":
    st.title("AI-Powered IT Support & Incident Resolution Assistant")
    st.subheader(
        "Automated Incident Classification, RAG Knowledge Retrieval & AI Recommendations"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 System Capabilities")
        st.markdown(
            """
        - **Instant Ticket Classification:** Machine learning powered categorisation and priority prediction.
        - **Semantic Knowledge Retrieval (RAG):** Context-aware searching of knowledge base articles.
        - **Grounded AI Guardrails:** Safe, non-destructive resolution steps powered by Gemini API.
        - **Full Lifecycle Management:** Real-time database tracking and incident audit logging.
        """
        )

    with col2:
        st.markdown("### 💻 Tech Stack")
        st.markdown(
            """
        - **Backend:** FastAPI + Python 3.10+
        - **Database:** PostgreSQL + SQLAlchemy
        - **Machine Learning:** Scikit-Learn + TF-IDF
        - **LLM Orchestration:** Google Gemini API
        - **Frontend:** Streamlit + Responsive UI
        """
        )

    st.info(
        "ℹ️ System initialised in Phase 2 mode. Core services ready for modular integration."
    )

elif page == "System Health":
    st.title("🖥️ System Health & Status")

    st.markdown("Checking connection to backend server...")

    try:
        response = requests.get(BACKEND_HEALTH_URL, timeout=3)
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Backend API is Operational")
            st.json(data)
        else:
            st.error(
                f"⚠️ Backend returned status code: {response.status_code}"
            )
    except Exception as e:
        st.error(
            "❌ Unable to connect to Backend FastAPI server. Ensure backend is running on port 8000."
        )

else:
    st.title(f"📂 {page}")
    st.warning(
        f"The **{page}** module is under development and scheduled for subsequent phases."
    )
    st.caption("All features will connect to live FastAPI backend services.")