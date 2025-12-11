"""
Onboarding Data Models

This module defines the data structures for the onboarding system.
These models represent the various states and configurations for
user onboarding flows in the CMS.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class OnboardingStepType(str, Enum):
    """
    Types of onboarding steps supported by the CMS.
    
    Each step type represents a different phase in the user journey:
    - WELCOME: Initial greeting and orientation
    - PROFILE: User profile setup and preferences
    - ORGANIZATION: Organization/workspace creation
    - PLAN_SELECTION: Subscription tier selection
    - PAYMENT: Payment method setup
    - THEME: Visual theme and branding
    - CONFIGURATION: System configuration and settings
    - TUTORIAL: Interactive tutorials and guides
    - COMPLETION: Final step with next actions
    """
    WELCOME = "welcome"
    PROFILE = "profile"
    ORGANIZATION = "organization"
    PLAN_SELECTION = "plan_selection"
    PAYMENT = "payment"
    THEME = "theme"
    CONFIGURATION = "configuration"
    TUTORIAL = "tutorial"
    COMPLETION = "completion"


class OnboardingState(str, Enum):
    """
    Current state of a user's onboarding process.
    
    States:
    - NOT_STARTED: User has not begun onboarding
    - IN_PROGRESS: User is actively going through onboarding
    - PAUSED: User has paused the onboarding process
    - COMPLETED: User has finished all onboarding steps
    - SKIPPED: User has opted to skip onboarding
    """
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class OnboardingStep(BaseModel):
    """
    Represents a single step in the onboarding flow.
    
    Each step contains:
    - Unique identifier
    - Step type and order
    - Content (title, description, CTA)
    - Configuration options
    - Validation rules
    - Skip capability
    
    The CMS content manager provides dynamic content for each step
    based on user context and preferences.
    """
    id: str = Field(..., description="Unique identifier for the step")
    step_type: OnboardingStepType = Field(..., description="Type of onboarding step")
    order: int = Field(..., description="Order in the flow (0-indexed)")
    title: str = Field(..., description="Step title displayed to user")
    description: str = Field(..., description="Detailed description of the step")
    content: Dict[str, Any] = Field(
        default_factory=dict,
        description="CMS-managed content for this step (HTML, markdown, etc.)"
    )
    is_required: bool = Field(
        default=True,
        description="Whether this step is required or can be skipped"
    )
    is_completed: bool = Field(
        default=False,
        description="Whether the user has completed this step"
    )
    configuration: Dict[str, Any] = Field(
        default_factory=dict,
        description="Step-specific configuration options"
    )
    validation_rules: Dict[str, Any] = Field(
        default_factory=dict,
        description="Validation rules for step completion"
    )
    cta_text: str = Field(
        default="Continue",
        description="Call-to-action button text"
    )
    skip_text: Optional[str] = Field(
        default=None,
        description="Text for skip button if step is optional"
    )


class OnboardingFlow(BaseModel):
    """
    Defines a complete onboarding flow with multiple steps.
    
    An onboarding flow is a sequence of steps that guides users
    through the initial setup process. The CMS allows for:
    - Multiple flow types (user, organization, admin)
    - Conditional steps based on user role or plan
    - Dynamic step ordering
    - Customizable content per step
    
    Example flows:
    - New user onboarding (Welcome → Profile → Tutorial)
    - Organization setup (Org details → Plan → Payment)
    - Feature onboarding (Introduction → Demo → Practice)
    """
    id: str = Field(..., description="Unique identifier for the flow")
    name: str = Field(..., description="Flow name (e.g., 'user_onboarding')")
    title: str = Field(..., description="Display title for the flow")
    description: str = Field(..., description="Description of the flow purpose")
    steps: List[OnboardingStep] = Field(
        default_factory=list,
        description="Ordered list of onboarding steps"
    )
    target_role: Optional[str] = Field(
        default=None,
        description="Target user role for this flow"
    )
    is_active: bool = Field(
        default=True,
        description="Whether this flow is currently active"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for the flow"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when flow was created"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when flow was last updated"
    )


class UserOnboardingProgress(BaseModel):
    """
    Tracks a user's progress through an onboarding flow.
    
    This model maintains state for each user going through onboarding:
    - Which flow they're in
    - Current step position
    - Completed steps
    - Collected data from each step
    - Overall completion status
    
    The CMS uses this to:
    - Resume interrupted onboarding sessions
    - Show progress indicators
    - Provide step navigation
    - Collect analytics on completion rates
    """
    id: str = Field(..., description="Unique identifier for this progress record")
    user_id: str = Field(..., description="User identifier")
    flow_id: str = Field(..., description="Onboarding flow identifier")
    state: OnboardingState = Field(
        default=OnboardingState.NOT_STARTED,
        description="Current state of onboarding"
    )
    current_step_index: int = Field(
        default=0,
        description="Index of the current step (0-indexed)"
    )
    completed_steps: List[str] = Field(
        default_factory=list,
        description="List of completed step IDs"
    )
    step_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Data collected from each step"
    )
    started_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when onboarding started"
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when onboarding completed"
    )
    last_activity_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp of last user activity"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (e.g., source, referrer)"
    )
    
    def get_progress_percentage(self, total_steps: int) -> float:
        """
        Calculate completion percentage.
        
        Args:
            total_steps: Total number of steps in the flow
            
        Returns:
            Percentage complete (0-100)
        """
        if total_steps == 0:
            return 0.0
        return (len(self.completed_steps) / total_steps) * 100
    
    def is_step_completed(self, step_id: str) -> bool:
        """
        Check if a specific step has been completed.
        
        Args:
            step_id: Step identifier to check
            
        Returns:
            True if step is completed, False otherwise
        """
        return step_id in self.completed_steps
