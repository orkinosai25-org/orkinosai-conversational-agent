# CMS Features Inventory

## Overview

This document tracks all CMS domain features that should be copied from the main papagancms project. These features are generic, reusable components that support multi-tenant, subscription-based applications.

## Status: NOT YET IMPLEMENTED

⚠️ **Important**: All CMS features must be copied from papagancms before continuing with agent-specific development.

## Features to be Copied from papagancms

### 1. User Management
**Priority**: High  
**Status**: Not Copied  
**Description**: Complete user lifecycle management system

**Components**:
- [ ] User registration and authentication
- [ ] Password management (reset, change)
- [ ] User profile management
- [ ] Email verification
- [ ] User status management (active, inactive, suspended)
- [ ] User preferences and settings

**Files to Copy**:
- `src/users/models.py` - User data models
- `src/users/services.py` - Business logic
- `src/users/api.py` - API endpoints
- `src/users/tests/` - Test suite

**Dependencies**: Database, Auth system

---

### 2. Role & Permission Management
**Priority**: High  
**Status**: Not Copied  
**Description**: RBAC (Role-Based Access Control) system

**Components**:
- [ ] Role definitions and management
- [ ] Permission assignment
- [ ] Role hierarchy
- [ ] Permission checking middleware
- [ ] Admin role management UI

**Files to Copy**:
- `src/roles/models.py`
- `src/roles/services.py`
- `src/roles/permissions.py`
- `src/roles/decorators.py`
- `src/roles/tests/`

**Dependencies**: User Management

---

### 3. Organization Management
**Priority**: High  
**Status**: Not Copied  
**Description**: Multi-tenant organization infrastructure

**Components**:
- [ ] Organization creation and management
- [ ] User-to-organization association
- [ ] Organization settings and preferences
- [ ] Tenant isolation
- [ ] Organization-level permissions
- [ ] Organization hierarchy (parent/child orgs)

**Files to Copy**:
- `src/organizations/models.py`
- `src/organizations/services.py`
- `src/organizations/api.py`
- `src/organizations/tests/`

**Dependencies**: User Management, Role Management

---

### 4. Subscription & Billing
**Priority**: High  
**Status**: Not Copied  
**Description**: Subscription tiers and payment processing

**Components**:
- [ ] Subscription tier definitions
- [ ] Payment processing integration
- [ ] Usage tracking
- [ ] Billing cycle management
- [ ] Invoice generation
- [ ] Payment method management
- [ ] Subscription upgrade/downgrade

**Files to Copy**:
- `src/billing/models.py`
- `src/billing/services.py`
- `src/billing/api.py`
- `src/billing/stripe_integration.py` (or other payment processor)
- `src/billing/tests/`

**Dependencies**: Organization Management

---

### 5. Generic Document Management
**Priority**: Medium  
**Status**: Not Copied  
**Description**: File upload, storage, and retrieval (non-AI-specific)

**Components**:
- [ ] File upload API
- [ ] Cloud storage integration (Azure Blob, S3, etc.)
- [ ] File metadata management
- [ ] File access control
- [ ] File versioning
- [ ] File preview generation
- [ ] Bulk operations

**Files to Copy**:
- `src/documents/models.py`
- `src/documents/services.py`
- `src/documents/storage.py`
- `src/documents/api.py`
- `src/documents/tests/`

**Dependencies**: User Management, Organization Management

---

### 6. Admin APIs
**Priority**: Medium  
**Status**: Not Copied  
**Description**: Administrative CRUD operations and system management

**Components**:
- [ ] Admin dashboard endpoints
- [ ] System configuration API
- [ ] Bulk user operations
- [ ] Data export/import
- [ ] System health monitoring
- [ ] Admin notification system

**Files to Copy**:
- `src/admin/api.py`
- `src/admin/services.py`
- `src/admin/middleware.py`
- `src/admin/tests/`

**Dependencies**: User Management, Role Management

---

### 7. Audit Logging
**Priority**: Medium  
**Status**: Not Copied  
**Description**: System-wide audit trail for compliance

**Components**:
- [ ] Audit event capture
- [ ] Audit log storage
- [ ] Audit log query API
- [ ] Audit report generation
- [ ] Data retention policies
- [ ] Compliance reporting

**Files to Copy**:
- `src/audit/models.py`
- `src/audit/services.py`
- `src/audit/decorators.py`
- `src/audit/api.py`
- `src/audit/tests/`

**Dependencies**: User Management

---

### 8. Settings Management
**Priority**: Medium  
**Status**: Not Copied  
**Description**: Application-wide and user-specific settings

**Components**:
- [ ] System settings (global configuration)
- [ ] User settings (preferences)
- [ ] Organization settings
- [ ] Settings validation
- [ ] Settings versioning
- [ ] Settings import/export

**Files to Copy**:
- `src/settings/models.py`
- `src/settings/services.py`
- `src/settings/api.py`
- `src/settings/tests/`

**Dependencies**: User Management, Organization Management

---

### 9. Onboarding Workflows
**Priority**: Low  
**Status**: Not Copied  
**Description**: User and organization onboarding automation

**Components**:
- [ ] Onboarding step definitions
- [ ] Progress tracking
- [ ] Welcome emails and notifications
- [ ] Setup wizard API
- [ ] Tutorial system
- [ ] Onboarding analytics

**Files to Copy**:
- `src/onboarding/models.py`
- `src/onboarding/services.py`
- `src/onboarding/workflows.py`
- `src/onboarding/api.py`
- `src/onboarding/tests/`

**Dependencies**: User Management, Organization Management

---

### 10. Data Synchronization
**Priority**: Low  
**Status**: Not Copied  
**Description**: Cross-system data sync capabilities

**Components**:
- [ ] Sync job scheduling
- [ ] Data conflict resolution
- [ ] Sync status monitoring
- [ ] Delta sync support
- [ ] Sync webhooks
- [ ] Sync API endpoints

**Files to Copy**:
- `src/sync/models.py`
- `src/sync/services.py`
- `src/sync/scheduler.py`
- `src/sync/api.py`
- `src/sync/tests/`

**Dependencies**: Multiple (various entities that need syncing)

---

## Copy Checklist

Before copying each feature:
- [ ] Review papagancms source code
- [ ] Identify all dependencies
- [ ] Check for breaking changes
- [ ] Plan integration strategy
- [ ] Prepare test environment

After copying each feature:
- [ ] Update imports for new project structure
- [ ] Adapt configuration
- [ ] Run and fix tests
- [ ] Update documentation
- [ ] Log sync details in CMS_SYNC_LOG.md

---

## Integration Priority Order

Recommended order of implementation (respecting dependencies):

1. **Phase 1 - Foundation** (High Priority)
   - User Management
   - Role & Permission Management
   - Organization Management

2. **Phase 2 - Business Features** (High Priority)
   - Subscription & Billing
   - Generic Document Management

3. **Phase 3 - Administration** (Medium Priority)
   - Admin APIs
   - Audit Logging
   - Settings Management

4. **Phase 4 - Enhancement** (Low Priority)
   - Onboarding Workflows
   - Data Synchronization

---

## Notes

- All copied code must remain generic (no agent-specific logic)
- Tests must be adapted but should maintain coverage
- Database migrations need careful review
- Configuration must be compatible with agent project
- Keep track of any modifications in CMS_SYNC_LOG.md

---

## References

- Main CMS Repository: https://github.com/orkinosai25-org/papagancms
- Architecture Documentation: [ARCHITECTURE.md](../ARCHITECTURE.md)
- Sync Log: [CMS_SYNC_LOG.md](./CMS_SYNC_LOG.md)
