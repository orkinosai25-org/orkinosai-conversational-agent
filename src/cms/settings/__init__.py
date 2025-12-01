"""
Settings Management Module

Application-wide and user-specific settings.
Source: To be copied from orkinosaicms
"""

from .models import Setting
from .services import SettingsService

__all__ = ['Setting', 'SettingsService']
