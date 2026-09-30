from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.models.db_models import Incident, KnowledgeArticle
from backend.app.core.logging_config import logger


class AnalyticsService:
    @staticmethod
    def get_summary_metrics(db: Session) -> Dict[str, Any]:
        """
        Calculates aggregate operational metrics across incidents and knowledge articles.
        """
        logger.info("Computing analytics summary metrics.")
        total_incidents = db.query(func.count(Incident.id)).scalar() or 0
        total_kb_articles = db.query(func.count(KnowledgeArticle.id)).scalar() or 0

        # Count incidents by priority
        priority_counts = dict(
            db.query(Incident.priority, func.count(Incident.id))
            .group_by(Incident.priority)
            .all()
        )

        # Count incidents by status
        status_counts = dict(
            db.query(Incident.status, func.count(Incident.id))
            .group_by(Incident.status)
            .all()
        )

        return {
            "total_incidents": total_incidents,
            "total_knowledge_articles": total_kb_articles,
            "incidents_by_priority": priority_counts,
            "incidents_by_status": status_counts
        }