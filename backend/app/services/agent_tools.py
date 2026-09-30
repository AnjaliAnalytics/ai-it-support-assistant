from typing import List, Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.db_models import Incident, KnowledgeArticle
from backend.app.services.rag_service import RAGService
from backend.app.core.logging_config import logger


class AgentTools:
    @staticmethod
    def search_knowledge_base(db: Session, query: str) -> List[Dict[str, Any]]:
        """Tool 1: Search KB articles using TF-IDF vector retrieval."""
        logger.info(f"Agent Tool Invoked: search_knowledge_base('{query}')")
        return RAGService.search_knowledge_base(db, query=query, top_k=3)

    @staticmethod
    def get_similar_incidents(db: Session, category: str) -> List[Dict[str, Any]]:
        """Tool 2: Retrieve recent historical incidents in the same category."""
        logger.info(f"Agent Tool Invoked: get_similar_incidents('{category}')")
        incidents = db.query(Incident).filter(
            Incident.category.ilike(f"%{category}%")
        ).limit(3).all()
        return [
            {
                "id": inc.id,
                "title": inc.title,
                "priority": inc.priority,
                "status": inc.status
            }
            for inc in incidents
        ]

    @staticmethod
    def get_incident_history(db: Session, incident_id: str) -> Dict[str, Any]:
        """Tool 3: Get full lifecycle and update history for a specific incident."""
        logger.info(f"Agent Tool Invoked: get_incident_history('{incident_id}')")
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            return {"error": "Incident not found"}
        return {
            "id": incident.id,
            "title": incident.title,
            "status": incident.status,
            "created_at": str(incident.created_at),
            "updated_at": str(incident.updated_at)
        }

    @staticmethod
    def get_incident_details(db: Session, incident_id: str) -> Dict[str, Any]:
        """Tool 4: Get detailed description and metadata for an incident."""
        logger.info(f"Agent Tool Invoked: get_incident_details('{incident_id}')")
        incident = db.query(Incident).filter(Incident.id == incident_id).first()
        if not incident:
            return {"error": "Incident not found"}
        return {
            "id": incident.id,
            "title": incident.title,
            "description": incident.description,
            "category": incident.category,
            "priority": incident.priority,
            "status": incident.status
        }

    @staticmethod
    def create_incident_summary(title: str, description: str, steps_taken: List[str]) -> Dict[str, Any]:
        """Tool 5: Formulate a structured diagnostic summary for engineering handover."""
        logger.info("Agent Tool Invoked: create_incident_summary")
        return {
            "title": title,
            "summary": f"Incident '{title}' processed with {len(steps_taken)} troubleshooting step(s) applied.",
            "steps_taken": steps_taken,
            "ready_for_escalation": True
        }