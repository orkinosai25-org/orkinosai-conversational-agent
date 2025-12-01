"""
Tests for CMS base classes

Basic tests to verify CMS structure is properly set up.
"""

import pytest
from datetime import datetime
from src.cms.base import (
    BaseEntity,
    ServiceResponse,
    CMSException,
    ValidationException,
    NotFoundException,
    PermissionDeniedException,
    DuplicateException
)


class TestBaseEntity:
    """Test BaseEntity model"""
    
    def test_base_entity_creation(self):
        """Test creating a BaseEntity instance"""
        entity = BaseEntity()
        assert entity.is_active is True
        assert entity.metadata == {}
        assert isinstance(entity.created_at, datetime)
        assert isinstance(entity.updated_at, datetime)
    
    def test_base_entity_with_data(self):
        """Test BaseEntity with custom data"""
        entity = BaseEntity(
            id="test-123",
            created_by="user-1",
            is_active=False,
            metadata={"key": "value"}
        )
        assert entity.id == "test-123"
        assert entity.created_by == "user-1"
        assert entity.is_active is False
        assert entity.metadata["key"] == "value"


class TestServiceResponse:
    """Test ServiceResponse model"""
    
    def test_success_response(self):
        """Test creating a success response"""
        response = ServiceResponse.success_response(
            message="Operation successful",
            data={"id": "123"}
        )
        assert response.success is True
        assert response.message == "Operation successful"
        assert response.data["id"] == "123"
        assert response.errors is None
    
    def test_error_response(self):
        """Test creating an error response"""
        response = ServiceResponse.error_response(
            message="Operation failed",
            errors=["Error 1", "Error 2"]
        )
        assert response.success is False
        assert response.message == "Operation failed"
        assert len(response.errors) == 2
        assert response.data is None


class TestCMSExceptions:
    """Test CMS exception classes"""
    
    def test_cms_exception(self):
        """Test CMSException"""
        with pytest.raises(CMSException) as exc_info:
            raise CMSException("Test error", code="TEST_ERROR")
        assert str(exc_info.value) == "Test error"
        assert exc_info.value.code == "TEST_ERROR"
    
    def test_validation_exception(self):
        """Test ValidationException"""
        with pytest.raises(ValidationException):
            raise ValidationException("Validation failed")
    
    def test_not_found_exception(self):
        """Test NotFoundException"""
        with pytest.raises(NotFoundException):
            raise NotFoundException("Entity not found")
    
    def test_permission_denied_exception(self):
        """Test PermissionDeniedException"""
        with pytest.raises(PermissionDeniedException):
            raise PermissionDeniedException("Access denied")
    
    def test_duplicate_exception(self):
        """Test DuplicateException"""
        with pytest.raises(DuplicateException):
            raise DuplicateException("Duplicate entry")
