"""
Unit tests for the onboarding system.

Tests cover:
- Data models
- Content manager
- Onboarding service
- API endpoints
"""

import pytest
from datetime import datetime
from src.cms.onboarding import (
    OnboardingStep,
    OnboardingStepType,
    OnboardingState,
    OnboardingFlow,
    UserOnboardingProgress,
    OnboardingService,
    OnboardingContentManager
)


class TestOnboardingModels:
    """Test onboarding data models."""
    
    def test_onboarding_step_creation(self):
        """Test creating an onboarding step."""
        step = OnboardingStep(
            id="test_step",
            step_type=OnboardingStepType.WELCOME,
            order=0,
            title="Test Step",
            description="Test description"
        )
        
        assert step.id == "test_step"
        assert step.step_type == OnboardingStepType.WELCOME
        assert step.order == 0
        assert step.is_required is True
        assert step.is_completed is False
    
    def test_onboarding_flow_creation(self):
        """Test creating an onboarding flow."""
        steps = [
            OnboardingStep(
                id="step1",
                step_type=OnboardingStepType.WELCOME,
                order=0,
                title="Step 1",
                description="First step"
            ),
            OnboardingStep(
                id="step2",
                step_type=OnboardingStepType.PROFILE,
                order=1,
                title="Step 2",
                description="Second step"
            )
        ]
        
        flow = OnboardingFlow(
            id="test_flow",
            name="test_flow",
            title="Test Flow",
            description="Test flow description",
            steps=steps
        )
        
        assert flow.id == "test_flow"
        assert len(flow.steps) == 2
        assert flow.is_active is True
    
    def test_user_progress_creation(self):
        """Test creating user progress record."""
        progress = UserOnboardingProgress(
            id="progress1",
            user_id="user1",
            flow_id="test_flow"
        )
        
        assert progress.id == "progress1"
        assert progress.user_id == "user1"
        assert progress.state == OnboardingState.NOT_STARTED
        assert progress.current_step_index == 0
        assert len(progress.completed_steps) == 0
    
    def test_progress_percentage_calculation(self):
        """Test progress percentage calculation."""
        progress = UserOnboardingProgress(
            id="progress1",
            user_id="user1",
            flow_id="test_flow",
            completed_steps=["step1", "step2"]
        )
        
        # 2 out of 6 steps completed = 33.33%
        percentage = progress.get_progress_percentage(6)
        assert percentage == pytest.approx(33.33, rel=0.01)
    
    def test_is_step_completed(self):
        """Test checking if step is completed."""
        progress = UserOnboardingProgress(
            id="progress1",
            user_id="user1",
            flow_id="test_flow",
            completed_steps=["step1", "step2"]
        )
        
        assert progress.is_step_completed("step1") is True
        assert progress.is_step_completed("step3") is False


class TestOnboardingContentManager:
    """Test onboarding content manager."""
    
    def test_content_manager_initialization(self):
        """Test content manager initializes with default content."""
        manager = OnboardingContentManager()
        
        # Should have content for all step types
        welcome_content = manager.get_step_content(OnboardingStepType.WELCOME)
        assert 'title' in welcome_content
        assert 'description' in welcome_content
        assert 'content' in welcome_content
    
    def test_get_step_content(self):
        """Test getting content for a step type."""
        manager = OnboardingContentManager()
        
        content = manager.get_step_content(OnboardingStepType.WELCOME)
        assert content['title'] == 'Welcome to Orkinosai! 🚀'
        assert 'hero_text' in content['content']
    
    def test_personalized_content(self):
        """Test content personalization with user context."""
        manager = OnboardingContentManager()
        
        # Get welcome content with user name
        content = manager.get_step_content(
            OnboardingStepType.WELCOME,
            user_context={'name': 'John'}
        )
        
        # Title should be personalized
        assert 'John' in content['title']
    
    def test_update_content(self):
        """Test updating content for a step type."""
        manager = OnboardingContentManager()
        
        # Update welcome content
        new_content = {
            'title': 'Custom Welcome',
            'description': 'Custom description',
            'content': {},
            'cta_text': 'Start',
            'skip_text': None
        }
        
        manager.update_content(OnboardingStepType.WELCOME, new_content)
        
        # Verify update
        content = manager.get_step_content(OnboardingStepType.WELCOME)
        assert content['title'] == 'Custom Welcome'
    
    def test_fallback_content(self):
        """Test fallback content for unknown step types."""
        manager = OnboardingContentManager()
        
        # Clear cache to test fallback
        manager._content_cache.clear()
        
        content = manager.get_step_content(OnboardingStepType.WELCOME)
        assert 'title' in content  # Should return fallback


class TestOnboardingService:
    """Test onboarding service."""
    
    def test_service_initialization(self):
        """Test service initializes with default flows."""
        service = OnboardingService()
        
        flows = service.list_flows()
        assert len(flows) > 0
        
        # Should have user_onboarding flow
        user_flow = service.get_flow("user_onboarding")
        assert user_flow is not None
        assert user_flow.name == "user_onboarding"
    
    def test_start_onboarding(self):
        """Test starting onboarding for a user."""
        service = OnboardingService()
        
        progress = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        assert progress is not None
        assert progress.user_id == "test_user"
        assert progress.flow_id == "user_onboarding"
        assert progress.state == OnboardingState.IN_PROGRESS
        assert progress.current_step_index == 0
    
    def test_start_onboarding_invalid_flow(self):
        """Test starting onboarding with invalid flow type."""
        service = OnboardingService()
        
        with pytest.raises(ValueError):
            service.start_onboarding(
                user_id="test_user",
                flow_type="invalid_flow"
            )
    
    def test_get_current_step(self):
        """Test getting current step."""
        service = OnboardingService()
        
        progress = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        step = service.get_current_step(progress.id)
        
        assert step is not None
        assert step.order == 0
        assert step.step_type == OnboardingStepType.WELCOME
    
    def test_get_current_step_with_context(self):
        """Test getting current step with user context."""
        service = OnboardingService()
        
        progress = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        step = service.get_current_step(
            progress.id,
            user_context={'name': 'Alice'}
        )
        
        # Title should be personalized
        assert 'Alice' in step.title
    
    def test_complete_step(self):
        """Test completing a step."""
        service = OnboardingService()
        
        progress = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        step = service.get_current_step(progress.id)
        
        # Complete the step
        success = service.complete_step(
            progress_id=progress.id,
            step_id=step.id,
            step_data={'test': 'data'}
        )
        
        assert success is True
        
        # Check progress updated
        updated_progress = service.get_progress(progress.id)
        assert updated_progress.current_step_index == 1
        assert step.id in updated_progress.completed_steps
        assert 'test' in updated_progress.step_data[step.id]
    
    def test_skip_step(self):
        """Test skipping an optional step."""
        service = OnboardingService()
        
        progress = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        # Move to profile step (which is optional)
        step = service.get_current_step(progress.id)
        service.complete_step(progress.id, step.id)
        
        # Get profile step
        profile_step = service.get_current_step(progress.id)
        
        # Skip it
        success = service.skip_step(progress.id, profile_step.id)
        assert success is True
        
        # Should move to next step
        updated_progress = service.get_progress(progress.id)
        assert updated_progress.current_step_index == 2
    
    def test_skip_required_step_fails(self):
        """Test that skipping a required step fails."""
        service = OnboardingService()
        
        progress = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        # Welcome step is required
        step = service.get_current_step(progress.id)
        
        # Try to skip it
        success = service.skip_step(progress.id, step.id)
        assert success is False
    
    def test_complete_all_steps(self):
        """Test completing all steps marks onboarding as complete."""
        service = OnboardingService()
        
        progress = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        flow = service.get_flow("user_onboarding")
        
        # Complete all steps
        for i in range(len(flow.steps)):
            step = service.get_current_step(progress.id)
            if step:
                if step.is_required:
                    service.complete_step(progress.id, step.id)
                else:
                    service.skip_step(progress.id, step.id)
        
        # Check onboarding is complete
        final_progress = service.get_progress(progress.id)
        assert final_progress.state == OnboardingState.COMPLETED
        assert final_progress.completed_at is not None
    
    def test_get_user_progress(self):
        """Test getting all progress for a user."""
        service = OnboardingService()
        
        # Start onboarding for user
        progress1 = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        # Get user progress
        user_progress = service.get_user_progress("test_user")
        
        assert len(user_progress) == 1
        assert user_progress[0].id == progress1.id
    
    def test_prevent_duplicate_onboarding(self):
        """Test that starting onboarding twice returns existing progress."""
        service = OnboardingService()
        
        # Start onboarding
        progress1 = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        # Try to start again
        progress2 = service.start_onboarding(
            user_id="test_user",
            flow_type="user_onboarding"
        )
        
        # Should return same progress
        assert progress1.id == progress2.id


class TestOnboardingFlow:
    """Test end-to-end onboarding flow."""
    
    def test_complete_user_onboarding_flow(self):
        """Test a complete user onboarding flow."""
        service = OnboardingService()
        
        # 1. Start onboarding
        progress = service.start_onboarding(
            user_id="new_user",
            flow_type="user_onboarding",
            metadata={'source': 'test'}
        )
        
        assert progress.state == OnboardingState.IN_PROGRESS
        
        # 2. Get welcome step
        step = service.get_current_step(
            progress.id,
            user_context={'name': 'Test User'}
        )
        assert step.step_type == OnboardingStepType.WELCOME
        
        # 3. Complete welcome
        service.complete_step(progress.id, step.id)
        
        # 4. Get profile step
        step = service.get_current_step(progress.id)
        assert step.step_type == OnboardingStepType.PROFILE
        
        # 5. Complete profile with data
        service.complete_step(
            progress.id,
            step.id,
            {'name': 'Test User', 'role': 'Developer'}
        )
        
        # 6. Continue through remaining steps
        while True:
            step = service.get_current_step(progress.id)
            if not step:
                break
            
            if step.is_required:
                service.complete_step(progress.id, step.id)
            else:
                service.skip_step(progress.id, step.id)
        
        # 7. Verify completion
        final_progress = service.get_progress(progress.id)
        assert final_progress.state == OnboardingState.COMPLETED
        assert len(final_progress.completed_steps) > 0
        assert final_progress.completed_at is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
