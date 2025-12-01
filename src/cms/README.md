# CMS Domain

This directory contains generic, reusable CMS features that are synchronized with the main [orkinosaicms](https://github.com/orkinosai25-org/orkinosaicms) project.

## Status: Initial Structure Created

⚠️ **Important**: This is currently a placeholder structure. Full implementations will be copied from orkinosaicms when available.

## Purpose

The CMS domain provides foundational features for a multi-tenant SaaS application including:
- User management and authentication
- Role-based access control (RBAC)
- Organization/tenant management
- Subscription and billing
- Document management
- Administrative operations
- Audit logging
- Settings management
- Onboarding workflows
- Data synchronization

## Architecture

All code in this domain must remain **generic and agent-agnostic**. No AI or conversational agent-specific logic should be added here.

### Dependency Rule
- ✅ Agent features CAN depend on CMS features
- ❌ CMS features CANNOT depend on Agent features

## Directory Structure

```
cms/
├── __init__.py              # Package initialization
├── base.py                  # Base classes and utilities
├── README.md                # This file
│
├── users/                   # User Management
│   ├── __init__.py
│   ├── models.py           # User, UserProfile, UserStatus
│   ├── services.py         # UserService
│   └── tests/
│
├── roles/                   # Role & Permission Management
│   ├── __init__.py
│   ├── models.py           # Role, Permission, RolePermission
│   ├── services.py         # RoleService, PermissionService
│   └── tests/
│
├── organizations/           # Organization/Tenant Management
│   ├── __init__.py
│   ├── models.py           # Organization, OrganizationMember
│   ├── services.py         # OrganizationService
│   └── tests/
│
├── billing/                 # Subscription & Billing
│   ├── __init__.py
│   ├── models.py           # Subscription, SubscriptionTier, Invoice
│   ├── services.py         # BillingService, SubscriptionService
│   └── tests/
│
├── documents/               # Document Management
│   ├── __init__.py
│   ├── models.py           # Document, DocumentVersion
│   ├── services.py         # DocumentService
│   └── tests/
│
├── admin/                   # Admin APIs
│   ├── __init__.py
│   ├── services.py         # AdminService
│   └── tests/
│
├── audit/                   # Audit Logging
│   ├── __init__.py
│   ├── models.py           # AuditLog
│   ├── services.py         # AuditService
│   └── tests/
│
├── settings/                # Settings Management
│   ├── __init__.py
│   ├── models.py           # Setting
│   ├── services.py         # SettingsService
│   └── tests/
│
├── onboarding/              # Onboarding Workflows
│   ├── __init__.py
│   ├── models.py           # OnboardingStep
│   ├── services.py         # OnboardingService
│   └── tests/
│
└── sync/                    # Data Synchronization
    ├── __init__.py
    ├── models.py           # SyncJob
    ├── services.py         # SyncService
    └── tests/
```

## Base Classes

### BaseEntity
Base model for all CMS entities with common fields:
- `id`, `created_at`, `updated_at`
- `created_by`, `updated_by`
- `is_active`, `metadata`

### ServiceResponse
Standard response wrapper for service operations with:
- `success`, `message`, `data`, `errors`

### Exceptions
- `CMSException` - Base exception
- `ValidationException` - Validation failures
- `NotFoundException` - Entity not found
- `PermissionDeniedException` - Access denied
- `DuplicateException` - Duplicate entry

## Current Status

All modules have been created with:
- ✅ Directory structure
- ✅ Model definitions (Pydantic)
- ✅ Service stubs (raise NotImplementedError)
- ✅ Package initialization
- ⏳ Actual implementations (awaiting copy from orkinosaicms)
- ⏳ Database integration
- ⏳ API endpoints
- ⏳ Comprehensive tests

## Usage Example

```python
# When fully implemented, usage will look like:
from src.cms.users import UserService, User
from src.cms.organizations import OrganizationService

# Create services
user_service = UserService()
org_service = OrganizationService()

# Create a user
response = user_service.create_user(
    email="user@example.com",
    username="johndoe",
    password="secure_password"
)

if response.success:
    user = response.data
    print(f"Created user: {user['id']}")
```

**Note**: Currently all service methods raise `NotImplementedError`.

## Development Guidelines

1. **Keep it Generic**: No agent-specific logic in CMS code
2. **Follow Patterns**: Use BaseEntity, ServiceResponse consistently
3. **Type Safety**: Use Pydantic models for validation
4. **Document Changes**: Update sync log when modifying CMS code
5. **Test Independence**: CMS tests should not depend on agent features

## Synchronization

- **Source Repository**: https://github.com/orkinosai25-org/orkinosaicms
- **Sync Log**: See [docs/CMS_SYNC_LOG.md](../../docs/CMS_SYNC_LOG.md)
- **Feature Inventory**: See [docs/CMS_FEATURES_INVENTORY.md](../../docs/CMS_FEATURES_INVENTORY.md)
- **Architecture**: See [ARCHITECTURE.md](../../ARCHITECTURE.md)

## Next Steps

1. Wait for orkinosaicms repository to become available
2. Copy actual implementations from orkinosaicms
3. Replace NotImplementedError stubs with real functionality
4. Adapt imports and dependencies
5. Add database integration
6. Create API endpoints
7. Write comprehensive tests
8. Integrate with agent features

## Contributing

When implementing or modifying CMS features:

1. Check if feature exists in orkinosaicms first
2. Keep implementations generic
3. Update tests
4. Document in sync log
5. Ensure backward compatibility
6. Review integration points with agent features

## License

Same as parent project (MIT License)
