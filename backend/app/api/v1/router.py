from fastapi import APIRouter
from backend.app.api.v1.endpoints import health, incidents, ml

api_router = APIRouter()
api_router.include_router(health.router, tags=["Health Checks"])
api_router.include_router(incidents.router, tags=["Incidents Management"])
api_router.include_router(ml.router, tags=["Machine Learning"])