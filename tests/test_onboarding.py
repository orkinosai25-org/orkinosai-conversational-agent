"""Tests for user onboarding functionality"""

import pytest
import json
from src.api import create_app
from src.cms_module.db.user_db import get_user_database
from src.cms_module.models.onboarding import OnboardingStep


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


@pytest.fixture
def registered_user(client):
    """Register a test user and return user data"""
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
    return data['user']


class TestOnboardingWorkflow:
    """Test onboarding workflow"""
    
    def test_start_onboarding(self, client, registered_user):
        """Test starting onboarding"""
        response = client.post(
            '/onboarding/start',
            data=json.dumps({"user_id": registered_user['id']}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Onboarding started successfully"
        assert 'progress' in data
        assert data['progress']['user_id'] == registered_user['id']
        assert data['progress']['current_step'] == OnboardingStep.WELCOME.value
        assert data['progress']['status'] == 'in_progress'
        assert len(data['progress']['completed_steps']) == 0
    
    def test_get_onboarding_progress(self, client, registered_user):
        """Test getting onboarding progress"""
        # Start onboarding first
        client.post(
            '/onboarding/start',
            data=json.dumps({"user_id": registered_user['id']}),
            content_type='application/json'
        )
        
        # Get progress
        response = client.get(f"/onboarding/progress/{registered_user['id']}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user_id'] == registered_user['id']
        assert data['current_step'] == OnboardingStep.WELCOME.value
        assert data['status'] == 'in_progress'
    
    def test_complete_onboarding_step(self, client, registered_user):
        """Test completing an onboarding step"""
        # Start onboarding
        client.post(
            '/onboarding/start',
            data=json.dumps({"user_id": registered_user['id']}),
            content_type='application/json'
        )
        
        # Complete welcome step
        response = client.post(
            '/onboarding/step/complete',
            data=json.dumps({
                "user_id": registered_user['id'],
                "step": OnboardingStep.WELCOME.value,
                "data": {"acknowledged": True}
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == f"Step {OnboardingStep.WELCOME.value} completed successfully"
        assert OnboardingStep.WELCOME.value in data['progress']['completed_steps']
        assert data['progress']['current_step'] == OnboardingStep.PROFILE_SETUP.value
    
    def test_complete_profile_setup(self, client, registered_user):
        """Test completing profile setup step"""
        # Start onboarding and complete welcome
        client.post(
            '/onboarding/start',
            data=json.dumps({"user_id": registered_user['id']}),
            content_type='application/json'
        )
        client.post(
            '/onboarding/step/complete',
            data=json.dumps({
                "user_id": registered_user['id'],
                "step": OnboardingStep.WELCOME.value,
                "data": {}
            }),
            content_type='application/json'
        )
        
        # Complete profile setup
        profile_data = {
            "job_title": "Product Manager",
            "department": "Product",
            "bio": "Building great products"
        }
        response = client.post(
            '/onboarding/step/complete',
            data=json.dumps({
                "user_id": registered_user['id'],
                "step": OnboardingStep.PROFILE_SETUP.value,
                "data": profile_data
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert OnboardingStep.PROFILE_SETUP.value in data['progress']['completed_steps']
        
        # Verify profile was created
        profile_response = client.get(f"/profile/{registered_user['id']}")
        assert profile_response.status_code == 200
        profile = json.loads(profile_response.data)
        assert profile['job_title'] == profile_data['job_title']
        assert profile['department'] == profile_data['department']
        assert profile['bio'] == profile_data['bio']
    
    def test_complete_preferences_step(self, client, registered_user):
        """Test completing preferences step"""
        # Start onboarding and complete first two steps
        client.post(
            '/onboarding/start',
            data=json.dumps({"user_id": registered_user['id']}),
            content_type='application/json'
        )
        client.post(
            '/onboarding/step/complete',
            data=json.dumps({
                "user_id": registered_user['id'],
                "step": OnboardingStep.WELCOME.value,
                "data": {}
            }),
            content_type='application/json'
        )
        client.post(
            '/onboarding/step/complete',
            data=json.dumps({
                "user_id": registered_user['id'],
                "step": OnboardingStep.PROFILE_SETUP.value,
                "data": {}
            }),
            content_type='application/json'
        )
        client.post(
            '/onboarding/step/complete',
            data=json.dumps({
                "user_id": registered_user['id'],
                "step": OnboardingStep.ORGANIZATION_SETUP.value,
                "data": {}
            }),
            content_type='application/json'
        )
        
        # Complete preferences
        preferences_data = {
            "theme": "dark",
            "language": "en",
            "notifications_enabled": False,
            "timezone": "America/New_York"
        }
        response = client.post(
            '/onboarding/step/complete',
            data=json.dumps({
                "user_id": registered_user['id'],
                "step": OnboardingStep.PREFERENCES.value,
                "data": preferences_data
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        # Verify preferences were saved
        profile_response = client.get(f"/profile/{registered_user['id']}")
        profile = json.loads(profile_response.data)
        assert profile['preferences']['theme'] == preferences_data['theme']
        assert profile['preferences']['language'] == preferences_data['language']
        assert profile['preferences']['notifications_enabled'] == preferences_data['notifications_enabled']
    
    def test_skip_onboarding(self, client, registered_user):
        """Test skipping onboarding"""
        # Start onboarding
        client.post(
            '/onboarding/start',
            data=json.dumps({"user_id": registered_user['id']}),
            content_type='application/json'
        )
        
        # Skip onboarding
        response = client.post(
            '/onboarding/skip',
            data=json.dumps({"user_id": registered_user['id']}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Onboarding skipped"
        assert data['progress']['status'] == 'skipped'
        
        # Verify user onboarding_completed is set
        from src.cms_module.db.user_db import get_user_database
        db = get_user_database()
        user = db.get_user_by_id(registered_user['id'])
        assert user.onboarding_completed is True


class TestUserProfile:
    """Test user profile management"""
    
    def test_update_profile(self, client, registered_user):
        """Test updating user profile"""
        profile_data = {
            "job_title": "Senior Developer",
            "department": "Engineering",
            "bio": "Passionate about coding",
            "preferences": {
                "theme": "dark",
                "language": "en"
            }
        }
        
        response = client.put(
            f"/profile/{registered_user['id']}",
            data=json.dumps(profile_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == "Profile updated successfully"
        assert data['profile']['job_title'] == profile_data['job_title']
        assert data['profile']['department'] == profile_data['department']
    
    def test_get_nonexistent_profile(self, client):
        """Test getting a profile that doesn't exist"""
        response = client.get("/profile/nonexistent_user_id")
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error'].lower()
    
    def test_get_progress_not_started(self, client, registered_user):
        """Test getting progress when onboarding not started"""
        response = client.get(f"/onboarding/progress/{registered_user['id']}")
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
