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