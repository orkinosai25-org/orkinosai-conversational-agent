"""Account schemas"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class AccountBase(BaseModel):
    """Base account schema"""
    name: str
    slug: str = Field(..., pattern="^[a-z0-9-]+$")


class AccountCreate(AccountBase):
    """Schema for creating an account"""
    subscription_tier: str = "free"
    max_agents: int = 1
    max_users: int = 1


class AccountUpdate(BaseModel):
    """Schema for updating an account"""
    name: Optional[str] = None
    subscription_tier: Optional[str] = None
    is_active: Optional[bool] = None
    max_agents: Optional[int] = None
    max_users: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None


class AccountResponse(AccountBase):
    """Schema for account response"""
    id: int
    subscription_tier: str
    is_active: bool
    max_agents: int
    max_users: int
    settings: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
