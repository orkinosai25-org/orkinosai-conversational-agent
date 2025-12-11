"""
Onboarding Service

This module provides the core onboarding service that manages user onboarding
flows, progress tracking, and step orchestration. It integrates with the CMS
content manager to provide dynamic, personalized onboarding experiences.

The service handles:
- Flow initialization and management
- Step progression and validation
- State persistence and recovery
- Progress tracking and analytics
- Integration with user management
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
import uuid
import logging

from .models import (
    OnboardingStep,
    OnboardingStepType,
    OnboardingState,
    OnboardingFlow,
    UserOnboardingProgress
)
from .content_manager import OnboardingContentManager

logger = logging.getLogger(__name__)


class OnboardingService:
    """
    Core service for managing user onboarding flows.
    
    This service orchestrates the entire onboarding process:
    1. Initialize onboarding flows for new users
    2. Track user progress through steps
    3. Validate step completion
    4. Provide content for each step via CMS
    5. Handle state transitions
    6. Collect and store user data
    
    The service uses the CMS content manager to provide dynamic,
    customizable content for each step, enabling:
    - Non-technical content updates
    - A/B testing of flows
    - Personalized experiences
    - Multi-language support
    
    Usage:
        service = OnboardingService()
        
        # Start onboarding for a new user
        progress = service.start_onboarding(
            user_id="user-123",
            flow_type="user_onboarding"
        )
        
        # Get current step
        step = service.get_current_step(progress.id)
        
        # Complete step and move to next
        service.complete_step(
            progress_id=progress.id,
            step_id=step.id,
            step_data={'profile': {'name': 'John'}}
        )
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the onboarding service.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.content_manager = OnboardingContentManager(config)
        
        # In-memory storage for demo (replace with database in production)
        self._flows: Dict[str, OnboardingFlow] = {}
        self._progress_records: Dict[str, UserOnboardingProgress] = {}
        
        # Initialize default flows
        self._initialize_default_flows()
    
    def _initialize_default_flows(self):
        """
        Initialize default onboarding flows.
        
        This method creates the standard onboarding flows that are
        available to all users. In production, flows would be loaded
        from a database and could be customized per organization.
        """
        # Standard user onboarding flow
        user_flow = self._create_user_onboarding_flow()
        self._flows[user_flow.id] = user_flow
        
        logger.info(f"Initialized {len(self._flows)} default onboarding flows")
    
    def _create_user_onboarding_flow(self) -> OnboardingFlow:
        """
        Create the standard user onboarding flow.
        
        This flow guides new users through:
        1. Welcome and introduction
        2. Profile setup
        3. Organization creation
        4. Plan selection
        5. Theme customization
        6. Completion and next steps
        
        Returns:
            Configured OnboardingFlow instance
        """
        flow_id = "user_onboarding"
        
        # Define the sequence of steps
        steps = [
            OnboardingStep(
                id=f"{flow_id}_welcome",
                step_type=OnboardingStepType.WELCOME,
                order=0,
                title="Welcome",
                description="Welcome to Orkinosai",
                is_required=True
            ),
            OnboardingStep(
                id=f"{flow_id}_profile",
                step_type=OnboardingStepType.PROFILE,
                order=1,
                title="Your Profile",
                description="Tell us about yourself",
                is_required=False
            ),
            OnboardingStep(
                id=f"{flow_id}_organization",
                step_type=OnboardingStepType.ORGANIZATION,
                order=2,
                title="Create Workspace",
                description="Set up your organization",
                is_required=True
            ),
            OnboardingStep(
                id=f"{flow_id}_plan",
                step_type=OnboardingStepType.PLAN_SELECTION,
                order=3,
                title="Choose Plan",
                description="Select your subscription plan",
                is_required=False
            ),
            OnboardingStep(
                id=f"{flow_id}_theme",
                step_type=OnboardingStepType.THEME,
                order=4,
                title="Customize Theme",
                description="Choose your visual theme",
                is_required=False
            ),
            OnboardingStep(
                id=f"{flow_id}_completion",
                step_type=OnboardingStepType.COMPLETION,
                order=5,
                title="All Set!",
                description="Your setup is complete",
                is_required=True
            )
        ]
        
        return OnboardingFlow(
            id=flow_id,
            name="user_onboarding",
            title="User Onboarding",
            description="Standard onboarding flow for new users",
            steps=steps,
            target_role=None,
            is_active=True
        )
    
    def start_onboarding(
        self,
        user_id: str,
        flow_type: str = "user_onboarding",
        metadata: Optional[Dict[str, Any]] = None
    ) -> UserOnboardingProgress:
        """
        Start onboarding for a user.
        
        This method initializes a new onboarding session for a user,
        creating a progress record and setting up the initial state.
        
        Args:
            user_id: Unique identifier for the user
            flow_type: Type of onboarding flow (default: "user_onboarding")
            metadata: Optional metadata (source, referrer, etc.)
            
        Returns:
            UserOnboardingProgress instance tracking the user's progress
            
        Raises:
            ValueError: If the specified flow type doesn't exist
            
        Example:
            >>> progress = service.start_onboarding(
            ...     user_id="user-123",
            ...     flow_type="user_onboarding",
            ...     metadata={'source': 'website', 'referrer': 'google'}
            ... )
        """
        # Get the flow
        flow = self._flows.get(flow_type)
        if not flow:
            raise ValueError(f"Onboarding flow not found: {flow_type}")
        
        # Check if user already has an in-progress onboarding
        existing = self._get_user_active_progress(user_id, flow_type)
        if existing:
            logger.info(f"User {user_id} already has active onboarding: {existing.id}")
            return existing
        
        # Create progress record
        progress_id = str(uuid.uuid4())
        progress = UserOnboardingProgress(
            id=progress_id,
            user_id=user_id,
            flow_id=flow.id,
            state=OnboardingState.IN_PROGRESS,
            current_step_index=0,
            started_at=datetime.now(timezone.utc),
            metadata=metadata or {}
        )
        
        # Store progress
        self._progress_records[progress_id] = progress
        
        logger.info(f"Started onboarding for user {user_id}: {progress_id}")
        return progress
    
    def get_current_step(
        self,
        progress_id: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Optional[OnboardingStep]:
        """
        Get the current step for a user's onboarding progress.
        
        This method retrieves the current step the user is on,
        enriched with content from the CMS content manager.
        
        Args:
            progress_id: Progress record identifier
            user_context: Optional user context for content personalization
            
        Returns:
            OnboardingStep with CMS content, or None if not found
            
        Example:
            >>> step = service.get_current_step(
            ...     progress_id="progress-123",
            ...     user_context={'name': 'John', 'role': 'admin'}
            ... )
            >>> print(step.title)
            'Welcome to Orkinosai, John! 🚀'
        """
        progress = self._progress_records.get(progress_id)
        if not progress:
            logger.warning(f"Progress record not found: {progress_id}")
            return None
        
        flow = self._flows.get(progress.flow_id)
        if not flow:
            logger.error(f"Flow not found: {progress.flow_id}")
            return None
        
        if progress.current_step_index >= len(flow.steps):
            logger.warning(f"Current step index out of range: {progress.current_step_index}")
            return None
        
        # Get the step
        step = flow.steps[progress.current_step_index]
        
        # Enrich with CMS content
        content = self.content_manager.get_step_content(
            step.step_type,
            user_context=user_context
        )
        
        # Update step with CMS content
        step.title = content.get('title', step.title)
        step.description = content.get('description', step.description)
        step.content = content.get('content', {})
        step.cta_text = content.get('cta_text', step.cta_text)
        step.skip_text = content.get('skip_text', step.skip_text)
        
        return step
    
    def complete_step(
        self,
        progress_id: str,
        step_id: str,
        step_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Mark a step as completed and advance to the next step.
        
        This method handles step completion:
        1. Validates the step can be completed
        2. Stores any data collected during the step
        3. Marks the step as completed
        4. Advances to the next step
        5. Checks if onboarding is complete
        
        Args:
            progress_id: Progress record identifier
            step_id: Step identifier to complete
            step_data: Optional data collected during the step
            
        Returns:
            True if step was completed successfully, False otherwise
            
        Example:
            >>> service.complete_step(
            ...     progress_id="progress-123",
            ...     step_id="user_onboarding_profile",
            ...     step_data={'name': 'John', 'role': 'Developer'}
            ... )
            True
        """
        progress = self._progress_records.get(progress_id)
        if not progress:
            logger.error(f"Progress record not found: {progress_id}")
            return False
        
        flow = self._flows.get(progress.flow_id)
        if not flow:
            logger.error(f"Flow not found: {progress.flow_id}")
            return False
        
        # Find the step
        current_step = flow.steps[progress.current_step_index]
        if current_step.id != step_id:
            logger.error(f"Step mismatch: expected {current_step.id}, got {step_id}")
            return False
        
        # Store step data
        if step_data:
            progress.step_data[step_id] = step_data
        
        # Mark step as completed
        if step_id not in progress.completed_steps:
            progress.completed_steps.append(step_id)
        
        # Update timestamp
        progress.last_activity_at = datetime.now(timezone.utc)
        
        # Move to next step
        progress.current_step_index += 1
        
        # Check if onboarding is complete
        if progress.current_step_index >= len(flow.steps):
            progress.state = OnboardingState.COMPLETED
            progress.completed_at = datetime.now(timezone.utc)
            logger.info(f"Onboarding completed for user {progress.user_id}")
        
        logger.info(f"Completed step {step_id} for progress {progress_id}")
        return True
    
    def skip_step(
        self,
        progress_id: str,
        step_id: str
    ) -> bool:
        """
        Skip an optional step and move to the next step.
        
        This method allows users to skip non-required steps.
        
        Args:
            progress_id: Progress record identifier
            step_id: Step identifier to skip
            
        Returns:
            True if step was skipped successfully, False otherwise
        """
        progress = self._progress_records.get(progress_id)
        if not progress:
            logger.error(f"Progress record not found: {progress_id}")
            return False
        
        flow = self._flows.get(progress.flow_id)
        if not flow:
            logger.error(f"Flow not found: {progress.flow_id}")
            return False
        
        current_step = flow.steps[progress.current_step_index]
        if current_step.id != step_id:
            logger.error(f"Step mismatch: expected {current_step.id}, got {step_id}")
            return False
        
        # Check if step can be skipped
        if current_step.is_required:
            logger.warning(f"Cannot skip required step: {step_id}")
            return False
        
        # Move to next step without marking as completed
        progress.current_step_index += 1
        progress.last_activity_at = datetime.now(timezone.utc)
        
        # Check if onboarding is complete
        if progress.current_step_index >= len(flow.steps):
            progress.state = OnboardingState.COMPLETED
            progress.completed_at = datetime.now(timezone.utc)
        
        logger.info(f"Skipped step {step_id} for progress {progress_id}")
        return True
    
    def get_progress(self, progress_id: str) -> Optional[UserOnboardingProgress]:
        """
        Get onboarding progress by ID.
        
        Args:
            progress_id: Progress record identifier
            
        Returns:
            UserOnboardingProgress instance or None if not found
        """
        return self._progress_records.get(progress_id)
    
    def get_user_progress(
        self,
        user_id: str,
        flow_type: Optional[str] = None
    ) -> List[UserOnboardingProgress]:
        """
        Get all onboarding progress records for a user.
        
        Args:
            user_id: User identifier
            flow_type: Optional flow type filter
            
        Returns:
            List of UserOnboardingProgress instances
        """
        results = []
        for progress in self._progress_records.values():
            if progress.user_id == user_id:
                if flow_type is None or progress.flow_id == flow_type:
                    results.append(progress)
        return results
    
    def _get_user_active_progress(
        self,
        user_id: str,
        flow_type: str
    ) -> Optional[UserOnboardingProgress]:
        """
        Get active (in-progress) onboarding for a user.
        
        Args:
            user_id: User identifier
            flow_type: Flow type
            
        Returns:
            Active UserOnboardingProgress or None
        """
        for progress in self._progress_records.values():
            if (progress.user_id == user_id and
                progress.flow_id == flow_type and
                progress.state == OnboardingState.IN_PROGRESS):
                return progress
        return None
    
    def get_flow(self, flow_id: str) -> Optional[OnboardingFlow]:
        """
        Get an onboarding flow by ID.
        
        Args:
            flow_id: Flow identifier
            
        Returns:
            OnboardingFlow instance or None if not found
        """
        return self._flows.get(flow_id)
    
    def list_flows(self) -> List[OnboardingFlow]:
        """
        List all available onboarding flows.
        
        Returns:
            List of OnboardingFlow instances
        """
        return list(self._flows.values())
