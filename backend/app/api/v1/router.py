from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, incidents, ml, knowledge, analysis, agent

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health Checks"])
api_router.include_router(incidents.router, tags=["Incidents Management"])
api_router.include_router(ml.router, tags=["Machine Learning"])
api_router.include_router(knowledge.router, tags=["Knowledge Base & RAG"])
api_router.include_router(analysis.router, tags=["AI Resolution Engine"])
api_router.include_router(agent.router, tags=["Controlled AI Agent"])