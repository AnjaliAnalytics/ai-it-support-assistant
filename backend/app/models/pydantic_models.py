from datetime import datetime
from typing import List, Optional
from pydantic import ConfigDict, BaseModel, Field


# Incident Schemas
class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=255, json_schema_extra={"example": "Cannot connect to VPN"})
    description: str = Field(
        ..., min_length=10, json_schema_extra={"example": "My Cisco AnyConnect VPN fails to authenticate when working remotely."}
    )
    category: Optional[str] = Field(None, json_schema_extra={"example": "Network"})
    priority: Optional[str] = Field(None, json_schema_extra={"example": "High"})


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    category: Optional[str]
    priority: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


# Knowledge Article Schemas
class KnowledgeArticleCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=255)
    category: str = Field(..., json_schema_extra={"example": "Authentication"})
    content: str = Field(..., min_length=20)


class KnowledgeArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    category: str
    content: str
    created_at: datetime


# ML Schemas
class MLPredictRequest(BaseModel):
    description: str = Field(..., min_length=10, json_schema_extra={"example": "Core database server memory limit reached causing query timeouts."})
    category: Optional[str] = Field("Database", json_schema_extra={"example": "Database"})
    system_criticality: Optional[str] = Field("High", json_schema_extra={"example": "High"})
    affected_users: Optional[int] = Field(150, ge=1, le=10000, json_schema_extra={"example": 150})


class MLPredictResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    predicted_priority: str = Field(..., json_schema_extra={"example": "P1"})
    confidence: float = Field(..., json_schema_extra={"example": 0.9425})
    model_version: str = Field(..., json_schema_extra={"example": "1.0.0-logistic-regression"})


# RAG Knowledge Search Schemas
class KBSearchRequest(BaseModel):
    query: str = Field(..., min_length=3, json_schema_extra={"example": "VPN connects but internal applications fail to load"})
    top_k: Optional[int] = Field(3, ge=1, le=10, json_schema_extra={"example": 3})


class KBSearchItem(BaseModel):
    id: str
    title: str
    category: str
    content: str
    relevance_score: float


class KBSearchResponse(BaseModel):
    query: str
    total_results: int
    articles: List[KBSearchItem]