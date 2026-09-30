import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    priority = Column(String(50), nullable=True)
    status = Column(String(50), default="OPEN", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    analysis = relationship(
        "IncidentAnalysis", back_populates="incident", uselist=False, cascade="all, delete-orphan"
    )


class KnowledgeArticle(Base):
    __tablename__ = "knowledge_articles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class IncidentAnalysis(Base):
    __tablename__ = "incident_analyses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=False)
    classification = Column(String(100), nullable=False)
    priority_prediction = Column(String(50), nullable=False)
    retrieved_context = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    recommended_steps = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    incident = relationship("Incident", back_populates="analysis")