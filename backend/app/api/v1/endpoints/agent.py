from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.pydantic_models import AgentStepRequest, AgentStepResponse
from backend.app.services.agent_service import TroubleshootingAgentService

router = APIRouter()


@router.post("/agent/step", response_model=AgentStepResponse, status_code=status.HTTP_200_OK)
def process_agent_troubleshooting_step(request: AgentStepRequest, db: Session = Depends(get_db)):
    """
    Execute a controlled agent state step utilizing tools and LLM analytical reasoning.
    """
    result = TroubleshootingAgentService.process_troubleshooting_step(
        db=db,
        title=request.title,
        description=request.description,
        category=request.category or "General",
        user_feedback=request.user_feedback or "",
        conversation_history=request.conversation_history or []
    )
    return result