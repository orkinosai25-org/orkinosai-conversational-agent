# Domain Integration Guide

## Overview

This guide provides practical instructions for developers working with the CMS and Agent domains in the Orkinosai Conversational Agent project.

## Quick Reference

### Is my feature CMS or Agent domain?

Ask yourself these questions:

1. **Would this feature be useful in other applications?** → CMS Domain
2. **Is this specific to conversational AI?** → Agent Domain
3. **Does it involve generic CRUD operations?** → CMS Domain
4. **Does it involve Azure OpenAI or chat interactions?** → Agent Domain

### Examples by Domain

**CMS Domain** (Generic, Reusable):
- User authentication and authorization
- Role-based access control
- Organization management
- Subscription billing
- File upload and storage
- Admin dashboards
- Audit trails
- Email notifications (generic)

**Agent Domain** (AI-Specific):
- Chat message handling
- Conversation history
- Azure OpenAI integration
- Token usage tracking
- Prompt engineering
- Model configuration
- Training data management
- AI-specific feedback collection

---

## Development Guidelines

### For CMS Domain Development

#### 1. Before Writing Code

```python
# ❌ DON'T start from scratch
# ✅ DO check if it exists in papagancms first
```

**Process**:
1. Check `docs/CMS_FEATURES_INVENTORY.md` to see if feature is listed
2. If listed but not copied, wait for it to be copied from papagancms
3. If not listed, verify it truly belongs in CMS domain
4. If it's generic and reusable, consider adding to papagancms first

#### 2. Writing CMS Code

```python
# ❌ BAD - Agent-specific logic in CMS code
from src.agent.conversation import ConversationManager

class UserService:
    def create_user(self, user_data):
        user = User(**user_data)
        # BAD: Agent-specific logic
        ConversationManager().create_conversation(user.id)
        return user

# ✅ GOOD - Keep CMS code generic
class UserService:
    def create_user(self, user_data):
        user = User(**user_data)
        # Emit event that agent can listen to
        self.emit_event('user.created', user)
        return user
```

**Best Practices**:
- Keep code framework-agnostic where possible
- Use dependency injection for external services
- Emit events instead of direct calls to other domains
- Write comprehensive tests that don't depend on agent features

#### 3. Testing CMS Features

```python
# tests/cms/test_users.py
import pytest
from src.cms.users import UserService

class TestUserService:
    """Tests should not import agent domain code"""
    
    def test_create_user(self):
        service = UserService()
        user = service.create_user({
            "email": "test@example.com",
            "name": "Test User"
        })
        assert user.email == "test@example.com"
        # ✅ No agent-specific assertions
```

#### 4. Documentation

```python
# ✅ GOOD - Clear domain indicator
"""
CMS Domain: User Management Service

This module provides generic user management functionality
that can be reused across multiple applications.

Note: This code is synchronized with papagancms.
Any modifications must be synced back to the main CMS project.
"""
```

---

### For Agent Domain Development

#### 1. Leveraging CMS Features

```python
# ✅ GOOD - Agent uses CMS services
from src.cms.users import UserService
from src.cms.organizations import OrganizationService

class ConversationManager:
    def __init__(self):
        self.user_service = UserService()
        self.org_service = OrganizationService()
    
    def create_conversation(self, user_id: str):
        # Use CMS to verify user exists
        user = self.user_service.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Agent-specific logic
        return Conversation(user_id=user_id)
```

#### 2. Extending CMS Features

```python
# ✅ GOOD - Extend, don't modify
from src.cms.documents import DocumentService

class TrainingDataManager:
    """Agent Domain: Training Data Management
    
    Extends generic document management with AI-specific features.
    """
    def __init__(self):
        self.doc_service = DocumentService()
    
    def upload_training_data(self, file, user_id: str):
        # Agent-specific validation
        if not self._is_valid_training_format(file):
            raise ValueError("Invalid training data format")
        
        # Use CMS for storage
        return self.doc_service.upload(file, user_id, 
                                      category='training_data')
    
    def _is_valid_training_format(self, file):
        # AI-specific validation logic
        pass
```

#### 3. Agent-Specific Configuration

```yaml
# config.yaml
# ✅ GOOD - Clear separation

# CMS configuration (generic)
cms:
  database_url: "${DATABASE_URL}"
  auth:
    jwt_secret: "${JWT_SECRET}"

# Agent configuration (AI-specific)
agent:
  azure:
    openai:
      endpoint: "${AZURE_OPENAI_ENDPOINT}"
      deployment: "${AZURE_OPENAI_DEPLOYMENT}"
  conversation:
    max_history: 10
    default_temperature: 0.7
```

---

## Integration Patterns

### Pattern 1: Event-Driven Integration

```python
# CMS Domain - Emits events
class UserService:
    def __init__(self):
        self.event_bus = EventBus()
    
    def create_user(self, user_data):
        user = User(**user_data)
        self.event_bus.emit('user.created', user)
        return user

# Agent Domain - Listens to events
class ConversationSetup:
    def __init__(self):
        self.event_bus = EventBus()
        self.event_bus.on('user.created', self.on_user_created)
    
    def on_user_created(self, user):
        # Create default conversation for new user
        self.create_default_conversation(user.id)
```

### Pattern 2: Service Layer Integration

```python
# Agent Domain
class AgentService:
    """High-level agent service that coordinates CMS and Agent features"""
    
    def __init__(self):
        # CMS services
        self.user_service = UserService()
        self.org_service = OrganizationService()
        
        # Agent services
        self.conversation_manager = ConversationManager()
        self.azure_client = AzureAIClient()
    
    def start_conversation(self, user_id: str, org_id: str):
        # Validate using CMS
        user = self.user_service.get_user(user_id)
        org = self.org_service.get_organization(org_id)
        
        if not self.org_service.user_in_org(user_id, org_id):
            raise PermissionError("User not in organization")
        
        # Create conversation (agent-specific)
        return self.conversation_manager.create_conversation(user_id)
```

### Pattern 3: Adapter Pattern

```python
# Agent Domain - Adapts CMS interface for agent needs
class AgentUserAdapter:
    """Adapts CMS UserService for agent-specific needs"""
    
    def __init__(self):
        self.user_service = UserService()
    
    def get_user_with_preferences(self, user_id: str):
        user = self.user_service.get_user(user_id)
        
        # Add agent-specific data
        return {
            **user.dict(),
            'default_temperature': self._get_user_temperature(user_id),
            'preferred_model': self._get_user_model(user_id),
        }
    
    def _get_user_temperature(self, user_id: str):
        # Agent-specific logic
        pass
```

---

## API Design

### CMS API Endpoints

```python
# src/api/cms_routes.py (when implemented)
from flask import Blueprint
from src.cms.users import UserService

cms_api = Blueprint('cms', __name__, url_prefix='/api/cms')

@cms_api.route('/users', methods=['POST'])
def create_user():
    """Generic user creation - part of CMS domain"""
    # Generic implementation
    pass

@cms_api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Generic user retrieval - part of CMS domain"""
    pass
```

### Agent API Endpoints

```python
# src/api/agent_routes.py (example)
from flask import Blueprint
from src.agent.conversation import ConversationManager

agent_api = Blueprint('agent', __name__, url_prefix='/api/agent')

@agent_api.route('/chat', methods=['POST'])
def chat():
    """AI chat endpoint - part of Agent domain"""
    # Agent-specific implementation
    pass

@agent_api.route('/conversations/<id>/feedback', methods=['POST'])
def submit_feedback(id):
    """AI feedback - part of Agent domain"""
    pass
```

---

## Database Schema

### CMS Tables (Generic)

```python
# src/cms/users/models.py
class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    # Generic user fields
```

### Agent Tables (AI-Specific)

```python
# src/agent/models.py
class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey('users.id'))
    # Agent-specific fields
    azure_deployment = Column(String)
    total_tokens_used = Column(Integer)
```

---

## Testing Strategy

### CMS Tests (Independent)

```python
# tests/cms/test_users.py
"""CMS Domain tests - no agent dependencies"""

def test_user_creation():
    service = UserService()
    user = service.create_user({"email": "test@test.com"})
    assert user.email == "test@test.com"
```

### Agent Tests (May use CMS)

```python
# tests/agent/test_conversation.py
"""Agent Domain tests - can use CMS mocks"""

from unittest.mock import Mock

def test_conversation_with_user():
    # Mock CMS service
    user_service = Mock()
    user_service.get_user.return_value = User(id="123")
    
    # Test agent functionality
    conv_manager = ConversationManager(user_service)
    conv = conv_manager.create_conversation("123")
    assert conv.user_id == "123"
```

### Integration Tests

```python
# tests/integration/test_cms_agent_integration.py
"""Integration tests for CMS-Agent interaction"""

def test_user_to_conversation_flow():
    # Create user (CMS)
    user = user_service.create_user(user_data)
    
    # Create conversation (Agent)
    conv = conversation_manager.create_conversation(user.id)
    
    # Verify integration
    assert conv.user_id == user.id
```

---

## Checklist for New Features

### Before Implementation

- [ ] Determine if feature is CMS or Agent domain
- [ ] Check if similar feature exists in papagancms
- [ ] Review dependencies on other domains
- [ ] Plan integration approach

### During Implementation

- [ ] Follow domain separation guidelines
- [ ] Write domain-appropriate tests
- [ ] Document any cross-domain interactions
- [ ] Keep CMS code generic

### After Implementation

- [ ] Run all tests (CMS and Agent)
- [ ] Update relevant documentation
- [ ] If CMS feature: Plan sync back to papagancms
- [ ] Code review focusing on domain boundaries

---

## Common Pitfalls to Avoid

### ❌ Pitfall 1: Mixing Domains in One Module

```python
# BAD: cms_and_agent_service.py
class MixedService:
    def create_user_and_conversation(self, user_data):
        # Mixes CMS and Agent concerns
        user = self.create_user(user_data)  # CMS
        conv = self.create_conversation(user.id)  # Agent
        return user, conv
```

### ✅ Solution: Separate Services

```python
# GOOD: Use composition in Agent domain
class AgentOnboarding:
    def __init__(self):
        self.user_service = UserService()  # CMS
        self.conv_manager = ConversationManager()  # Agent
    
    def onboard_user(self, user_data):
        user = self.user_service.create_user(user_data)
        conv = self.conv_manager.create_conversation(user.id)
        return user, conv
```

### ❌ Pitfall 2: CMS Code Depending on Agent

```python
# BAD: In CMS domain
from src.agent.conversation import ConversationManager

class UserService:
    def delete_user(self, user_id):
        ConversationManager().delete_user_conversations(user_id)
        # Delete user...
```

### ✅ Solution: Use Events or Hooks

```python
# GOOD: CMS emits event
class UserService:
    def delete_user(self, user_id):
        self.event_bus.emit('user.deleting', user_id)
        # Delete user...

# Agent listens
class ConversationCleanup:
    def on_user_deleting(self, user_id):
        self.conv_manager.delete_user_conversations(user_id)
```

---

## Questions and Support

### When to Ask for Help

- Uncertain about domain classification
- Need to modify copied CMS code
- Planning major feature that spans domains
- Encountering sync conflicts

### Resources

- Architecture Documentation: [ARCHITECTURE.md](../ARCHITECTURE.md)
- Features Inventory: [CMS_FEATURES_INVENTORY.md](./CMS_FEATURES_INVENTORY.md)
- Sync Log: [CMS_SYNC_LOG.md](./CMS_SYNC_LOG.md)

---

## References

- Main CMS Repository: https://github.com/orkinosai25-org/papagancms
- Domain-Driven Design Principles
- Microservices Architecture Patterns
