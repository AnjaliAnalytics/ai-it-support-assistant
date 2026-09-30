from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.pydantic_models import AnalyticsSummaryResponse
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse, status_code=status.HTTP_200_OK)
def get_analytics_summary(db: Session = Depends(get_db)):
    """
    Retrieve operational KPI summary including incident counts by priority and status.
    """
    return AnalyticsService.get_summary_metrics(db)