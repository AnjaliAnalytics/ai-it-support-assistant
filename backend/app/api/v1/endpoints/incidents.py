from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.pydantic_models import IncidentCreate, IncidentResponse
from backend.app.services.incident_service import IncidentService

router = APIRouter()


@router.post("/incidents", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(incident_in: IncidentCreate, db: Session = Depends(get_db)):
    """
    Create a new IT incident ticket.
    """
    return IncidentService.create_incident(db, incident_in)


@router.get("/incidents", response_model=List[IncidentResponse])
def list_incidents(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Retrieve history of IT incident tickets.
    """
    return IncidentService.get_incidents(db, skip=skip, limit=limit)


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    """
    Get incident details by ID.
    """
    incident = IncidentService.get_incident_by_id(db, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident ticket not found")
    return incident