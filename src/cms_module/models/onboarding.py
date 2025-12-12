"""Onboarding data models for user onboarding workflow"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class OnboardingStep(str, Enum):
    """Onboarding step types"""
    WELCOME = "welcome"
    PROFILE_SETUP = "profile_setup"
    ORGANIZATION_SETUP = "organization_setup"
    PREFERENCES = "preferences"
    TRAINING_INTRO = "training_intro"
    COMPLETE = "complete"


class OnboardingStatus(str, Enum):
    """Onboarding status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class UserPreferences(BaseModel):
    """User preferences model"""
    theme: str = Field(default="light", description="UI theme (light/dark)")
    language: str = Field(default="en", description="Preferred language")
    notifications_enabled: bool = Field(default=True, description="Enable notifications")
    email_notifications: bool = Field(default=True, description="Enable email notifications")
    chat_history_enabled: bool = Field(default=True, description="Save chat history")
    timezone: str = Field(default="UTC", description="User timezone")
    
    class Config:
        json_schema_extra = {
            "example": {
                "theme": "dark",
                "language": "en",
                "notifications_enabled": True,
                "email_notifications": True,
                "chat_history_enabled": True,
                "timezone": "America/New_York"
            }
        }


class UserProfile(BaseModel):
    """Extended user profile information"""
    user_id: str = Field(..., description="User ID")
    job_title: Optional[str] = Field(None, description="Job title")
    department: Optional[str] = Field(None, description="Department")
    bio: Optional[str] = Field(None, description="Short bio")
    avatar_url: Optional[str] = Field(None, description="Avatar image URL")
    preferences: UserPreferences = Field(default_factory=UserPreferences, description="User preferences")
    custom_fields: Dict[str, Any] = Field(default_factory=dict, description="Custom profile fields")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123abc",
                "job_title": "Product Manager",
                "department": "Product",
                "bio": "Passionate about building great products",
                "preferences": {
                    "theme": "dark",
                    "language": "en"
                }
            }
        }


class OnboardingProgress(BaseModel):
    """User onboarding progress tracking"""
    user_id: str = Field(..., description="User ID")
    current_step: OnboardingStep = Field(default=OnboardingStep.WELCOME, description="Current onboarding step")
    completed_steps: List[OnboardingStep] = Field(default_factory=list, description="Completed steps")
    status: OnboardingStatus = Field(default=OnboardingStatus.NOT_STARTED, description="Overall status")
    started_at: Optional[datetime] = Field(None, description="When onboarding was started")
    completed_at: Optional[datetime] = Field(None, description="When onboarding was completed")
    data: Dict[str, Any] = Field(default_factory=dict, description="Onboarding data collected")
    
    def is_step_completed(self, step: OnboardingStep) -> bool:
        """Check if a step is completed"""
        return step in self.completed_steps
    
    def complete_step(self, step: OnboardingStep):
        """Mark a step as completed"""
        if step not in self.completed_steps:
            self.completed_steps.append(step)
        
        # Update current step to next step
        steps_order = list(OnboardingStep)
        current_index = steps_order.index(step)
        if current_index < len(steps_order) - 1:
            self.current_step = steps_order[current_index + 1]
        
        # Check if all steps are completed
        if len(self.completed_steps) == len(OnboardingStep) - 1:  # -1 for COMPLETE
            self.status = OnboardingStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            self.current_step = OnboardingStep.COMPLETE


class OnboardingStepData(BaseModel):
    """Data for completing an onboarding step"""
    step: OnboardingStep = Field(..., description="Step to complete")
    data: Dict[str, Any] = Field(default_factory=dict, description="Step data")


class OnboardingResponse(BaseModel):
    """Response for onboarding operations"""
    success: bool = Field(..., description="Operation success status")
    message: str = Field(..., description="Response message")
    progress: Optional[OnboardingProgress] = Field(None, description="Onboarding progress")
    profile: Optional[UserProfile] = Field(None, description="User profile")
