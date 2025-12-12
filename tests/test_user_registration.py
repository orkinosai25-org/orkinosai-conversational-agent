"""Tests for CMS user registration and authentication"""

import pytest
import json
from src.api import create_app
from src.cms_module.db.user_db import get_user_database


@pytest.fixture
def app():
    """Create Flask app for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create Flask test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def clear_database():
    """Clear user database before each test"""
    db = get_user_database()
    db.clear()
    yield
    db.clear()


class TestUserRegistration:
    """Test user registration functionality"""
    
    def test_register_user_success(self, client):
        """Test successful user registration"""
        # Prepare registration data
        user_data = {
            "email": "test@example.com",
            "password": "TestPass123",
            "name": "Test User",
            "phone": "+1234567890",
            "organization_name": "Test Corp"
        }
        
        # Send registration request
        response = client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Verify response
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == "User registered successfully"
        assert 'token' in data
        assert data['token'] is not None
        assert 'user' in data
        assert data['user']['email'] == user_data['email']
        assert data['user']['name'] == user_data['name']
        assert data['user']['phone'] == user_data['phone']
        assert data['user']['organization_name'] == user_data['organization_name']
        assert data['user']['is_verified'] is False
        assert data['user']['onboarding_completed'] is False
    
    def test_register_user_duplicate_email(self, client):
        """Test registration with duplicate email"""
        user_data = {
            "email": "test@example.com",
            "password": "TestPass123",
            "name": "Test User"
        }
        
        # Register first user
        client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Try to register again with same email
        response = client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Verify error response
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'already exists' in data['error'].lower()
    
    def test_register_user_missing_fields(self, client):
        """Test registration with missing required fields"""
        # Missing password
        response = client.post(
            '/auth/register',
            data=json.dumps({"email": "test@example.com", "name": "Test"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Missing name
        response = client.post(
            '/auth/register',
            data=json.dumps({"email": "test@example.com", "password": "TestPass123"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Missing email
        response = client.post(
            '/auth/register',
            data=json.dumps({"name": "Test", "password": "TestPass123"}),
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_register_user_weak_password(self, client):
        """Test registration with weak password"""
        user_data = {
            "email": "test@example.com",
            "password": "weak",  # Too short, no uppercase, no digits
            "name": "Test User"
        }
        
        response = client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Should fail validation
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_register_user_invalid_email(self, client):
        """Test registration with invalid email"""
        user_data = {
            "email": "not-an-email",
            "password": "TestPass123",
            "name": "Test User"
        }
        
        response = client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Should fail validation
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data


class TestUserLogin:
    """Test user login functionality"""
    
    def test_login_success(self, client):
        """Test successful user login"""
        # First register a user
        user_data = {
            "email": "test@example.com",
            "password": "TestPass123",
            "name": "Test User"
        }
        client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Now login
        login_data = {
            "email": "test@example.com",
            "password": "TestPass123"
        }
        response = client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Verify response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Login successful"
        assert 'token' in data
        assert data['token'] is not None
        assert 'user' in data
        assert data['user']['email'] == user_data['email']
        assert 'last_login' in data['user']
    
    def test_login_invalid_email(self, client):
        """Test login with non-existent email"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "TestPass123"
        }
        response = client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Verify error response
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid' in data['error']
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password"""
        # Register user
        user_data = {
            "email": "test@example.com",
            "password": "TestPass123",
            "name": "Test User"
        }
        client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Try to login with wrong password
        login_data = {
            "email": "test@example.com",
            "password": "WrongPass456"
        }
        response = client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Verify error response
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid' in data['error']
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields"""
        # Missing password
        response = client.post(
            '/auth/login',
            data=json.dumps({"email": "test@example.com"}),
            content_type='application/json'
        )
        assert response.status_code == 400
        
        # Missing email
        response = client.post(
            '/auth/login',
            data=json.dumps({"password": "TestPass123"}),
            content_type='application/json'
        )
        assert response.status_code == 400


class TestPasswordSecurity:
    """Test password security features"""
    
    def test_password_hashing(self, client):
        """Test that passwords are properly hashed"""
        from src.cms_module.db.user_db import get_user_database
        
        # Register user
        user_data = {
            "email": "test@example.com",
            "password": "TestPass123",
            "name": "Test User"
        }
        client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        # Get user from database
        db = get_user_database()
        user_in_db = db.get_user_by_email("test@example.com")
        
        # Verify password is hashed (not plain text)
        assert user_in_db.password_hash != user_data['password']
        assert len(user_in_db.password_hash) > 50  # bcrypt hashes are long
        assert user_in_db.password_hash.startswith('$2b$')  # bcrypt format
    
    def test_jwt_token_format(self, client):
        """Test that JWT tokens are properly formatted"""
        # Register user
        user_data = {
            "email": "test@example.com",
            "password": "TestPass123",
            "name": "Test User"
        }
        response = client.post(
            '/auth/register',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        token = data['token']
        
        # JWT tokens have 3 parts separated by dots
        parts = token.split('.')
        assert len(parts) == 3
        
        # Each part should be base64-encoded
        for part in parts:
            assert len(part) > 0
