"""
Tests for CMS API endpoints
"""

import pytest
import json
from src.api.app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestMasterPageAPI:
    """Tests for Master Page API endpoints"""
    
    def test_create_master_page(self, client):
        """Test creating a master page via API"""
        response = client.post(
            '/api/cms/master-pages',
            data=json.dumps({
                'name': 'test-master',
                'title': 'Test Master Page',
                'html_template': '<html>{{content}}</html>',
                'content_placeholders': ['main', 'sidebar']
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'test-master'
    
    def test_list_master_pages(self, client):
        """Test listing master pages"""
        # Create a master page first
        client.post(
            '/api/cms/master-pages',
            data=json.dumps({
                'name': 'master1',
                'title': 'Master 1',
                'html_template': '<html></html>'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/cms/master-pages')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['master_pages']) >= 1
    
    def test_get_master_page(self, client):
        """Test getting a specific master page"""
        # Create a master page
        create_response = client.post(
            '/api/cms/master-pages',
            data=json.dumps({
                'name': 'get-test',
                'title': 'Get Test',
                'html_template': '<html></html>'
            }),
            content_type='application/json'
        )
        
        master_page_id = json.loads(create_response.data)['data']['id']
        
        # Get the master page
        response = client.get(f'/api/cms/master-pages/{master_page_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == master_page_id
    
    def test_update_master_page(self, client):
        """Test updating a master page"""
        # Create a master page
        create_response = client.post(
            '/api/cms/master-pages',
            data=json.dumps({
                'name': 'update-test',
                'title': 'Update Test',
                'html_template': '<html></html>'
            }),
            content_type='application/json'
        )
        
        master_page_id = json.loads(create_response.data)['data']['id']
        
        # Update the master page
        response = client.put(
            f'/api/cms/master-pages/{master_page_id}',
            data=json.dumps({
                'title': 'Updated Title'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'Updated Title'
    
    def test_delete_master_page(self, client):
        """Test deleting a master page"""
        # Create a master page
        create_response = client.post(
            '/api/cms/master-pages',
            data=json.dumps({
                'name': 'delete-test',
                'title': 'Delete Test',
                'html_template': '<html></html>'
            }),
            content_type='application/json'
        )
        
        master_page_id = json.loads(create_response.data)['data']['id']
        
        # Delete the master page
        response = client.delete(f'/api/cms/master-pages/{master_page_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True


class TestPageLayoutAPI:
    """Tests for Page Layout API endpoints"""
    
    def test_create_layout(self, client):
        """Test creating a page layout"""
        response = client.post(
            '/api/cms/layouts',
            data=json.dumps({
                'name': 'two-column',
                'title': 'Two Column Layout',
                'master_page_id': 'mp1',
                'layout_template': '<div>{{content}}</div>',
                'page_types': ['content', 'landing']
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'two-column'
    
    def test_list_layouts(self, client):
        """Test listing layouts"""
        # Create a layout
        client.post(
            '/api/cms/layouts',
            data=json.dumps({
                'name': 'layout1',
                'title': 'Layout 1',
                'master_page_id': 'mp1',
                'layout_template': '<div></div>'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/cms/layouts')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['layouts']) >= 1


class TestPageAPI:
    """Tests for Page API endpoints"""
    
    def test_create_page(self, client):
        """Test creating a page"""
        response = client.post(
            '/api/cms/pages',
            data=json.dumps({
                'title': 'Test Page',
                'slug': 'test-page',
                'page_layout_id': 'pl1',
                'page_type': 'content'
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'Test Page'
        assert data['data']['slug'] == 'test-page'
    
    def test_list_pages(self, client):
        """Test listing pages"""
        # Create a page
        client.post(
            '/api/cms/pages',
            data=json.dumps({
                'title': 'List Test Page',
                'slug': 'list-test',
                'page_layout_id': 'pl1'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/cms/pages')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['pages']) >= 1
    
    def test_get_page_by_slug(self, client):
        """Test getting a page by slug"""
        # Create a page
        client.post(
            '/api/cms/pages',
            data=json.dumps({
                'title': 'Slug Test',
                'slug': 'slug-test',
                'page_layout_id': 'pl1'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/cms/pages/by-slug/slug-test')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['slug'] == 'slug-test'
    
    def test_publish_page(self, client):
        """Test publishing a page"""
        # Create a page
        create_response = client.post(
            '/api/cms/pages',
            data=json.dumps({
                'title': 'Publish Test',
                'slug': 'publish-test',
                'page_layout_id': 'pl1'
            }),
            content_type='application/json'
        )
        
        page_id = json.loads(create_response.data)['data']['id']
        
        # Publish the page
        response = client.post(
            f'/api/cms/pages/{page_id}/publish',
            data=json.dumps({'published_by': 'user1'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['status'] == 'published'


class TestWidgetAPI:
    """Tests for Widget API endpoints"""
    
    def test_create_widget(self, client):
        """Test creating a widget"""
        response = client.post(
            '/api/cms/widgets',
            data=json.dumps({
                'title': 'Test Widget',
                'widget_type': 'text',
                'page_id': 'p1',
                'zone_id': 'main',
                'content': {'text': 'Hello world'}
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['title'] == 'Test Widget'
    
    def test_list_widgets(self, client):
        """Test listing widgets for a page"""
        # Create a widget
        client.post(
            '/api/cms/widgets',
            data=json.dumps({
                'title': 'Widget 1',
                'widget_type': 'text',
                'page_id': 'p1',
                'zone_id': 'main'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/cms/widgets?page_id=p1')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['widgets']) >= 1
    
    def test_list_widgets_missing_page_id(self, client):
        """Test listing widgets without page_id"""
        response = client.get('/api/cms/widgets')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False


class TestWidgetTemplateAPI:
    """Tests for Widget Template API endpoints"""
    
    def test_create_widget_template(self, client):
        """Test creating a widget template"""
        response = client.post(
            '/api/cms/widget-templates',
            data=json.dumps({
                'name': 'hero-banner',
                'title': 'Hero Banner',
                'widget_type': 'html',
                'default_content': {'html': '<div>Hero</div>'}
            }),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['name'] == 'hero-banner'
    
    def test_list_widget_templates(self, client):
        """Test listing widget templates"""
        # Create a template
        client.post(
            '/api/cms/widget-templates',
            data=json.dumps({
                'name': 'template1',
                'title': 'Template 1',
                'widget_type': 'text'
            }),
            content_type='application/json'
        )
        
        response = client.get('/api/cms/widget-templates')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert len(data['data']['templates']) >= 1


class TestCMSHealth:
    """Test CMS health endpoint"""
    
    def test_cms_health(self, client):
        """Test CMS health check"""
        response = client.get('/api/cms/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert data['module'] == 'CMS API'
