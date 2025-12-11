"""
Onboarding Content Manager

This module manages dynamic content for onboarding flows using CMS features.
It provides content retrieval, customization, and localization for each
onboarding step.

The content manager integrates with the CMS to:
- Load step content from configuration
- Apply user-specific customizations
- Support multiple languages
- Track content versions
- Enable A/B testing
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from .models import OnboardingStep, OnboardingStepType

logger = logging.getLogger(__name__)


class OnboardingContentManager:
    """
    Manages content for onboarding steps using CMS features.
    
    This class provides centralized content management for the onboarding
    system, allowing content to be:
    - Configured dynamically without code changes
    - Personalized based on user context
    - Localized for different languages
    - Version controlled for A/B testing
    
    Usage:
        content_manager = OnboardingContentManager()
        content = content_manager.get_step_content(
            step_type=OnboardingStepType.WELCOME,
            user_context={'name': 'John', 'role': 'admin'}
        )
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the content manager with optional configuration.
        
        Args:
            config: Optional configuration dictionary with content settings
        """
        self.config = config or {}
        self._content_cache: Dict[str, Dict[str, Any]] = {}
        self._load_default_content()
    
    def _load_default_content(self):
        """
        Load default content templates for all onboarding steps.
        
        This method initializes the content cache with default content
        for each step type. In a production system, this would load
        from a database or external CMS API.
        """
        # Default content for WELCOME step
        self._content_cache[OnboardingStepType.WELCOME] = {
            'title': 'Welcome to Orkinosai! 🚀',
            'description': 'Let\'s get you set up in just a few minutes.',
            'content': {
                'hero_text': 'Welcome to the future of conversational AI',
                'subtitle': 'We\'re excited to help you build amazing experiences',
                'features': [
                    'AI-powered conversations',
                    'Easy integration',
                    'Scalable infrastructure'
                ],
                'video_url': None,
                'image_url': '/static/images/welcome-hero.png'
            },
            'cta_text': 'Get Started',
            'skip_text': None
        }
        
        # Default content for PROFILE step
        self._content_cache[OnboardingStepType.PROFILE] = {
            'title': 'Tell Us About Yourself',
            'description': 'Help us personalize your experience',
            'content': {
                'fields': [
                    {
                        'id': 'full_name',
                        'label': 'Full Name',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'John Doe'
                    },
                    {
                        'id': 'role',
                        'label': 'Your Role',
                        'type': 'select',
                        'required': True,
                        'options': [
                            'Developer',
                            'Product Manager',
                            'Business Owner',
                            'Other'
                        ]
                    },
                    {
                        'id': 'company',
                        'label': 'Company Name',
                        'type': 'text',
                        'required': False,
                        'placeholder': 'Acme Inc.'
                    }
                ]
            },
            'cta_text': 'Continue',
            'skip_text': 'Skip for now'
        }
        
        # Default content for ORGANIZATION step
        self._content_cache[OnboardingStepType.ORGANIZATION] = {
            'title': 'Create Your Workspace',
            'description': 'Set up your organization and invite team members',
            'content': {
                'fields': [
                    {
                        'id': 'org_name',
                        'label': 'Organization Name',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'My Organization'
                    },
                    {
                        'id': 'org_url',
                        'label': 'Workspace URL',
                        'type': 'text',
                        'required': True,
                        'placeholder': 'my-org',
                        'help_text': 'This will be your workspace identifier'
                    }
                ],
                'help_text': 'You can invite team members after setup'
            },
            'cta_text': 'Create Workspace',
            'skip_text': None
        }
        
        # Default content for PLAN_SELECTION step
        self._content_cache[OnboardingStepType.PLAN_SELECTION] = {
            'title': 'Choose Your Plan',
            'description': 'Select the plan that best fits your needs',
            'content': {
                'plans': [
                    {
                        'id': 'free',
                        'name': 'Free',
                        'price': 0,
                        'period': 'month',
                        'features': [
                            '1 workspace',
                            'Basic features',
                            'Community support'
                        ],
                        'recommended': False
                    },
                    {
                        'id': 'starter',
                        'name': 'Starter',
                        'price': 12,
                        'period': 'month',
                        'features': [
                            '3 workspaces',
                            'No ads',
                            'Email support'
                        ],
                        'recommended': True
                    },
                    {
                        'id': 'pro',
                        'name': 'Pro',
                        'price': 35,
                        'period': 'month',
                        'features': [
                            '10 workspaces',
                            'Advanced analytics',
                            'Priority support'
                        ],
                        'recommended': False
                    }
                ]
            },
            'cta_text': 'Select Plan',
            'skip_text': 'Start with Free'
        }
        
        # Default content for THEME step
        self._content_cache[OnboardingStepType.THEME] = {
            'title': 'Choose Your Theme',
            'description': 'Customize the look and feel',
            'content': {
                'themes': [
                    {
                        'id': 'azure',
                        'name': 'Azure',
                        'preview_url': '/static/images/theme-azure.png',
                        'primary_color': '#0078D4'
                    },
                    {
                        'id': 'dark',
                        'name': 'Dark Mode',
                        'preview_url': '/static/images/theme-dark.png',
                        'primary_color': '#1a1a1a'
                    },
                    {
                        'id': 'light',
                        'name': 'Light',
                        'preview_url': '/static/images/theme-light.png',
                        'primary_color': '#ffffff'
                    }
                ]
            },
            'cta_text': 'Apply Theme',
            'skip_text': 'Use default'
        }
        
        # Default content for COMPLETION step
        self._content_cache[OnboardingStepType.COMPLETION] = {
            'title': 'You\'re All Set! 🎉',
            'description': 'Your workspace is ready to go',
            'content': {
                'success_message': 'Congratulations! Your setup is complete.',
                'next_steps': [
                    {
                        'title': 'Explore the Dashboard',
                        'description': 'Get familiar with your new workspace',
                        'action_url': '/dashboard',
                        'action_text': 'Go to Dashboard'
                    },
                    {
                        'title': 'Invite Team Members',
                        'description': 'Collaborate with your team',
                        'action_url': '/settings/team',
                        'action_text': 'Invite Team'
                    },
                    {
                        'title': 'Read Documentation',
                        'description': 'Learn about advanced features',
                        'action_url': '/docs',
                        'action_text': 'View Docs'
                    }
                ]
            },
            'cta_text': 'Get Started',
            'skip_text': None
        }
    
    def get_step_content(
        self,
        step_type: OnboardingStepType,
        user_context: Optional[Dict[str, Any]] = None,
        locale: str = 'en'
    ) -> Dict[str, Any]:
        """
        Get content for a specific onboarding step.
        
        This method retrieves and customizes content for an onboarding step
        based on the step type and user context. Content can be personalized
        using template variables from the user context.
        
        Args:
            step_type: Type of onboarding step
            user_context: Optional user context for personalization (name, role, etc.)
            locale: Language locale for localization (default: 'en')
            
        Returns:
            Dictionary containing step content with personalization applied
            
        Example:
            >>> content = manager.get_step_content(
            ...     OnboardingStepType.WELCOME,
            ...     {'name': 'John', 'role': 'admin'}
            ... )
            >>> print(content['title'])
            'Welcome to Orkinosai, John! 🚀'
        """
        user_context = user_context or {}
        
        # Get base content from cache
        base_content = self._content_cache.get(step_type, {}).copy()
        
        if not base_content:
            logger.warning(f"No content found for step type: {step_type}")
            return self._get_fallback_content(step_type)
        
        # Apply personalization if user context provided
        if user_context.get('name'):
            # Personalize title with user name for WELCOME step
            if step_type == OnboardingStepType.WELCOME:
                base_content['title'] = f"Welcome to Orkinosai, {user_context['name']}! 🚀"
        
        # Apply locale-specific content (for future localization support)
        # In production, this would load translations from a database or i18n files
        
        return base_content
    
    def _get_fallback_content(self, step_type: OnboardingStepType) -> Dict[str, Any]:
        """
        Get fallback content when primary content is unavailable.
        
        Args:
            step_type: Type of onboarding step
            
        Returns:
            Basic fallback content dictionary
        """
        return {
            'title': f'Step: {step_type.value}',
            'description': 'Complete this step to continue',
            'content': {},
            'cta_text': 'Continue',
            'skip_text': None
        }
    
    def update_content(
        self,
        step_type: OnboardingStepType,
        content: Dict[str, Any]
    ):
        """
        Update content for a specific step type.
        
        This method allows dynamic content updates without code changes.
        In production, this would persist changes to a database.
        
        Args:
            step_type: Type of onboarding step
            content: New content dictionary
        """
        self._content_cache[step_type] = content
        logger.info(f"Updated content for step type: {step_type}")
    
    def get_all_content(self) -> Dict[OnboardingStepType, Dict[str, Any]]:
        """
        Get all content for all step types.
        
        Returns:
            Dictionary mapping step types to their content
        """
        return self._content_cache.copy()
