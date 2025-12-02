"""
CMS API Routes

RESTful API endpoints for SharePoint-style CMS management:
- Master pages
- Page layouts
- Pages
- Widgets
"""

from flask import Blueprint, request, jsonify
from typing import Optional

from src.cms.pages import (
    MasterPageService,
    PageLayoutService,
    PageService,
    WidgetService,
    PageType,
    PageStatus,
    WidgetType
)

# Create blueprint
cms_bp = Blueprint('cms', __name__, url_prefix='/api/cms')

# Initialize services
master_page_service = MasterPageService()
page_layout_service = PageLayoutService()
page_service = PageService()
widget_service = WidgetService()


# Master Page Endpoints

@cms_bp.route('/master-pages', methods=['POST'])
def create_master_page():
    """Create a new master page"""
    data = request.get_json()
    
    response = master_page_service.create_master_page(
        name=data.get('name'),
        title=data.get('title'),
        html_template=data.get('html_template'),
        description=data.get('description'),
        organization_id=data.get('organization_id'),
        is_global=data.get('is_global', False),
        css_references=data.get('css_references', []),
        js_references=data.get('js_references', []),
        content_placeholders=data.get('content_placeholders', []),
        created_by=data.get('created_by')
    )
    
    status_code = 201 if response.success else 400
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/master-pages', methods=['GET'])
def list_master_pages():
    """List all master pages"""
    organization_id = request.args.get('organization_id')
    include_global = request.args.get('include_global', 'true').lower() == 'true'
    
    response = master_page_service.list_master_pages(
        organization_id=organization_id,
        include_global=include_global
    )
    
    return jsonify(response.model_dump())


@cms_bp.route('/master-pages/<master_page_id>', methods=['GET'])
def get_master_page(master_page_id: str):
    """Get a specific master page"""
    response = master_page_service.get_master_page(master_page_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/master-pages/<master_page_id>', methods=['PUT'])
def update_master_page(master_page_id: str):
    """Update a master page"""
    data = request.get_json()
    
    response = master_page_service.update_master_page(
        master_page_id,
        **data
    )
    
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/master-pages/<master_page_id>', methods=['DELETE'])
def delete_master_page(master_page_id: str):
    """Delete a master page"""
    response = master_page_service.delete_master_page(master_page_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


# Page Layout Endpoints

@cms_bp.route('/layouts', methods=['POST'])
def create_layout():
    """Create a new page layout"""
    data = request.get_json()
    
    # Convert page_types strings to PageType enums
    page_types = None
    if 'page_types' in data:
        page_types = [PageType(pt) for pt in data['page_types']]
    
    response = page_layout_service.create_layout(
        name=data.get('name'),
        title=data.get('title'),
        master_page_id=data.get('master_page_id'),
        layout_template=data.get('layout_template'),
        description=data.get('description'),
        organization_id=data.get('organization_id'),
        is_global=data.get('is_global', False),
        content_zones=data.get('content_zones', []),
        fields=data.get('fields', []),
        page_types=page_types,
        created_by=data.get('created_by')
    )
    
    status_code = 201 if response.success else 400
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/layouts', methods=['GET'])
def list_layouts():
    """List page layouts"""
    organization_id = request.args.get('organization_id')
    master_page_id = request.args.get('master_page_id')
    page_type = request.args.get('page_type')
    include_global = request.args.get('include_global', 'true').lower() == 'true'
    
    # Convert page_type string to enum if provided
    page_type_enum = PageType(page_type) if page_type else None
    
    response = page_layout_service.list_layouts(
        organization_id=organization_id,
        master_page_id=master_page_id,
        page_type=page_type_enum,
        include_global=include_global
    )
    
    return jsonify(response.model_dump())


@cms_bp.route('/layouts/<layout_id>', methods=['GET'])
def get_layout(layout_id: str):
    """Get a specific page layout"""
    response = page_layout_service.get_layout(layout_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/layouts/<layout_id>', methods=['PUT'])
def update_layout(layout_id: str):
    """Update a page layout"""
    data = request.get_json()
    
    response = page_layout_service.update_layout(
        layout_id,
        **data
    )
    
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/layouts/<layout_id>', methods=['DELETE'])
def delete_layout(layout_id: str):
    """Delete a page layout"""
    response = page_layout_service.delete_layout(layout_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


# Page Endpoints

@cms_bp.route('/pages', methods=['POST'])
def create_page():
    """Create a new page"""
    data = request.get_json()
    
    # Convert page_type string to enum if provided
    page_type = PageType(data['page_type']) if 'page_type' in data else PageType.CONTENT
    
    response = page_service.create_page(
        title=data.get('title'),
        slug=data.get('slug'),
        page_layout_id=data.get('page_layout_id'),
        organization_id=data.get('organization_id'),
        page_type=page_type,
        description=data.get('description'),
        author_id=data.get('author_id'),
        created_by=data.get('created_by')
    )
    
    status_code = 201 if response.success else 400
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/pages', methods=['GET'])
def list_pages():
    """List pages"""
    organization_id = request.args.get('organization_id')
    page_type = request.args.get('page_type')
    status = request.args.get('status')
    parent_page_id = request.args.get('parent_page_id')
    
    # Convert enums
    page_type_enum = PageType(page_type) if page_type else None
    status_enum = PageStatus(status) if status else None
    
    response = page_service.list_pages(
        organization_id=organization_id,
        page_type=page_type_enum,
        status=status_enum,
        parent_page_id=parent_page_id
    )
    
    return jsonify(response.model_dump())


@cms_bp.route('/pages/<page_id>', methods=['GET'])
def get_page(page_id: str):
    """Get a specific page"""
    response = page_service.get_page(page_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/pages/by-slug/<slug>', methods=['GET'])
def get_page_by_slug(slug: str):
    """Get a page by slug"""
    organization_id = request.args.get('organization_id')
    
    response = page_service.get_page_by_slug(slug, organization_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/pages/<page_id>', methods=['PUT'])
def update_page(page_id: str):
    """Update a page"""
    data = request.get_json()
    
    response = page_service.update_page(
        page_id,
        **data
    )
    
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/pages/<page_id>/publish', methods=['POST'])
def publish_page(page_id: str):
    """Publish a page"""
    data = request.get_json() or {}
    
    response = page_service.publish_page(
        page_id,
        published_by=data.get('published_by')
    )
    
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/pages/<page_id>', methods=['DELETE'])
def delete_page(page_id: str):
    """Delete a page"""
    response = page_service.delete_page(page_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


# Widget Endpoints

@cms_bp.route('/widgets', methods=['POST'])
def create_widget():
    """Create a new widget"""
    data = request.get_json()
    
    # Convert widget_type string to enum
    widget_type = WidgetType(data['widget_type'])
    
    response = widget_service.create_widget(
        title=data.get('title'),
        widget_type=widget_type,
        page_id=data.get('page_id'),
        zone_id=data.get('zone_id'),
        content=data.get('content'),
        settings=data.get('settings'),
        position=data.get('position', 0),
        created_by=data.get('created_by')
    )
    
    status_code = 201 if response.success else 400
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/widgets', methods=['GET'])
def list_widgets():
    """List widgets for a page"""
    page_id = request.args.get('page_id')
    zone_id = request.args.get('zone_id')
    
    if not page_id:
        return jsonify({
            'success': False,
            'message': 'page_id parameter is required',
            'data': None,
            'errors': ['Missing page_id parameter']
        }), 400
    
    response = widget_service.list_widgets_for_page(page_id, zone_id)
    return jsonify(response.model_dump())


@cms_bp.route('/widgets/<widget_id>', methods=['GET'])
def get_widget(widget_id: str):
    """Get a specific widget"""
    response = widget_service.get_widget(widget_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/widgets/<widget_id>', methods=['PUT'])
def update_widget(widget_id: str):
    """Update a widget"""
    data = request.get_json()
    
    response = widget_service.update_widget(
        widget_id,
        **data
    )
    
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/widgets/<widget_id>', methods=['DELETE'])
def delete_widget(widget_id: str):
    """Delete a widget"""
    response = widget_service.delete_widget(widget_id)
    status_code = 200 if response.success else 404
    return jsonify(response.model_dump()), status_code


# Widget Template Endpoints

@cms_bp.route('/widget-templates', methods=['POST'])
def create_widget_template():
    """Create a new widget template"""
    data = request.get_json()
    
    # Convert widget_type string to enum
    widget_type = WidgetType(data['widget_type'])
    
    response = widget_service.create_widget_template(
        name=data.get('name'),
        title=data.get('title'),
        widget_type=widget_type,
        organization_id=data.get('organization_id'),
        is_global=data.get('is_global', False),
        default_content=data.get('default_content'),
        default_settings=data.get('default_settings'),
        created_by=data.get('created_by')
    )
    
    status_code = 201 if response.success else 400
    return jsonify(response.model_dump()), status_code


@cms_bp.route('/widget-templates', methods=['GET'])
def list_widget_templates():
    """List widget templates"""
    organization_id = request.args.get('organization_id')
    widget_type = request.args.get('widget_type')
    include_global = request.args.get('include_global', 'true').lower() == 'true'
    
    # Convert widget_type string to enum if provided
    widget_type_enum = WidgetType(widget_type) if widget_type else None
    
    response = widget_service.list_widget_templates(
        organization_id=organization_id,
        widget_type=widget_type_enum,
        include_global=include_global
    )
    
    return jsonify(response.model_dump())


# Health check for CMS API
@cms_bp.route('/health', methods=['GET'])
def cms_health():
    """CMS API health check"""
    return jsonify({
        'status': 'healthy',
        'module': 'CMS API',
        'version': '1.0.0'
    })
