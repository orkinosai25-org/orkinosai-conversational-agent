"""
Base classes and utilities for CMS domain

This module contains common base classes and utilities shared across
all CMS modules. These should be generic and reusable.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class BaseEntity(BaseModel):
    """
    Base model for all CMS entities
    
    Provides common fields and functionality for all domain objects.
    """
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ServiceResponse(BaseModel):
    """
    Standard response wrapper for service operations
    
    Provides consistent response structure across all CMS services.
    """
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[list] = None
    
    @classmethod
    def success_response(cls, message: str, data: Optional[Dict[str, Any]] = None):
        """Create a success response"""
        return cls(success=True, message=message, data=data)
    
    @classmethod
    def error_response(cls, message: str, errors: Optional[list] = None):
        """Create an error response"""
        return cls(success=False, message=message, errors=errors)


class CMSException(Exception):
    """Base exception for CMS domain"""
    
    def __init__(self, message: str, code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationException(CMSException):
    """Raised when validation fails"""
    pass


class NotFoundException(CMSException):
    """Raised when entity is not found"""
    pass


class PermissionDeniedException(CMSException):
    """Raised when permission is denied"""
    pass


class DuplicateException(CMSException):
    """Raised when duplicate entry is detected"""
    pass
