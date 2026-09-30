from fastapi import APIRouter
from backend.app.core.config import settings
from backend.app.core.logging_config import logger

router = APIRouter()


@router.get("/health", status_code=200)
def check_health():
    """
    Simple health check endpoint returning system status.
    """
    logger.info("Health check endpoint pinged.")
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
    }