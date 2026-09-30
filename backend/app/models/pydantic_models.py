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