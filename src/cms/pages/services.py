"""
SharePoint-inspired CMS Services

Service layer for CMS operations including:
- Master page management
- Page layout management
- Page creation and publishing
- Content zone management
- Widget management
"""

from typing import List, Optional, Dict, Any
from uuid import uuid4
from datetime import datetime

from src.cms.base import ServiceResponse, NotFoundException, ValidationException, DuplicateException
from src.cms.pages.models import (
    MasterPage, PageLayout, Page, ContentZone, Widget, WidgetTemplate, PageVersion,
    PageType, PageStatus, ContentZoneType, WidgetType
)


class MasterPageService:
    """Service for managing master pages"""
    
    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would use a database
        self._storage: Dict[str, MasterPage] = {}
    
    def create_master_page(
        self,
        name: str,
        title: str,
        html_template: str,
        description: Optional[str] = None,
        organization_id: Optional[str] = None,
        is_global: bool = False,
        css_references: Optional[List[str]] = None,
        js_references: Optional[List[str]] = None,
        content_placeholders: Optional[List[str]] = None,
        created_by: Optional[str] = None
    ) -> ServiceResponse:
        """Create a new master page"""
        try:
            # Check for duplicate name
            if any(mp.name == name for mp in self._storage.values()):
                raise DuplicateException(f"Master page with name '{name}' already exists")
            
            master_page = MasterPage(
                id=str(uuid4()),
                name=name,
                title=title,
                description=description,
                organization_id=organization_id,
                is_global=is_global,
                html_template=html_template,
                css_references=css_references or [],
                js_references=js_references or [],
                content_placeholders=content_placeholders or [],
                created_by=created_by
            )
            
            self._storage[master_page.id] = master_page
            
            return ServiceResponse.success_response(
                "Master page created successfully",
                data=master_page.model_dump()
            )
        except (ValidationException, DuplicateException) as e:
            return ServiceResponse.error_response(str(e), errors=[str(e)])
        except Exception as e:
            return ServiceResponse.error_response("Failed to create master page", errors=[str(e)])
    
    def get_master_page(self, master_page_id: str) -> ServiceResponse:
        """Get a master page by ID"""
        master_page = self._storage.get(master_page_id)
        if not master_page:
            return ServiceResponse.error_response(
                f"Master page not found: {master_page_id}",
                errors=["Master page not found"]
            )
        
        return ServiceResponse.success_response(
            "Master page retrieved",
            data=master_page.model_dump()
        )
    
    def list_master_pages(
        self,
        organization_id: Optional[str] = None,
        include_global: bool = True
    ) -> ServiceResponse:
        """List all master pages"""
        pages = []
        for mp in self._storage.values():
            if organization_id:
                if mp.organization_id == organization_id or (include_global and mp.is_global):
                    pages.append(mp.model_dump())
            else:
                pages.append(mp.model_dump())
        
        return ServiceResponse.success_response(
            f"Found {len(pages)} master page(s)",
            data={"master_pages": pages}
        )
    
    def update_master_page(
        self,
        master_page_id: str,
        **updates
    ) -> ServiceResponse:
        """Update a master page"""
        master_page = self._storage.get(master_page_id)
        if not master_page:
            return ServiceResponse.error_response(
                f"Master page not found: {master_page_id}",
                errors=["Master page not found"]
            )
        
        try:
            for key, value in updates.items():
                if hasattr(master_page, key):
                    setattr(master_page, key, value)
            
            return ServiceResponse.success_response(
                "Master page updated successfully",
                data=master_page.model_dump()
            )
        except Exception as e:
            return ServiceResponse.error_response("Failed to update master page", errors=[str(e)])
    
    def delete_master_page(self, master_page_id: str) -> ServiceResponse:
        """Delete a master page"""
        if master_page_id not in self._storage:
            return ServiceResponse.error_response(
                f"Master page not found: {master_page_id}",
                errors=["Master page not found"]
            )
        
        del self._storage[master_page_id]
        return ServiceResponse.success_response("Master page deleted successfully")


class PageLayoutService:
    """Service for managing page layouts"""
    
    def __init__(self):
        self._storage: Dict[str, PageLayout] = {}
    
    def create_layout(
        self,
        name: str,
        title: str,
        master_page_id: str,
        layout_template: str,
        description: Optional[str] = None,
        organization_id: Optional[str] = None,
        is_global: bool = False,
        content_zones: Optional[List[Dict[str, Any]]] = None,
        fields: Optional[List[Dict[str, Any]]] = None,
        page_types: Optional[List[PageType]] = None,
        created_by: Optional[str] = None
    ) -> ServiceResponse:
        """Create a new page layout"""
        try:
            # Check for duplicate name
            if any(layout.name == name for layout in self._storage.values()):
                raise DuplicateException(f"Page layout with name '{name}' already exists")
            
            layout = PageLayout(
                id=str(uuid4()),
                name=name,
                title=title,
                description=description,
                organization_id=organization_id,
                is_global=is_global,
                master_page_id=master_page_id,
                layout_template=layout_template,
                content_zones=content_zones or [],
                fields=fields or [],
                page_types=page_types or [PageType.CONTENT],
                created_by=created_by
            )
            
            self._storage[layout.id] = layout
            
            return ServiceResponse.success_response(
                "Page layout created successfully",
                data=layout.model_dump()
            )
        except (ValidationException, DuplicateException) as e:
            return ServiceResponse.error_response(str(e), errors=[str(e)])
        except Exception as e:
            return ServiceResponse.error_response("Failed to create page layout", errors=[str(e)])
    
    def get_layout(self, layout_id: str) -> ServiceResponse:
        """Get a page layout by ID"""
        layout = self._storage.get(layout_id)
        if not layout:
            return ServiceResponse.error_response(
                f"Page layout not found: {layout_id}",
                errors=["Page layout not found"]
            )
        
        return ServiceResponse.success_response(
            "Page layout retrieved",
            data=layout.model_dump()
        )
    
    def list_layouts(
        self,
        organization_id: Optional[str] = None,
        master_page_id: Optional[str] = None,
        page_type: Optional[PageType] = None,
        include_global: bool = True
    ) -> ServiceResponse:
        """List page layouts with optional filters"""
        layouts = []
        for layout in self._storage.values():
            # Organization filter
            if organization_id:
                if not (layout.organization_id == organization_id or (include_global and layout.is_global)):
                    continue
            
            # Master page filter
            if master_page_id and layout.master_page_id != master_page_id:
                continue
            
            # Page type filter
            if page_type and page_type not in layout.page_types:
                continue
            
            layouts.append(layout.model_dump())
        
        return ServiceResponse.success_response(
            f"Found {len(layouts)} layout(s)",
            data={"layouts": layouts}
        )
    
    def update_layout(self, layout_id: str, **updates) -> ServiceResponse:
        """Update a page layout"""
        layout = self._storage.get(layout_id)
        if not layout:
            return ServiceResponse.error_response(
                f"Page layout not found: {layout_id}",
                errors=["Page layout not found"]
            )
        
        try:
            for key, value in updates.items():
                if hasattr(layout, key):
                    setattr(layout, key, value)
            
            return ServiceResponse.success_response(
                "Page layout updated successfully",
                data=layout.model_dump()
            )
        except Exception as e:
            return ServiceResponse.error_response("Failed to update page layout", errors=[str(e)])
    
    def delete_layout(self, layout_id: str) -> ServiceResponse:
        """Delete a page layout"""
        if layout_id not in self._storage:
            return ServiceResponse.error_response(
                f"Page layout not found: {layout_id}",
                errors=["Page layout not found"]
            )
        
        del self._storage[layout_id]
        return ServiceResponse.success_response("Page layout deleted successfully")


class PageService:
    """Service for managing pages"""
    
    def __init__(self):
        self._storage: Dict[str, Page] = {}
        self._versions: Dict[str, List[PageVersion]] = {}
    
    def create_page(
        self,
        title: str,
        slug: str,
        page_layout_id: str,
        organization_id: Optional[str] = None,
        page_type: PageType = PageType.CONTENT,
        description: Optional[str] = None,
        author_id: Optional[str] = None,
        created_by: Optional[str] = None
    ) -> ServiceResponse:
        """Create a new page"""
        try:
            # Check for duplicate slug within organization
            if any(
                p.slug == slug and p.organization_id == organization_id
                for p in self._storage.values()
            ):
                raise DuplicateException(f"Page with slug '{slug}' already exists in this organization")
            
            page = Page(
                id=str(uuid4()),
                title=title,
                slug=slug,
                description=description,
                organization_id=organization_id,
                page_layout_id=page_layout_id,
                page_type=page_type,
                status=PageStatus.DRAFT,
                author_id=author_id,
                created_by=created_by
            )
            
            self._storage[page.id] = page
            
            return ServiceResponse.success_response(
                "Page created successfully",
                data=page.model_dump()
            )
        except (ValidationException, DuplicateException) as e:
            return ServiceResponse.error_response(str(e), errors=[str(e)])
        except Exception as e:
            return ServiceResponse.error_response("Failed to create page", errors=[str(e)])
    
    def get_page(self, page_id: str) -> ServiceResponse:
        """Get a page by ID"""
        page = self._storage.get(page_id)
        if not page:
            return ServiceResponse.error_response(
                f"Page not found: {page_id}",
                errors=["Page not found"]
            )
        
        return ServiceResponse.success_response(
            "Page retrieved",
            data=page.model_dump()
        )
    
    def get_page_by_slug(self, slug: str, organization_id: Optional[str] = None) -> ServiceResponse:
        """Get a page by slug"""
        for page in self._storage.values():
            if page.slug == slug and page.organization_id == organization_id:
                return ServiceResponse.success_response(
                    "Page retrieved",
                    data=page.model_dump()
                )
        
        return ServiceResponse.error_response(
            f"Page not found with slug: {slug}",
            errors=["Page not found"]
        )
    
    def list_pages(
        self,
        organization_id: Optional[str] = None,
        page_type: Optional[PageType] = None,
        status: Optional[PageStatus] = None,
        parent_page_id: Optional[str] = None
    ) -> ServiceResponse:
        """List pages with optional filters"""
        pages = []
        for page in self._storage.values():
            if organization_id and page.organization_id != organization_id:
                continue
            if page_type and page.page_type != page_type:
                continue
            if status and page.status != status:
                continue
            if parent_page_id is not None and page.parent_page_id != parent_page_id:
                continue
            
            pages.append(page.model_dump())
        
        return ServiceResponse.success_response(
            f"Found {len(pages)} page(s)",
            data={"pages": pages}
        )
    
    def update_page(self, page_id: str, **updates) -> ServiceResponse:
        """Update a page"""
        page = self._storage.get(page_id)
        if not page:
            return ServiceResponse.error_response(
                f"Page not found: {page_id}",
                errors=["Page not found"]
            )
        
        try:
            for key, value in updates.items():
                if hasattr(page, key):
                    setattr(page, key, value)
            
            return ServiceResponse.success_response(
                "Page updated successfully",
                data=page.model_dump()
            )
        except Exception as e:
            return ServiceResponse.error_response("Failed to update page", errors=[str(e)])
    
    def publish_page(self, page_id: str, published_by: Optional[str] = None) -> ServiceResponse:
        """Publish a page"""
        page = self._storage.get(page_id)
        if not page:
            return ServiceResponse.error_response(
                f"Page not found: {page_id}",
                errors=["Page not found"]
            )
        
        page.status = PageStatus.PUBLISHED
        page.published_at = datetime.now()
        page.updated_by = published_by
        
        return ServiceResponse.success_response(
            "Page published successfully",
            data=page.model_dump()
        )
    
    def delete_page(self, page_id: str) -> ServiceResponse:
        """Delete a page"""
        if page_id not in self._storage:
            return ServiceResponse.error_response(
                f"Page not found: {page_id}",
                errors=["Page not found"]
            )
        
        del self._storage[page_id]
        return ServiceResponse.success_response("Page deleted successfully")


class WidgetService:
    """Service for managing widgets"""
    
    def __init__(self):
        self._storage: Dict[str, Widget] = {}
        self._templates: Dict[str, WidgetTemplate] = {}
    
    def create_widget(
        self,
        title: str,
        widget_type: WidgetType,
        page_id: str,
        zone_id: str,
        content: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None,
        position: int = 0,
        created_by: Optional[str] = None
    ) -> ServiceResponse:
        """Create a new widget"""
        try:
            widget = Widget(
                id=str(uuid4()),
                title=title,
                widget_type=widget_type,
                page_id=page_id,
                zone_id=zone_id,
                position=position,
                content=content or {},
                settings=settings or {},
                created_by=created_by
            )
            
            self._storage[widget.id] = widget
            
            return ServiceResponse.success_response(
                "Widget created successfully",
                data=widget.model_dump()
            )
        except Exception as e:
            return ServiceResponse.error_response("Failed to create widget", errors=[str(e)])
    
    def get_widget(self, widget_id: str) -> ServiceResponse:
        """Get a widget by ID"""
        widget = self._storage.get(widget_id)
        if not widget:
            return ServiceResponse.error_response(
                f"Widget not found: {widget_id}",
                errors=["Widget not found"]
            )
        
        return ServiceResponse.success_response(
            "Widget retrieved",
            data=widget.model_dump()
        )
    
    def list_widgets_for_page(self, page_id: str, zone_id: Optional[str] = None) -> ServiceResponse:
        """List widgets for a page, optionally filtered by zone"""
        widgets = []
        for widget in self._storage.values():
            if widget.page_id == page_id:
                if zone_id is None or widget.zone_id == zone_id:
                    widgets.append(widget)
        
        # Sort widgets by position before converting to dict
        widgets.sort(key=lambda w: w.position)
        
        # Convert to dict after sorting
        widget_dicts = [w.model_dump() for w in widgets]
        
        return ServiceResponse.success_response(
            f"Found {len(widget_dicts)} widget(s)",
            data={"widgets": widget_dicts}
        )
    
    def update_widget(self, widget_id: str, **updates) -> ServiceResponse:
        """Update a widget"""
        widget = self._storage.get(widget_id)
        if not widget:
            return ServiceResponse.error_response(
                f"Widget not found: {widget_id}",
                errors=["Widget not found"]
            )
        
        try:
            for key, value in updates.items():
                if hasattr(widget, key):
                    setattr(widget, key, value)
            
            return ServiceResponse.success_response(
                "Widget updated successfully",
                data=widget.model_dump()
            )
        except Exception as e:
            return ServiceResponse.error_response("Failed to update widget", errors=[str(e)])
    
    def delete_widget(self, widget_id: str) -> ServiceResponse:
        """Delete a widget"""
        if widget_id not in self._storage:
            return ServiceResponse.error_response(
                f"Widget not found: {widget_id}",
                errors=["Widget not found"]
            )
        
        del self._storage[widget_id]
        return ServiceResponse.success_response("Widget deleted successfully")
    
    def create_widget_template(
        self,
        name: str,
        title: str,
        widget_type: WidgetType,
        organization_id: Optional[str] = None,
        is_global: bool = False,
        default_content: Optional[Dict[str, Any]] = None,
        default_settings: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None
    ) -> ServiceResponse:
        """Create a widget template"""
        try:
            template = WidgetTemplate(
                id=str(uuid4()),
                name=name,
                title=title,
                widget_type=widget_type,
                organization_id=organization_id,
                is_global=is_global,
                default_content=default_content or {},
                default_settings=default_settings or {},
                created_by=created_by
            )
            
            self._templates[template.id] = template
            
            return ServiceResponse.success_response(
                "Widget template created successfully",
                data=template.model_dump()
            )
        except Exception as e:
            return ServiceResponse.error_response("Failed to create widget template", errors=[str(e)])
    
    def list_widget_templates(
        self,
        organization_id: Optional[str] = None,
        widget_type: Optional[WidgetType] = None,
        include_global: bool = True
    ) -> ServiceResponse:
        """List widget templates"""
        templates = []
        for template in self._templates.values():
            if organization_id:
                if not (template.organization_id == organization_id or (include_global and template.is_global)):
                    continue
            if widget_type and template.widget_type != widget_type:
                continue
            
            templates.append(template.model_dump())
        
        return ServiceResponse.success_response(
            f"Found {len(templates)} template(s)",
            data={"templates": templates}
        )
