from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.pydantic_models import KBSearchRequest, KBSearchResponse
from backend.app.services.rag_service import RAGService

router = APIRouter()


@router.post("/knowledge/search", response_model=KBSearchResponse, status_code=status.HTTP_200_OK)
def search_knowledge_base(request: KBSearchRequest, db: Session = Depends(get_db)):
    """
    Search Knowledge Base articles using vector similarity (RAG retrieval step).
    """
    results = RAGService.search_knowledge_base(db, query=request.query, top_k=request.top_k)
    return {
        "query": request.query,
        "total_results": len(results),
        "articles": results
    }