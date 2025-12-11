"""
CMS Onboarding Module

This module provides onboarding integration with the OrkinosaiCMS system.
It manages user onboarding flows, welcome experiences, and configuration
workflows for new users and organizations.

Key Features:
- Multi-step onboarding wizard
- User welcome flows
- Content management for onboarding steps
- Progress tracking and state management
- Scalable configuration options

This module integrates with the CMS to provide:
- Dynamic content for each onboarding step
- User preference collection
- Organization setup
- Theme and branding configuration
"""

from .models import (
    OnboardingStep,
    OnboardingStepType,
    OnboardingState,
    OnboardingFlow,
    UserOnboardingProgress
)
from .service import OnboardingService
from .content_manager import OnboardingContentManager

__all__ = [
    'OnboardingStep',
    'OnboardingStepType',
    'OnboardingState',
    'OnboardingFlow',
    'UserOnboardingProgress',
    'OnboardingService',
    'OnboardingContentManager'
]
