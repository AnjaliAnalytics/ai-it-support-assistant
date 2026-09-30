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


# Gemini AI Analysis Schemas (Phase 6)
class AIAnalysisRequest(BaseModel):
    title: str = Field(..., min_length=5, json_schema_extra={"example": "Cannot connect to VPN"})
    description: str = Field(..., min_length=10, json_schema_extra={"example": "User receives timeout error when connecting to Mumbai VPN gateway."})
    category: Optional[str] = Field("Network", json_schema_extra={"example": "Network"})
    system_criticality: Optional[str] = Field("High", json_schema_extra={"example": "High"})
    affected_users: Optional[int] = Field(100, ge=1, json_schema_extra={"example": 100})


class AIAnalysisResponse(BaseModel):
    predicted_priority: str
    ml_confidence: float
    summary: str
    category_explanation: str
    priority_explanation: str
    recommended_steps: List[str]
    evidence_used: List[str]
    possible_cause: str
    escalation_needed: bool
    confidence: str
    limitations: str
    fallback_used: bool = False


    # Append to backend/app/models/pydantic_models.py

class AgentStepRequest(BaseModel):
    title: str = Field(..., min_length=3, json_schema_extra={"example": "VPN connection application issue"})
    description: str = Field(..., min_length=5, json_schema_extra={"example": "VPN connects but internal app fails to open."})
    category: Optional[str] = Field("Network", json_schema_extra={"example": "Network"})
    user_feedback: Optional[str] = Field("", json_schema_extra={"example": "I restarted VPN but app still gives 404."})
    conversation_history: Optional[List[str]] = Field(default_factory=list)


class AgentStepResponse(BaseModel):
    current_step: int
    status: str
    ai_summary: str
    recommended_action: str
    all_recommended_steps: List[str]
    evidence_retrieved: List[str]
    possible_cause: str
    escalation_recommended: bool
    fallback_used: bool