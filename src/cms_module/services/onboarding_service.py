"""Onboarding service for user onboarding workflow"""

import logging
from datetime import datetime
from typing import Optional, Dict, Any
from ..models.onboarding import (
    OnboardingProgress,
    OnboardingStatus,
    OnboardingStep,
    OnboardingStepData,
    OnboardingResponse,
    UserProfile,
    UserPreferences
)
from ..db.user_db import get_user_database

logger = logging.getLogger(__name__)


class OnboardingService:
    """Service for managing user onboarding workflow"""
    
    def __init__(self):
        """Initialize onboarding service"""
        self.user_db = get_user_database()
        # In-memory storage for onboarding progress and profiles
        # In production, this would be in a database
        self._onboarding_progress: Dict[str, OnboardingProgress] = {}
        self._user_profiles: Dict[str, UserProfile] = {}
    
    def start_onboarding(self, user_id: str) -> OnboardingResponse:
        """
        Start onboarding for a user
        
        Args:
            user_id: User unique identifier
            
        Returns:
            OnboardingResponse with progress
        """
        try:
            # Check if user exists
            user = self.user_db.get_user_by_id(user_id)
            if not user:
                return OnboardingResponse(
                    success=False,
                    message="User not found",
                    progress=None,
                    profile=None
                )
            
            # Check if onboarding already started
            if user_id in self._onboarding_progress:
                progress = self._onboarding_progress[user_id]
                if progress.status == OnboardingStatus.COMPLETED:
                    return OnboardingResponse(
                        success=False,
                        message="Onboarding already completed",
                        progress=progress,
                        profile=self._user_profiles.get(user_id)
                    )
            
            # Create new onboarding progress
            progress = OnboardingProgress(
                user_id=user_id,
                current_step=OnboardingStep.WELCOME,
                completed_steps=[],
                status=OnboardingStatus.IN_PROGRESS,
                started_at=datetime.utcnow()
            )
            
            self._onboarding_progress[user_id] = progress
            
            logger.info(f"Onboarding started for user {user_id}")
            
            return OnboardingResponse(
                success=True,
                message="Onboarding started successfully",
                progress=progress,
                profile=self._user_profiles.get(user_id)
            )
            
        except Exception as e:
            logger.error(f"Error starting onboarding: {e}")
            return OnboardingResponse(
                success=False,
                message=f"Error starting onboarding: {str(e)}",
                progress=None,
                profile=None
            )
    
    def get_onboarding_progress(self, user_id: str) -> Optional[OnboardingProgress]:
        """
        Get onboarding progress for a user
        
        Args:
            user_id: User unique identifier
            
        Returns:
            OnboardingProgress if found, None otherwise
        """
        return self._onboarding_progress.get(user_id)
    
    def complete_step(self, user_id: str, step_data: OnboardingStepData) -> OnboardingResponse:
        """
        Complete an onboarding step
        
        Args:
            user_id: User unique identifier
            step_data: Step data including step type and collected data
            
        Returns:
            OnboardingResponse with updated progress
        """
        try:
            # Get onboarding progress
            progress = self._onboarding_progress.get(user_id)
            if not progress:
                return OnboardingResponse(
                    success=False,
                    message="Onboarding not started",
                    progress=None,
                    profile=None
                )
            
            # Validate current step
            if progress.current_step != step_data.step and step_data.step not in progress.completed_steps:
                return OnboardingResponse(
                    success=False,
                    message=f"Cannot complete step {step_data.step.value}. Current step is {progress.current_step.value}",
                    progress=progress,
                    profile=self._user_profiles.get(user_id)
                )
            
            # Store step data
            progress.data[step_data.step.value] = step_data.data
            
            # Handle specific steps
            if step_data.step == OnboardingStep.PROFILE_SETUP:
                self._handle_profile_setup(user_id, step_data.data)
            elif step_data.step == OnboardingStep.PREFERENCES:
                self._handle_preferences(user_id, step_data.data)
            
            # Complete the step
            progress.complete_step(step_data.step)
            
            # Update user onboarding_completed flag if all done
            if progress.status == OnboardingStatus.COMPLETED:
                self.user_db.update_user(user_id, {"onboarding_completed": True})
            
            logger.info(f"Step {step_data.step.value} completed for user {user_id}")
            
            return OnboardingResponse(
                success=True,
                message=f"Step {step_data.step.value} completed successfully",
                progress=progress,
                profile=self._user_profiles.get(user_id)
            )
            
        except Exception as e:
            logger.error(f"Error completing step: {e}")
            return OnboardingResponse(
                success=False,
                message=f"Error completing step: {str(e)}",
                progress=None,
                profile=None
            )
    
    def skip_onboarding(self, user_id: str) -> OnboardingResponse:
        """
        Skip onboarding for a user
        
        Args:
            user_id: User unique identifier
            
        Returns:
            OnboardingResponse with updated status
        """
        try:
            progress = self._onboarding_progress.get(user_id)
            if not progress:
                progress = OnboardingProgress(
                    user_id=user_id,
                    status=OnboardingStatus.SKIPPED
                )
                self._onboarding_progress[user_id] = progress
            else:
                progress.status = OnboardingStatus.SKIPPED
                progress.completed_at = datetime.utcnow()
            
            # Update user onboarding_completed flag
            self.user_db.update_user(user_id, {"onboarding_completed": True})
            
            logger.info(f"Onboarding skipped for user {user_id}")
            
            return OnboardingResponse(
                success=True,
                message="Onboarding skipped",
                progress=progress,
                profile=self._user_profiles.get(user_id)
            )
            
        except Exception as e:
            logger.error(f"Error skipping onboarding: {e}")
            return OnboardingResponse(
                success=False,
                message=f"Error skipping onboarding: {str(e)}",
                progress=None,
                profile=None
            )
    
    def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> OnboardingResponse:
        """
        Update user profile
        
        Args:
            user_id: User unique identifier
            profile_data: Profile data to update
            
        Returns:
            OnboardingResponse with updated profile
        """
        try:
            # Get or create profile
            profile = self._user_profiles.get(user_id)
            if not profile:
                profile = UserProfile(user_id=user_id)
                self._user_profiles[user_id] = profile
            
            # Update profile fields
            for key, value in profile_data.items():
                if key == 'preferences' and isinstance(value, dict):
                    # Handle preferences specially
                    profile.preferences = UserPreferences(**value)
                elif hasattr(profile, key):
                    setattr(profile, key, value)
            
            profile.updated_at = datetime.utcnow()
            
            logger.info(f"Profile updated for user {user_id}")
            
            return OnboardingResponse(
                success=True,
                message="Profile updated successfully",
                progress=self._onboarding_progress.get(user_id),
                profile=profile
            )
            
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            return OnboardingResponse(
                success=False,
                message=f"Error updating profile: {str(e)}",
                progress=None,
                profile=None
            )
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """
        Get user profile
        
        Args:
            user_id: User unique identifier
            
        Returns:
            UserProfile if found, None otherwise
        """
        return self._user_profiles.get(user_id)
    
    def _handle_profile_setup(self, user_id: str, data: Dict[str, Any]):
        """Handle profile setup step"""
        profile = self._user_profiles.get(user_id)
        if not profile:
            profile = UserProfile(user_id=user_id)
            self._user_profiles[user_id] = profile
        
        # Update profile with setup data
        if "job_title" in data:
            profile.job_title = data["job_title"]
        if "department" in data:
            profile.department = data["department"]
        if "bio" in data:
            profile.bio = data["bio"]
        
        profile.updated_at = datetime.utcnow()
    
    def _handle_preferences(self, user_id: str, data: Dict[str, Any]):
        """Handle preferences step"""
        profile = self._user_profiles.get(user_id)
        if not profile:
            profile = UserProfile(user_id=user_id)
            self._user_profiles[user_id] = profile
        
        # Update preferences
        preferences_data = {}
        for key in UserPreferences.model_fields.keys():
            if key in data:
                preferences_data[key] = data[key]
        
        if preferences_data:
            profile.preferences = UserPreferences(**preferences_data)
            profile.updated_at = datetime.utcnow()
