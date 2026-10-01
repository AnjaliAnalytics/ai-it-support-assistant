import streamlit as st
import streamlit.components.v1 as components


def render_visual_architecture():
    """Renders a full-height HTML/CSS visual architecture diagram."""
    html_code = """
    <style>
        .arch-container {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #0f172a;
            border-radius: 16px;
            padding: 24px;
            color: #f8fafc;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }
        .arch-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            gap: 16px;
        }
        .arch-card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 16px;
            flex: 1;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .arch-card:hover {
            border-color: #38bdf8;
            transform: translateY(-2px);
        }
        .card-icon {
            font-size: 26px;
            margin-bottom: 8px;
        }
        .card-title {
            font-weight: 700;
            font-size: 15px;
            color: #f1f5f9;
            margin-bottom: 4px;
        }
        .card-desc {
            font-size: 12px;
            color: #94a3b8;
            line-height: 1.4;
        }
        .arch-arrow {
            color: #38bdf8;
            font-size: 22px;
            font-weight: bold;
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 600;
            margin-top: 8px;
        }
        .badge-blue { background: rgba(56, 189, 248, 0.2); color: #38bdf8; }
        .badge-green { background: rgba(74, 222, 128, 0.2); color: #4ade80; }
        .badge-purple { background: rgba(192, 132, 252, 0.2); color: #c084fc; }
        .badge-amber { background: rgba(251, 191, 36, 0.2); color: #fbbf24; }
        .section-header {
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #64748b;
            margin-bottom: 12px;
            font-weight: 700;
        }
    </style>

    <div class="arch-container">
        <!-- Tier 1: Client & Presentation Layer -->
        <div class="section-header">1. Presentation & API Gateway Layer</div>
        <div class="arch-row">
            <div class="arch-card">
                <div class="card-icon">👤</div>
                <div class="card-title">User / IT Engineer</div>
                <div class="card-desc">Submits incident anomaly symptoms</div>
                <span class="badge badge-blue">Client Session</span>
            </div>
            <div class="arch-arrow">➔</div>
            <div class="arch-card">
                <div class="card-icon">💻</div>
                <div class="card-title">Streamlit SaaS UI</div>
                <div class="card-desc">Interactive dashboard & state engine</div>
                <span class="badge badge-blue">Frontend App</span>
            </div>
            <div class="arch-arrow">➔</div>
            <div class="arch-card">
                <div class="card-icon">🚀</div>
                <div class="card-title">FastAPI Backend Gateway</div>
                <div class="card-desc">ASGI Router, Pydantic V2 & CORS</div>
                <span class="badge badge-green">REST API</span>
            </div>
        </div>

        <!-- Tier 2: Microservice Core Layer -->
        <div class="section-header">2. Intelligence & Microservice Engine</div>
        <div class="arch-row">
            <div class="arch-card">
                <div class="card-icon">🤖</div>
                <div class="card-title">Scikit-Learn Classifier</div>
                <div class="card-desc">Logistic Regression N-gram model for priority scoring</div>
                <span class="badge badge-purple">ML Engine</span>
            </div>
            <div class="arch-card">
                <div class="card-icon">📚</div>
                <div class="card-title">TF-IDF RAG Search</div>
                <div class="card-desc">Cosine Similarity vector retrieval over KB articles</div>
                <span class="badge badge-purple">RAG Vector Retrieval</span>
            </div>
            <div class="arch-card">
                <div class="card-icon">🛡️️</div>
                <div class="card-title">Controlled Agent</div>
                <div class="card-desc">Tool execution boundary preventing arbitrary code</div>
                <span class="badge badge-purple">Stateful Agent</span>
            </div>
        </div>

        <!-- Tier 3: Synthesis & Persistence Layer -->
        <div class="section-header">3. Synthesis & Persistence Layer</div>
        <div class="arch-row">
            <div class="arch-card">
                <div class="card-icon">⚡</div>
                <div class="card-title">Google Gemini 2.5 Flash</div>
                <div class="card-desc">Grounded resolution synthesis & structured response</div>
                <span class="badge badge-amber">LLM Engine</span>
            </div>
            <div class="arch-arrow">➔</div>
            <div class="arch-card">
                <div class="card-icon">💾</div>
                <div class="card-title">PostgreSQL Database</div>
                <div class="card-desc">SQLAlchemy ORM persistence for tickets & articles</div>
                <span class="badge badge-amber">Database Layer</span>
            </div>
        </div>
    </div>
    """
    # Increased height to 680 to prevent clipping
    components.html(html_code, height=680, scrolling=False)


def render_about():
    st.markdown('<div class="header-title">🏢 Enterprise AI IT Support Platform Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-subtitle">System Specification, Workflow Pipeline & Technical Architecture Guide</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🌐 System Architecture",
        "⚙️ Tool & Agent Engine",
        "🧠 RAG & LLM Integration",
        "🛡️ Enterprise Security & Tech Stack"
    ])

    with tab1:
        st.subheader("1. System Topology & Pipeline Flow Diagram")
        st.write("End-to-end request processing flow across microservices.")

        render_visual_architecture()

        st.markdown("---")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("**Frontend Layer**\n\nModular Streamlit UI with Plotly analytics charts, responsive SaaS styling, and dynamic state tracking.")
        with c2:
            st.success("**API & Service Layer**\n\nFastAPI ASGI server with asynchronous router endpoints, Pydantic v2 schemas, and dependency injection.")
        with c3:
            st.warning("**Data & Intelligence**\n\nPostgreSQL storage paired with Scikit-Learn priority classification, TF-IDF RAG, and Gemini LLM synthesis.")

    with tab2:
        st.subheader("2. Controlled Agent Execution Engine & Tools")
        st.write("The agent operates under a strict tool abstraction layer, isolating the LLM from executing raw code or SQL.")

        st.markdown("""
        #### Predefined Application Tools
        - **`search_knowledge_base()`**: Pulls top-K relevant Knowledge Articles using TF-IDF cosine similarity.
        - **`get_similar_incidents()`**: Fetches historical tickets under the same incident category.
        - **`get_incident_history()`**: Retrieves complete update audit trail for a ticket UUID.
        - **`get_incident_details()`**: Extracts user impact and system criticality metrics.
        - **`create_incident_summary()`**: Generates structured handovers for Tier-2 engineering escalation.
        """)

    with tab3:
        st.subheader("3. Machine Learning & RAG Deep Dive")
        
        col_ml, col_rag = st.columns(2)
        with col_ml:
            st.markdown("""
            #### 🤖 Machine Learning Classifier
            * **Algorithm**: Logistic Regression with TF-IDF N-Gram Feature Extraction.
            * **Target Labels**: `P1` (Critical Outage), `P2` (High Impairment), `P3` (Medium), `P4` (Low).
            * **Features Evaluated**: Text description, category, criticality, and affected users.
            """)

        with col_rag:
            st.markdown("""
            #### 📚 RAG Vector Retrieval Layer
            * **Vectorization**: TF-IDF Document Matrix.
            * **Distance Calculation**: Cosine Similarity between user query vector and KB article vectors.
            * **Grounding Threshold**: Top K=3 articles injected directly into LLM system prompt.
            """)

    with tab4:
        st.subheader("4. Tech Stack Specifications & Security")

        st.markdown("""
        | Layer | Technology | Key Responsibility |
        | :--- | :--- | :--- |
        | **Frontend UI** | Streamlit + Plotly | Interactive SaaS Workbench & Telemetry Dashboards |
        | **REST API** | FastAPI + Uvicorn | High-performance ASGI REST Service Layer |
        | **Data Validation** | Pydantic v2 | Strict Schema Validation & Type Enforcement |
        | **Database ORM** | SQLAlchemy 2.0 | Transactional persistence for tickets and articles |
        | **Database Engine** | PostgreSQL / Supabase | Enterprise Relational Database Storage |
        | **Machine Learning** | Scikit-Learn | Incident Priority Scoring & Confidence Estimation |
        | **LLM Engine** | Google Gemini API (`2.5 Flash`) | Grounded Diagnostic Synthesis & Remediation Steps |
        | **Test Suite** | Pytest + Starlette TestClient | Automated Unit & Integration Testing (100% Pass Rate) |
        """)