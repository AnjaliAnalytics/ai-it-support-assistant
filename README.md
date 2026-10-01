# 🛠️ Enterprise AI-Powered IT Support & Incident Resolution Platform

An enterprise-grade, recruiter-focused AI SaaS platform that automates IT ticket priority classification, semantic Knowledge Base vector retrieval (RAG), grounded AI resolution synthesis, and multi-step agent troubleshooting workflows.

---

## 📌 Project Overview
Modern enterprise IT service desks receive hundreds of repetitive incidents daily. Manual classification and manual Knowledge Base searches lead to high Mean Time to Resolution (MTTR). 

This platform bridges classical Machine Learning with modern Generative AI to deliver:
1. **Automated Incident Priority Scoring** (Scikit-Learn).
2. **Grounded Evidence Retrieval** (TF-IDF Vector RAG).
3. **Controlled Multi-step AI Troubleshooting Agent** (Isolated Tool Execution Boundary).
4. **Structured Resolution Synthesis** (Google Gemini 2.5 Flash with deterministic JSON outputs).

---

## ✨ Features
- **Executive Operations Dashboard**: Interactive Plotly metrics displaying real-time incident lifecycle telemetry.
- **Automated Ticket Classification**: Predicts priority (`P1`-`P4`) with confidence scoring.
- **RAG Knowledge Base Engine**: TF-IDF vector similarity search providing grounded evidence to prevent LLM hallucinations.
- **Controlled Troubleshooting Agent**: Stateful multi-turn agent operating strictly within predefined application tools (`search_knowledge_base`, `get_similar_incidents`, etc.).
- **FastAPI REST Service Layer**: Modular ASGI API layer with strict Pydantic v2 validation and global exception handling.
- **Resilient Fallback Mode**: Graceful degradation to local RAG recommendations if Gemini API limit is reached.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Presentation_Layer [Presentation & Client Tier]
        User[IT Engineer / Client] -->|HTTP / REST Requests| UI[Streamlit SaaS Application UI]
    end

    UI <-->|CORS Protected REST API| API[FastAPI Backend Gateway]

    subgraph Intelligence_Core [Microservice Core & Analytics Layer]
        API --> ML[Scikit-Learn Classifier]
        API --> RAG[TF-IDF RAG Search Engine]
        API --> Agent[Controlled AI Agent]
    end

    subgraph Infrastructure_Tier [Synthesis & Data Tier]
        RAG -->|Context Ingestion| LLM[Google Gemini 2.5 Flash Engine]
        Agent -->|Tool Execution Results| LLM
        LLM -->|Structured JSON Output| API
        API <-->|SQLAlchemy ORM| DB[(PostgreSQL Database)]
    end
⚙️ Controlled Agent Execution Workflow
Code snippet
sequenceDiagram
    autonumber
    actor User as IT Engineer
    participant Agent as Controlled Agent Orchestrator
    participant Tools as Application Tools Boundary
    participant DB as PostgreSQL / RAG Index
    participant LLM as Google Gemini 2.5 Flash

    User->>Agent: Submit Incident Symptom Anomaly
    Agent->>Tools: Invoke search_knowledge_base()
    Tools->>DB: Query TF-IDF Vector Index
    DB-->>Tools: Return Top Grounded KB Articles
    Tools-->>Agent: Return Verified Evidence
    Agent->>LLM: Pass Grounded Evidence + State History
    LLM-->>Agent: Synthesize Remediation Action Steps
    Agent-->>User: Present Step Action & Await Feedback
🧰 Tech Stack
Backend: Python 3.12, FastAPI, Uvicorn, Pydantic v2

Database / ORM: PostgreSQL, SQLite, SQLAlchemy 2.0

Machine Learning: Scikit-Learn, Pandas, NumPy, Joblib

LLM & RAG: Google Gemini 2.5 Flash (google-genai), TF-IDF Cosine Similarity

Frontend UI: Streamlit, Plotly Express, Custom SaaS HTML/CSS

Testing & CI/CD: Pytest, Starlette TestClient, GitHub Actions

⚙️ Setup & Local Installation
1. Prerequisites
Python 3.12+ installed

Git installed

2. Clone Repository & Setup Virtual Environment
Bash
git clone [https://github.com/AnjaliAnalytics/ai-it-support-assistant.git](https://github.com/AnjaliAnalytics/ai-it-support-assistant.git)
cd ai-it-support-assistant

python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate
