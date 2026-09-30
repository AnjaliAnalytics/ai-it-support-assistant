from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    description: str = Field(..., min_length=10)
    category: Optional[str] = Field(None)
    priority: Optional[str] = Field(None)


class IncidentResponse(BaseModel):
    id: str
    title: str
    description: str
    category: Optional[str]
    priority: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class KnowledgeArticleCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    category: str = Field(...)
    content: str = Field(..., min_length=20)


class KnowledgeArticleResponse(BaseModel):
    id: str
    title: str
    category: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# Append to backend/app/models/pydantic_models.py

class MLPredictRequest(BaseModel):
    description: str = Field(..., min_length=10, example="Core database server memory limit reached causing query timeouts.")
    category: Optional[str] = Field("Database", example="Database")
    system_criticality: Optional[str] = Field("High", example="High")
    affected_users: Optional[int] = Field(150, ge=1, le=10000, example=150)


class MLPredictResponse(BaseModel):
    predicted_priority: str = Field(..., example="P1")
    confidence: float = Field(..., example=0.9425)
    model_version: str = Field(..., example="1.0.0-logistic-regression")