# SharePoint-Style CMS System

A comprehensive, flexible content management system inspired by SharePoint, designed for modern web applications with multi-tenant support.

## Overview

The CMS system provides a hierarchical approach to content management with:

- **Master Pages**: Define the overall site structure and chrome (header, footer, navigation)
- **Page Layouts**: Templates that use master pages and define content zones
- **Pages**: Actual content pages that use layouts and contain widgets
- **Content Zones**: Modular areas within pages for placing widgets
- **Widgets**: Reusable content components (text, images, forms, etc.)
- **Multi-tenant Support**: Organization-scoped content with global templates

## Architecture

### Content Hierarchy

```
Master Page (Site Structure)
    └── Page Layout (Content Structure)
        └── Page (Actual Content)
            └── Content Zones
                └── Widgets
```

### Key Concepts

#### Master Pages

Master pages define the overall structure of your site:

- Site header and navigation
- Footer
- Common CSS and JavaScript references
- Content placeholders where page layouts can inject content

**Example Use Case**: A corporate site might have different master pages for:
- Public-facing pages (with marketing header/footer)
- Internal portal pages (with employee navigation)
- Minimalist landing pages (with simplified chrome)

#### Page Layouts

Page layouts define the structure of content within a master page:

- Content zone configuration
- Custom field definitions for structured content
- Page type compatibility (content, landing, system, application)

**Example Use Case**: Common layout templates:
- Two-column blog layout (main content + sidebar)
- Full-width landing page layout
- Three-column product showcase layout
- Dashboard layout with multiple widget zones

#### Pages

Pages are the actual content that users see:

- Use a specific page layout
- Have a unique URL slug
- Support draft, published, archived, and scheduled states
- Include SEO metadata
- Can be organized in hierarchies for navigation

#### Content Zones

Content zones are placeholders for widgets:

- Can restrict allowed widget types
- Support positioning and styling
- Can be locked to prevent editing

#### Widgets

Widgets are reusable content components:

- Multiple types: text, HTML, images, videos, forms, navigation, search
- Customizable content and settings
- Can be templated for reuse
- Position-aware for ordering within zones

## Database Models

### MasterPage

```python
{
    "id": "uuid",
    "name": "default-master",
    "title": "Default Master Page",
    "html_template": "<html>{{content}}</html>",
    "css_references": ["/css/main.css"],
    "js_references": ["/js/main.js"],
    "content_placeholders": ["header", "main", "footer"],
    "organization_id": "org-123",  # or null for global
    "is_global": false,
    "is_default": false,
    "created_at": "2025-12-02T00:00:00Z",
    "updated_at": "2025-12-02T00:00:00Z"
}
```

### PageLayout

```python
{
    "id": "uuid",
    "name": "two-column",
    "title": "Two Column Layout",
    "master_page_id": "mp-uuid",
    "layout_template": "<div class='container'>{{content}}</div>",
    "content_zones": [
        {
            "name": "main",
            "title": "Main Content",
            "zone_type": "main",
            "allowed_widget_types": ["text", "html", "image"]
        },
        {
            "name": "sidebar",
            "title": "Sidebar",
            "zone_type": "sidebar",
            "max_widgets": 5
        }
    ],
    "fields": [
        {
            "name": "hero_image",
            "type": "image",
            "required": false
        }
    ],
    "page_types": ["content", "landing"],
    "organization_id": "org-123",
    "is_global": false
}
```

### Page

```python
{
    "id": "uuid",
    "title": "About Us",
    "slug": "about-us",
    "description": "Learn about our company",
    "page_layout_id": "layout-uuid",
    "page_type": "content",
    "status": "published",
    "organization_id": "org-123",
    "published_at": "2025-12-02T00:00:00Z",
    "author_id": "user-123",
    "meta_title": "About Us - Company Name",
    "meta_description": "Our company story",
    "meta_keywords": ["about", "company", "team"],
    "content_zones_data": {
        "main": {
            "widgets": ["widget-1", "widget-2"]
        }
    },
    "field_values": {
        "hero_image": "/images/hero.jpg"
    },
    "parent_page_id": null,
    "menu_title": "About",
    "include_in_menu": true,
    "is_public": true,
    "version": 1
}
```

### Widget

```python
{
    "id": "uuid",
    "title": "Welcome Text",
    "widget_type": "text",
    "page_id": "page-uuid",
    "zone_id": "main",
    "position": 0,
    "content": {
        "text": "Welcome to our site!",
        "format": "markdown"
    },
    "settings": {
        "font_size": "large",
        "alignment": "center"
    },
    "css_classes": ["hero-text"],
    "is_visible": true
}
```

## API Endpoints

### Master Pages

- `POST /api/cms/master-pages` - Create master page
- `GET /api/cms/master-pages` - List master pages
- `GET /api/cms/master-pages/{id}` - Get master page
- `PUT /api/cms/master-pages/{id}` - Update master page
- `DELETE /api/cms/master-pages/{id}` - Delete master page

### Page Layouts

- `POST /api/cms/layouts` - Create layout
- `GET /api/cms/layouts` - List layouts
- `GET /api/cms/layouts/{id}` - Get layout
- `PUT /api/cms/layouts/{id}` - Update layout
- `DELETE /api/cms/layouts/{id}` - Delete layout

### Pages

- `POST /api/cms/pages` - Create page
- `GET /api/cms/pages` - List pages
- `GET /api/cms/pages/{id}` - Get page
- `GET /api/cms/pages/by-slug/{slug}` - Get page by slug
- `PUT /api/cms/pages/{id}` - Update page
- `POST /api/cms/pages/{id}/publish` - Publish page
- `DELETE /api/cms/pages/{id}` - Delete page

### Widgets

- `POST /api/cms/widgets` - Create widget
- `GET /api/cms/widgets?page_id={id}` - List widgets for page
- `GET /api/cms/widgets/{id}` - Get widget
- `PUT /api/cms/widgets/{id}` - Update widget
- `DELETE /api/cms/widgets/{id}` - Delete widget

### Widget Templates

- `POST /api/cms/widget-templates` - Create template
- `GET /api/cms/widget-templates` - List templates

## Usage Examples

### Creating a Simple Page

```python
# 1. Create a master page
POST /api/cms/master-pages
{
    "name": "main-site",
    "title": "Main Site Master",
    "html_template": "<html><head>{{head}}</head><body>{{body}}</body></html>",
    "content_placeholders": ["head", "body"]
}

# 2. Create a page layout
POST /api/cms/layouts
{
    "name": "blog-post",
    "title": "Blog Post Layout",
    "master_page_id": "<master-page-id>",
    "layout_template": "<article>{{content}}</article>",
    "content_zones": [
        {
            "name": "main",
            "title": "Main Content",
            "zone_type": "main"
        }
    ]
}

# 3. Create a page
POST /api/cms/pages
{
    "title": "My First Blog Post",
    "slug": "my-first-post",
    "page_layout_id": "<layout-id>",
    "page_type": "content"
}

# 4. Add a widget to the page
POST /api/cms/widgets
{
    "title": "Post Content",
    "widget_type": "html",
    "page_id": "<page-id>",
    "zone_id": "main",
    "content": {
        "html": "<h1>Welcome!</h1><p>This is my first post.</p>"
    }
}

# 5. Publish the page
POST /api/cms/pages/<page-id>/publish
{
    "published_by": "user-id"
}
```

### Multi-Tenant Usage

```python
# Create organization-specific master page
POST /api/cms/master-pages
{
    "name": "acme-corp-master",
    "title": "ACME Corp Master",
    "organization_id": "org-acme",
    "html_template": "...",
    "is_global": false
}

# List master pages for organization (includes global)
GET /api/cms/master-pages?organization_id=org-acme&include_global=true

# Create page scoped to organization
POST /api/cms/pages
{
    "title": "ACME Home",
    "slug": "home",
    "organization_id": "org-acme",
    "page_layout_id": "<layout-id>"
}
```

## Page Types

### Content Pages
Regular content pages like blog posts, articles, about pages, etc.

### Landing Pages
Marketing pages designed for campaigns, often with custom layouts.

### System Pages
Special pages like login, 404 error, maintenance pages.

### Application Pages
Pages that contain application functionality, like dashboards or tools.

## Widget Types

### Text
Simple text content with optional formatting.

### HTML
Rich HTML content for maximum flexibility.

### Image
Image display with caption and alt text.

### Video
Video embed with player configuration.

### Form
Interactive forms for data collection.

### Navigation
Dynamic navigation menus.

### Search
Search functionality for site content.

### Custom
Extensible widget type for custom implementations.

## Multi-Tenant Features

### Organization Scoping
- Content can be scoped to specific organizations
- Global templates available to all organizations
- Tenant isolation ensures data security

### Permissions
- Organization-level access control
- Role-based permissions for content editing
- Public/private page visibility

### Customization
- Organization-specific master pages and layouts
- Custom widget templates per organization
- Branded content for each tenant

## Best Practices

### Master Pages
1. Keep master pages minimal and focused on structure
2. Use content placeholders for flexibility
3. Include common CSS/JS references
4. Create different masters for distinct user experiences

### Page Layouts
1. Design layouts with reusability in mind
2. Define clear content zones with specific purposes
3. Use custom fields for structured content
4. Document layout usage and guidelines

### Pages
1. Use descriptive, SEO-friendly slugs
2. Always set meta descriptions and titles
3. Organize pages in hierarchies for better navigation
4. Use draft status for work-in-progress content

### Widgets
1. Keep widgets focused and single-purpose
2. Use widget templates for repeated patterns
3. Order widgets logically within zones
4. Set appropriate access controls

### Performance
1. Minimize CSS/JS references on master pages
2. Use caching for published pages
3. Lazy-load widget content when appropriate
4. Optimize images and media

## Extension Points

### Custom Widget Types
Create custom widget types by extending the Widget model and implementing custom rendering logic.

### Custom Field Types
Define custom field types for page layouts to capture structured data specific to your use case.

### Workflow Integration
Add approval workflows for page publishing in enterprise scenarios.

### Version Control
Implement detailed version history and rollback capabilities using the PageVersion model.

### Search Integration
Index page content for full-text search capabilities.

### Analytics
Track page views, engagement, and conversion metrics.

## Security Considerations

1. **Access Control**: Implement proper authentication and authorization
2. **Input Validation**: Sanitize all user input, especially HTML widgets
3. **SQL Injection**: Use parameterized queries with database integration
4. **XSS Prevention**: Escape output in templates
5. **CSRF Protection**: Implement CSRF tokens for state-changing operations
6. **Rate Limiting**: Protect API endpoints from abuse
7. **Content Security Policy**: Configure CSP headers appropriately

## Future Enhancements

- [ ] Database persistence (currently in-memory)
- [ ] Real-time collaborative editing
- [ ] Page analytics and insights
- [ ] A/B testing for layouts and content
- [ ] Content scheduling and expiration
- [ ] Workflow and approval processes
- [ ] Media library management
- [ ] Multi-language support
- [ ] SEO optimization tools
- [ ] Performance caching layer

## Support

For questions and issues related to the CMS system, please:
1. Review this documentation
2. Check the test files for usage examples
3. Open an issue on GitHub with detailed information
