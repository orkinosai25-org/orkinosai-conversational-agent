"""
User domain models

Data models for user management.
To be copied from orkinosaicms.
"""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import EmailStr, Field
from ..base import BaseEntity


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


class User(BaseEntity):
    """
    User entity
    
    Represents a user account in the system.
    """
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password_hash: Optional[str] = None  # Should be hashed, never plain text
    status: UserStatus = UserStatus.PENDING_VERIFICATION
    email_verified: bool = False
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    preferences: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True


class UserProfile(BaseEntity):
    """
    Extended user profile information
    
    Additional profile data that supplements the core User model.
    """
    user_id: str
    bio: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    social_links: Dict[str, str] = Field(default_factory=dict)
    timezone: str = "UTC"
    language: str = "en"
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
