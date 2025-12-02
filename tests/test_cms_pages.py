"""
Tests for SharePoint-inspired CMS Pages module
"""

import pytest
from datetime import datetime
from src.cms.pages import (
    PageType, PageStatus, ContentZoneType, WidgetType,
    MasterPage, PageLayout, Page, Widget,
    MasterPageService, PageLayoutService, PageService, WidgetService
)


class TestMasterPageModel:
    """Tests for MasterPage model"""
    
    def test_create_master_page(self):
        """Test creating a master page"""
        master_page = MasterPage(
            id="mp1",
            name="default-master",
            title="Default Master Page",
            html_template="<html>{{content}}</html>",
            content_placeholders=["main", "sidebar"]
        )
        
        assert master_page.name == "default-master"
        assert master_page.title == "Default Master Page"
        assert "main" in master_page.content_placeholders
        assert master_page.is_active is True
    
    def test_master_page_validation(self):
        """Test master page name validation"""
        with pytest.raises(ValueError, match="Master page name cannot be empty"):
            MasterPage(
                name="  ",
                title="Test",
                html_template="<html></html>"
            )


class TestPageLayoutModel:
    """Tests for PageLayout model"""
    
    def test_create_page_layout(self):
        """Test creating a page layout"""
        layout = PageLayout(
            id="pl1",
            name="two-column",
            title="Two Column Layout",
            master_page_id="mp1",
            layout_template="<div>{{content}}</div>",
            page_types=[PageType.CONTENT, PageType.LANDING]
        )
        
        assert layout.name == "two-column"
        assert layout.master_page_id == "mp1"
        assert PageType.CONTENT in layout.page_types
    
    def test_page_layout_validation(self):
        """Test page layout name validation"""
        with pytest.raises(ValueError, match="Layout name cannot be empty"):
            PageLayout(
                name="",
                title="Test",
                master_page_id="mp1",
                layout_template="<div></div>"
            )


class TestPageModel:
    """Tests for Page model"""
    
    def test_create_page(self):
        """Test creating a page"""
        page = Page(
            id="p1",
            title="Home Page",
            slug="home",
            page_layout_id="pl1",
            page_type=PageType.CONTENT,
            status=PageStatus.DRAFT
        )
        
        assert page.title == "Home Page"
        assert page.slug == "home"
        assert page.status == PageStatus.DRAFT
        assert page.is_public is True
    
    def test_page_slug_validation(self):
        """Test page slug validation"""
        with pytest.raises(ValueError, match="Slug must contain only lowercase"):
            Page(
                title="Test Page",
                slug="Invalid Slug!",
                page_layout_id="pl1"
            )
    
    def test_page_with_content_zones(self):
        """Test page with content zones data"""
        page = Page(
            title="Content Page",
            slug="content-page",
            page_layout_id="pl1",
            content_zones_data={
                "main": {"text": "Main content here"},
                "sidebar": {"widgets": ["widget1", "widget2"]}
            }
        )
        
        assert "main" in page.content_zones_data
        assert "sidebar" in page.content_zones_data


class TestWidgetModel:
    """Tests for Widget model"""
    
    def test_create_widget(self):
        """Test creating a widget"""
        widget = Widget(
            id="w1",
            title="Text Widget",
            widget_type=WidgetType.TEXT,
            page_id="p1",
            zone_id="zone1",
            content={"text": "Hello world"},
            position=0
        )
        
        assert widget.title == "Text Widget"
        assert widget.widget_type == WidgetType.TEXT
        assert widget.content["text"] == "Hello world"


class TestMasterPageService:
    """Tests for MasterPageService"""
    
    def test_create_master_page(self):
        """Test creating a master page via service"""
        service = MasterPageService()
        
        response = service.create_master_page(
            name="default",
            title="Default Master",
            html_template="<html>{{content}}</html>",
            content_placeholders=["main"]
        )
        
        assert response.success is True
        assert response.data["name"] == "default"
        assert response.data["id"] is not None
    
    def test_create_duplicate_master_page(self):
        """Test creating duplicate master page"""
        service = MasterPageService()
        
        service.create_master_page(
            name="default",
            title="Default Master",
            html_template="<html>{{content}}</html>"
        )
        
        response = service.create_master_page(
            name="default",
            title="Another Default",
            html_template="<html>{{content}}</html>"
        )
        
        assert response.success is False
        assert "already exists" in response.message
    
    def test_get_master_page(self):
        """Test getting a master page"""
        service = MasterPageService()
        
        create_response = service.create_master_page(
            name="test",
            title="Test Master",
            html_template="<html>{{content}}</html>"
        )
        
        master_page_id = create_response.data["id"]
        get_response = service.get_master_page(master_page_id)
        
        assert get_response.success is True
        assert get_response.data["id"] == master_page_id
    
    def test_list_master_pages(self):
        """Test listing master pages"""
        service = MasterPageService()
        
        service.create_master_page(
            name="master1",
            title="Master 1",
            html_template="<html></html>",
            organization_id="org1"
        )
        
        service.create_master_page(
            name="master2",
            title="Master 2",
            html_template="<html></html>",
            organization_id="org2"
        )
        
        response = service.list_master_pages(organization_id="org1", include_global=False)
        
        assert response.success is True
        assert len(response.data["master_pages"]) == 1
    
    def test_update_master_page(self):
        """Test updating a master page"""
        service = MasterPageService()
        
        create_response = service.create_master_page(
            name="test",
            title="Test Master",
            html_template="<html></html>"
        )
        
        master_page_id = create_response.data["id"]
        update_response = service.update_master_page(
            master_page_id,
            title="Updated Master"
        )
        
        assert update_response.success is True
        assert update_response.data["title"] == "Updated Master"
    
    def test_delete_master_page(self):
        """Test deleting a master page"""
        service = MasterPageService()
        
        create_response = service.create_master_page(
            name="test",
            title="Test Master",
            html_template="<html></html>"
        )
        
        master_page_id = create_response.data["id"]
        delete_response = service.delete_master_page(master_page_id)
        
        assert delete_response.success is True
        
        get_response = service.get_master_page(master_page_id)
        assert get_response.success is False


class TestPageLayoutService:
    """Tests for PageLayoutService"""
    
    def test_create_layout(self):
        """Test creating a page layout"""
        service = PageLayoutService()
        
        response = service.create_layout(
            name="two-column",
            title="Two Column Layout",
            master_page_id="mp1",
            layout_template="<div>{{content}}</div>",
            page_types=[PageType.CONTENT]
        )
        
        assert response.success is True
        assert response.data["name"] == "two-column"
    
    def test_list_layouts_by_master_page(self):
        """Test listing layouts filtered by master page"""
        service = PageLayoutService()
        
        service.create_layout(
            name="layout1",
            title="Layout 1",
            master_page_id="mp1",
            layout_template="<div></div>"
        )
        
        service.create_layout(
            name="layout2",
            title="Layout 2",
            master_page_id="mp2",
            layout_template="<div></div>"
        )
        
        response = service.list_layouts(master_page_id="mp1")
        
        assert response.success is True
        assert len(response.data["layouts"]) == 1
        assert response.data["layouts"][0]["master_page_id"] == "mp1"


class TestPageService:
    """Tests for PageService"""
    
    def test_create_page(self):
        """Test creating a page"""
        service = PageService()
        
        response = service.create_page(
            title="Home Page",
            slug="home",
            page_layout_id="pl1",
            organization_id="org1"
        )
        
        assert response.success is True
        assert response.data["title"] == "Home Page"
        assert response.data["slug"] == "home"
        assert response.data["status"] == PageStatus.DRAFT
    
    def test_create_duplicate_slug(self):
        """Test creating page with duplicate slug"""
        service = PageService()
        
        service.create_page(
            title="Page 1",
            slug="home",
            page_layout_id="pl1",
            organization_id="org1"
        )
        
        response = service.create_page(
            title="Page 2",
            slug="home",
            page_layout_id="pl1",
            organization_id="org1"
        )
        
        assert response.success is False
        assert "already exists" in response.message
    
    def test_get_page_by_slug(self):
        """Test getting page by slug"""
        service = PageService()
        
        service.create_page(
            title="Test Page",
            slug="test-page",
            page_layout_id="pl1",
            organization_id="org1"
        )
        
        response = service.get_page_by_slug("test-page", organization_id="org1")
        
        assert response.success is True
        assert response.data["slug"] == "test-page"
    
    def test_publish_page(self):
        """Test publishing a page"""
        service = PageService()
        
        create_response = service.create_page(
            title="Draft Page",
            slug="draft-page",
            page_layout_id="pl1"
        )
        
        page_id = create_response.data["id"]
        publish_response = service.publish_page(page_id, published_by="user1")
        
        assert publish_response.success is True
        assert publish_response.data["status"] == PageStatus.PUBLISHED
        assert publish_response.data["published_at"] is not None
    
    def test_list_pages_by_type(self):
        """Test listing pages by type"""
        service = PageService()
        
        service.create_page(
            title="Content Page",
            slug="content",
            page_layout_id="pl1",
            page_type=PageType.CONTENT
        )
        
        service.create_page(
            title="Landing Page",
            slug="landing",
            page_layout_id="pl1",
            page_type=PageType.LANDING
        )
        
        response = service.list_pages(page_type=PageType.CONTENT)
        
        assert response.success is True
        assert len(response.data["pages"]) == 1
        assert response.data["pages"][0]["page_type"] == PageType.CONTENT


class TestWidgetService:
    """Tests for WidgetService"""
    
    def test_create_widget(self):
        """Test creating a widget"""
        service = WidgetService()
        
        response = service.create_widget(
            title="Text Widget",
            widget_type=WidgetType.TEXT,
            page_id="p1",
            zone_id="main",
            content={"text": "Hello world"}
        )
        
        assert response.success is True
        assert response.data["title"] == "Text Widget"
        assert response.data["content"]["text"] == "Hello world"
    
    def test_list_widgets_for_page(self):
        """Test listing widgets for a page"""
        service = WidgetService()
        
        service.create_widget(
            title="Widget 1",
            widget_type=WidgetType.TEXT,
            page_id="p1",
            zone_id="main",
            position=1
        )
        
        service.create_widget(
            title="Widget 2",
            widget_type=WidgetType.IMAGE,
            page_id="p1",
            zone_id="main",
            position=0
        )
        
        service.create_widget(
            title="Widget 3",
            widget_type=WidgetType.TEXT,
            page_id="p2",
            zone_id="main"
        )
        
        response = service.list_widgets_for_page("p1")
        
        assert response.success is True
        assert len(response.data["widgets"]) == 2
        # Check sorting by position
        assert response.data["widgets"][0]["position"] == 0
        assert response.data["widgets"][1]["position"] == 1
    
    def test_create_widget_template(self):
        """Test creating a widget template"""
        service = WidgetService()
        
        response = service.create_widget_template(
            name="hero-banner",
            title="Hero Banner",
            widget_type=WidgetType.HTML,
            default_content={"html": "<div class='hero'>{{title}}</div>"},
            default_settings={"height": "400px"}
        )
        
        assert response.success is True
        assert response.data["name"] == "hero-banner"
    
    def test_list_widget_templates_by_type(self):
        """Test listing widget templates by type"""
        service = WidgetService()
        
        service.create_widget_template(
            name="text-template",
            title="Text Template",
            widget_type=WidgetType.TEXT
        )
        
        service.create_widget_template(
            name="image-template",
            title="Image Template",
            widget_type=WidgetType.IMAGE
        )
        
        response = service.list_widget_templates(widget_type=WidgetType.TEXT)
        
        assert response.success is True
        assert len(response.data["templates"]) == 1
        assert response.data["templates"][0]["widget_type"] == WidgetType.TEXT
