"""Tests for UI and new API endpoints."""

import pytest
from src.api.app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app("config.yaml")
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Test that index page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Orkinosai' in response.data


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'agent' in data


def test_register_endpoint(client):
    """Test user registration."""
    response = client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpassword123',
        'name': 'Test User'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert 'token' in data
    assert 'user' in data
    assert data['user']['email'] == 'test@example.com'


def test_register_duplicate_user(client):
    """Test registering duplicate user."""
    # Register first user
    client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    
    # Try to register again
    response = client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    assert response.status_code == 400


def test_login_endpoint(client):
    """Test user login."""
    # Register user first
    client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'testpassword123',
        'name': 'Test User'
    })
    
    # Login
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpassword123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'token' in data
    assert 'user' in data


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post('/auth/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401


def test_train_from_url(client):
    """Test URL training endpoint."""
    response = client.post('/training/url', json={
        'url': 'https://example.com'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert 'training_id' in data


def test_train_from_url_missing_url(client):
    """Test URL training without URL."""
    response = client.post('/training/url', json={})
    assert response.status_code == 400


def test_get_documents_empty(client):
    """Test getting documents when none uploaded."""
    response = client.get('/training/documents')
    assert response.status_code == 200
    data = response.get_json()
    assert 'documents' in data
    assert len(data['documents']) == 0


def test_chat_with_mock_client(client):
    """Test chat endpoint with mock client."""
    response = client.post('/chat', json={
        'conversation_id': 'test-conv',
        'message': 'Hello!'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'assistant_message' in data
    assert 'usage' in data


def test_chat_missing_message(client):
    """Test chat without message."""
    response = client.post('/chat', json={
        'conversation_id': 'test-conv'
    })
    assert response.status_code == 400
