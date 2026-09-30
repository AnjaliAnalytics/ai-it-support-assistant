from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.models.db_models import Incident, KnowledgeArticle
from backend.app.models.pydantic_models import IncidentCreate, KnowledgeArticleCreate


class IncidentService:
    @staticmethod
    def create_incident(db: Session, incident_in: IncidentCreate) -> Incident:
        db_incident = Incident(
            title=incident_in.title,
            description=incident_in.description,
            category=incident_in.category or "Unassigned",
            priority=incident_in.priority or "Low",
        )
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
        return db_incident

    @staticmethod
    def get_incidents(db: Session, skip: int = 0, limit: int = 20) -> List[Incident]:
        return db.query(Incident).offset(skip).limit(limit).all()

    @staticmethod
    def get_incident_by_id(db: Session, incident_id: str) -> Optional[Incident]:
        return db.query(Incident).filter(Incident.id == incident_id).first()


class KBService:
    @staticmethod
    def create_article(db: Session, article_in: KnowledgeArticleCreate) -> KnowledgeArticle:
        db_article = KnowledgeArticle(
            title=article_in.title,
            category=article_in.category,
            content=article_in.content,
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article

    @staticmethod
    def get_articles(db: Session, skip: int = 0, limit: int = 50) -> List[KnowledgeArticle]:
        return db.query(KnowledgeArticle).offset(skip).limit(limit).all()