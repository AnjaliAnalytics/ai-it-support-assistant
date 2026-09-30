from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.pydantic_models import AIAnalysisRequest, AIAnalysisResponse
from backend.app.services.ml_service import MLService
from backend.app.services.rag_service import RAGService
from backend.app.services.gemini_service import GeminiService

router = APIRouter()


@router.post("/analysis/resolve", response_model=AIAnalysisResponse, status_code=status.HTTP_200_OK)
def analyze_and_resolve_incident(request: AIAnalysisRequest, db: Session = Depends(get_db)):
    """
    Complete Pipeline: ML Priority Prediction -> RAG KB Search -> Grounded Gemini AI Resolution Analysis.
    """
    # 1. ML Priority Prediction
    ml_result = MLService.predict_priority(
        description=request.description,
        category=request.category,
        system_criticality=request.system_criticality,
        affected_users=request.affected_users
    )

    # 2. Grounded RAG Search
    kb_results = RAGService.search_knowledge_base(db, query=f"{request.title} {request.description}", top_k=3)

    # 3. Gemini Resolution
    ai_result = GeminiService.generate_incident_analysis(
        title=request.title,
        description=request.description,
        category=request.category or "Unassigned",
        predicted_priority=ml_result["predicted_priority"],
        ml_confidence=ml_result["confidence"],
        kb_articles=kb_results
    )

    return {
        "predicted_priority": ml_result["predicted_priority"],
        "ml_confidence": ml_result["confidence"],
        "summary": ai_result.get("summary", ""),
        "category_explanation": ai_result.get("category_explanation", ""),
        "priority_explanation": ai_result.get("priority_explanation", ""),
        "recommended_steps": ai_result.get("recommended_steps", []),
        "evidence_used": ai_result.get("evidence_used", []),
        "possible_cause": ai_result.get("possible_cause", ""),
        "escalation_needed": ai_result.get("escalation_needed", False),
        "confidence": ai_result.get("confidence", "Medium"),
        "limitations": ai_result.get("limitations", "None"),
        "fallback_used": ai_result.get("fallback_used", False)
    }