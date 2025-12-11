"""User data models for CMS module"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class UserCreate(BaseModel):
    """Model for user registration"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password (min 8 characters)")
    name: str = Field(..., min_length=2, description="User full name")
    phone: Optional[str] = Field(None, description="User phone number")
    organization_name: Optional[str] = Field(None, description="Organization name")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format"""
        if v is None:
            return v
        # Remove common formatting characters
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.match(r'^\+?[1-9]\d{1,14}$', cleaned):
            raise ValueError('Invalid phone number format')
        return v


class UserLogin(BaseModel):
    """Model for user login"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class User(BaseModel):
    """User data model"""
    id: str = Field(..., description="User unique identifier")
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., description="User full name")
    phone: Optional[str] = Field(None, description="User phone number")
    organization_id: Optional[str] = Field(None, description="Organization ID")
    organization_name: Optional[str] = Field(None, description="Organization name")
    is_active: bool = Field(default=True, description="Whether user account is active")
    is_verified: bool = Field(default=False, description="Whether email is verified")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Account creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    last_login: Optional[datetime] = Field(None, description="Last login timestamp")
    onboarding_completed: bool = Field(default=False, description="Whether onboarding is completed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "user_123abc",
                "email": "john.doe@example.com",
                "name": "John Doe",
                "phone": "+1234567890",
                "organization_id": "org_456def",
                "organization_name": "Acme Corp",
                "is_active": True,
                "is_verified": True,
                "onboarding_completed": True
            }
        }


class UserResponse(BaseModel):
    """Response model for user operations"""
    success: bool = Field(..., description="Whether operation was successful")
    message: str = Field(..., description="Response message")
    user: Optional[User] = Field(None, description="User data")
    token: Optional[str] = Field(None, description="Authentication token")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "User registered successfully",
                "user": {
                    "id": "user_123abc",
                    "email": "john.doe@example.com",
                    "name": "John Doe"
                },
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }


class UserInDB(User):
    """User model with password hash for database storage"""
    password_hash: str = Field(..., description="Bcrypt password hash")
