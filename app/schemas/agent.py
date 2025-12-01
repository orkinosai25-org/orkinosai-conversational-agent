"""Agent schemas"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class AgentBase(BaseModel):
    """Base agent schema"""
    name: str
    description: Optional[str] = None
    agent_type: str = "conversational"


class AgentCreate(AgentBase):
    """Schema for creating an agent"""
    is_public: bool = False
    configuration: Optional[Dict[str, Any]] = None


class AgentUpdate(BaseModel):
    """Schema for updating an agent"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    configuration: Optional[Dict[str, Any]] = None


class AgentResponse(AgentBase):
    """Schema for agent response"""
    id: int
    is_active: bool
    is_public: bool
    training_status: str
    knowledge_sources: List[Dict[str, Any]]
    configuration: Dict[str, Any]
    azure_deployment_id: Optional[str] = None
    azure_model_version: Optional[str] = None
    owner_id: int
    account_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_trained_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TrainingRequest(BaseModel):
    """Schema for training request"""
    sources: List[Dict[str, Any]]  # List of URLs, documents, etc.
    azure_model: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
