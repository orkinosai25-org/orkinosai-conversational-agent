"""
CMS Pages Module

SharePoint-inspired content management system with master pages,
page layouts, flexible content zones, and modular widgets.
"""

from src.cms.pages.models import (
    PageType,
    PageStatus,
    ContentZoneType,
    WidgetType,
    MasterPage,
    PageLayout,
    Page,
    ContentZone,
    Widget,
    WidgetTemplate,
    PageVersion
)

from src.cms.pages.services import (
    MasterPageService,
    PageLayoutService,
    PageService,
    WidgetService
)

__all__ = [
    # Enums
    'PageType',
    'PageStatus',
    'ContentZoneType',
    'WidgetType',
    # Models
    'MasterPage',
    'PageLayout',
    'Page',
    'ContentZone',
    'Widget',
    'WidgetTemplate',
    'PageVersion',
    # Services
    'MasterPageService',
    'PageLayoutService',
    'PageService',
    'WidgetService'
]
