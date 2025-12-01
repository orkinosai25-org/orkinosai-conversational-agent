"""Onboarding service - To be copied from orkinosaicms"""

from ..base import ServiceResponse


class OnboardingService:
    """Onboarding workflow service - Placeholder"""
    
    def start_onboarding(self, user_id: str) -> ServiceResponse:
        """Start onboarding process"""
        raise NotImplementedError("To be implemented when copied from orkinosaicms")
    
    def complete_step(self, user_id: str, step_name: str) -> ServiceResponse:
        """Mark onboarding step as complete"""
        raise NotImplementedError("To be implemented when copied from orkinosaicms")
