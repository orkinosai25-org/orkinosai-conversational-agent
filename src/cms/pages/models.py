"""
SharePoint-inspired CMS Models

This module implements a flexible, SharePoint-style content management system with:
- Master Pages: Define overall site structure and chrome
- Page Layouts: Templates that use master pages and define content zones
- Pages: Actual content pages that use layouts
- Content Zones: Modular content areas within pages
- Widgets: Reusable content components
- Multi-tenant support for design agencies
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import Field, field_validator
from src.cms.base import BaseEntity


class PageType(str, Enum):
    """Types of pages in the CMS"""
    SYSTEM = "system"  # System pages (login, error pages)
    APPLICATION = "application"  # Application-specific pages
    CONTENT = "content"  # Regular content pages
    LANDING = "landing"  # Landing pages


class PageStatus(str, Enum):
    """Publication status of pages"""
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    SCHEDULED = "scheduled"


class ContentZoneType(str, Enum):
    """Types of content zones"""
    HEADER = "header"
    FOOTER = "footer"
    SIDEBAR = "sidebar"
    MAIN = "main"
    CUSTOM = "custom"


class WidgetType(str, Enum):
    """Types of widgets available"""
    TEXT = "text"
    HTML = "html"
    IMAGE = "image"
    VIDEO = "video"
    FORM = "form"
    NAVIGATION = "navigation"
    SEARCH = "search"
    CUSTOM = "custom"


class MasterPage(BaseEntity):
    """
    Master Page - Defines the overall structure and chrome of the site
    
    Similar to SharePoint master pages, these define:
    - Site header and navigation
    - Footer
    - Overall layout structure
    - CSS/JS references
    - Content placeholders
    """
    name: str = Field(..., description="Unique name for the master page")
    title: str = Field(..., description="Display title")
    description: Optional[str] = Field(None, description="Description of the master page")
    
    # Multi-tenant support
    organization_id: Optional[str] = Field(None, description="Organization that owns this master page")
    is_global: bool = Field(False, description="Available to all organizations")
    
    # Template structure
    html_template: str = Field(..., description="HTML template with placeholders")
    css_references: List[str] = Field(default_factory=list, description="CSS file references")
    js_references: List[str] = Field(default_factory=list, description="JavaScript file references")
    
    # Content placeholders
    content_placeholders: List[str] = Field(
        default_factory=list,
        description="Names of content placeholders in the template"
    )
    
    # Metadata
    is_default: bool = Field(False, description="Default master page for new pages")
    sort_order: int = Field(0, description="Sort order in listings")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Master page name cannot be empty")
        return v.strip()


class PageLayout(BaseEntity):
    """
    Page Layout - Defines content structure within a master page
    
    Layouts specify:
    - Which master page to use
    - Content zones and their arrangement
    - Available widget types per zone
    - Field definitions for structured content
    """
    name: str = Field(..., description="Unique name for the layout")
    title: str = Field(..., description="Display title")
    description: Optional[str] = Field(None, description="Description of the layout")
    
    # Multi-tenant support
    organization_id: Optional[str] = Field(None, description="Organization that owns this layout")
    is_global: bool = Field(False, description="Available to all organizations")
    
    # Master page association
    master_page_id: str = Field(..., description="Associated master page ID")
    
    # Layout structure
    layout_template: str = Field(..., description="HTML template for the layout")
    content_zones: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Content zones configuration"
    )
    
    # Field definitions for structured content
    fields: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Custom field definitions for this layout"
    )
    
    # Page type compatibility
    page_types: List[PageType] = Field(
        default_factory=lambda: [PageType.CONTENT],
        description="Compatible page types"
    )
    
    # Metadata
    thumbnail_url: Optional[str] = Field(None, description="Preview thumbnail")
    is_default: bool = Field(False, description="Default layout for page type")
    sort_order: int = Field(0, description="Sort order in listings")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Layout name cannot be empty")
        return v.strip()


class Page(BaseEntity):
    """
    Page - Actual content page using a layout
    
    Pages are the actual content that users see, combining:
    - Page layout structure
    - Content zone data
    - Custom field values
    - Publication settings
    """
    title: str = Field(..., description="Page title")
    slug: str = Field(..., description="URL-friendly slug")
    description: Optional[str] = Field(None, description="Page description/excerpt")
    
    # Multi-tenant support
    organization_id: Optional[str] = Field(None, description="Organization that owns this page")
    
    # Layout association
    page_layout_id: str = Field(..., description="Associated page layout ID")
    
    # Page type and status
    page_type: PageType = Field(PageType.CONTENT, description="Type of page")
    status: PageStatus = Field(PageStatus.DRAFT, description="Publication status")
    
    # Publishing
    published_at: Optional[datetime] = Field(None, description="Publication timestamp")
    scheduled_publish_at: Optional[datetime] = Field(None, description="Scheduled publication time")
    author_id: Optional[str] = Field(None, description="Page author ID")
    
    # SEO
    meta_title: Optional[str] = Field(None, description="SEO meta title")
    meta_description: Optional[str] = Field(None, description="SEO meta description")
    meta_keywords: List[str] = Field(default_factory=list, description="SEO keywords")
    
    # Content
    content_zones_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Content data for each zone"
    )
    field_values: Dict[str, Any] = Field(
        default_factory=dict,
        description="Custom field values"
    )
    
    # Navigation
    parent_page_id: Optional[str] = Field(None, description="Parent page for hierarchy")
    menu_title: Optional[str] = Field(None, description="Title in navigation menus")
    include_in_menu: bool = Field(True, description="Include in navigation")
    sort_order: int = Field(0, description="Sort order in navigation")
    
    # Access control
    is_public: bool = Field(True, description="Publicly accessible")
    required_roles: List[str] = Field(
        default_factory=list,
        description="Required roles to access"
    )
    
    # Version control
    version: int = Field(1, description="Version number")
    parent_version_id: Optional[str] = Field(None, description="Previous version ID")
    
    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Page slug cannot be empty")
        # Basic slug validation
        import re
        if not re.match(r'^[a-z0-9\-]+$', v):
            raise ValueError("Slug must contain only lowercase letters, numbers, and hyphens")
        return v.strip()


class ContentZone(BaseEntity):
    """
    Content Zone - Modular content area within a page
    
    Zones are placeholders for widgets and content blocks
    """
    name: str = Field(..., description="Zone identifier")
    title: str = Field(..., description="Display title")
    
    # Zone configuration
    zone_type: ContentZoneType = Field(ContentZoneType.CUSTOM, description="Type of zone")
    page_layout_id: str = Field(..., description="Associated page layout ID")
    
    # Layout
    position: int = Field(0, description="Position within layout")
    width: Optional[str] = Field(None, description="Width specification (e.g., '100%', '300px')")
    height: Optional[str] = Field(None, description="Height specification")
    css_classes: List[str] = Field(default_factory=list, description="CSS classes")
    
    # Constraints
    max_widgets: Optional[int] = Field(None, description="Maximum number of widgets")
    allowed_widget_types: List[WidgetType] = Field(
        default_factory=list,
        description="Allowed widget types (empty = all)"
    )
    
    # Behavior
    is_required: bool = Field(False, description="Must have at least one widget")
    is_locked: bool = Field(False, description="Cannot be edited by content editors")


class Widget(BaseEntity):
    """
    Widget - Reusable content component
    
    Widgets are the actual content blocks placed in zones
    """
    title: str = Field(..., description="Widget title")
    widget_type: WidgetType = Field(..., description="Type of widget")
    
    # Placement
    page_id: str = Field(..., description="Page this widget belongs to")
    zone_id: str = Field(..., description="Zone this widget is placed in")
    position: int = Field(0, description="Position within zone")
    
    # Content
    content: Dict[str, Any] = Field(
        default_factory=dict,
        description="Widget content data"
    )
    
    # Configuration
    settings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Widget-specific settings"
    )
    
    # Display
    css_classes: List[str] = Field(default_factory=list, description="CSS classes")
    is_visible: bool = Field(True, description="Widget visibility")
    
    # Access control
    required_roles: List[str] = Field(
        default_factory=list,
        description="Required roles to view"
    )


class WidgetTemplate(BaseEntity):
    """
    Widget Template - Reusable widget configuration
    
    Templates define pre-configured widgets that can be instantiated
    """
    name: str = Field(..., description="Template name")
    title: str = Field(..., description="Display title")
    description: Optional[str] = Field(None, description="Template description")
    
    # Multi-tenant support
    organization_id: Optional[str] = Field(None, description="Organization that owns this template")
    is_global: bool = Field(False, description="Available to all organizations")
    
    # Template configuration
    widget_type: WidgetType = Field(..., description="Type of widget")
    default_content: Dict[str, Any] = Field(
        default_factory=dict,
        description="Default content structure"
    )
    default_settings: Dict[str, Any] = Field(
        default_factory=dict,
        description="Default settings"
    )
    
    # Schema
    content_schema: Dict[str, Any] = Field(
        default_factory=dict,
        description="JSON schema for content validation"
    )
    settings_schema: Dict[str, Any] = Field(
        default_factory=dict,
        description="JSON schema for settings validation"
    )
    
    # Metadata
    thumbnail_url: Optional[str] = Field(None, description="Preview thumbnail")
    category: Optional[str] = Field(None, description="Widget category")
    tags: List[str] = Field(default_factory=list, description="Search tags")


class PageVersion(BaseEntity):
    """
    Page Version - Historical version of a page
    
    Maintains version history for pages
    """
    page_id: str = Field(..., description="Original page ID")
    version_number: int = Field(..., description="Version number")
    
    # Snapshot of page data
    title: str = Field(..., description="Page title at this version")
    content_zones_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Content data snapshot"
    )
    field_values: Dict[str, Any] = Field(
        default_factory=dict,
        description="Field values snapshot"
    )
    
    # Version metadata
    change_summary: Optional[str] = Field(None, description="Summary of changes")
    changed_by: Optional[str] = Field(None, description="User who made changes")
    is_major_version: bool = Field(False, description="Major version flag")
