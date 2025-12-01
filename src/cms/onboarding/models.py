"""Onboarding models - To be copied from orkinosaicms"""

from typing import Optional
from ..base import BaseEntity


class OnboardingStep(BaseEntity):
    """Onboarding step tracking"""
    user_id: str
    organization_id: Optional[str] = None
    step_name: str
    step_order: int
    completed: bool = False
    skipped: bool = False
