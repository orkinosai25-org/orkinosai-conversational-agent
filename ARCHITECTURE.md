# Architecture Overview

This document describes the architecture and design of SiteChat Agent.

## Domain Partitioning: CMS vs Agent

This project is architecturally partitioned into two distinct domains to facilitate code reusability and maintainability between SiteChat Agent and the main sitechatcms project.

### Domain Separation Strategy

```
┌─────────────────────────────────────────────────────────────────────┐
│              SiteChat Agent Project                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────────┐  ┌────────────────────────────────┐│
│  │      CMS DOMAIN            │  │      AGENT DOMAIN              ││
│  │   (Reusable/Shared)        │  │    (Agent-Specific)            ││
│  ├────────────────────────────┤  ├────────────────────────────────┤│
│  │                            │  │                                ││
│  │ • User Management          │  │ • Chat UI                      ││
│  │ • Role Management          │  │ • Agent Configuration          ││
│  │ • Organization Management  │  │ • Azure/OpenAI Integration     ││
│  │ • Subscription/Billing     │  │ • Conversational Training      ││
│  │ • Document Management      │  │ • Feedback Loop                ││
│  │ • Admin APIs               │  │ • Session/Context Management   ││
│  │ • Multi-tenant Support     │  │ • Conversation History         ││
│  │ • CRUD Operations          │  │ • AI Model Configuration       ││
│  │ • Audit Logging            │  │ • Prompt Engineering           ││
│  │ • Settings Management      │  │ • Token Usage Tracking         ││
│  │ • Onboarding Workflows     │  │                                ││
│  │ • Data Synchronization     │  │                                ││
│  │                            │  │                                ││
│  └────────────────────────────┘  └────────────────────────────────┘│
│            ▲                                     │                   │
│            │                                     │                   │
│            │ Copy/Sync Features                  │                   │
│            │                                     │                   │
└────────────┼─────────────────────────────────────┼───────────────────┘
             │                                     │
             ▼                                     ▼
    ┌─────────────────┐                  ┌──────────────────┐
    │  sitechatcms     │                  │  Agent-Specific  │
    │  Main Project   │                  │   Features Only  │
    └─────────────────┘                  └──────────────────┘
```

### CMS Domain

**Purpose**: Generic, reusable features that should be synchronized back to the main sitechatcms project.

**Current State**: Not yet implemented in this project. These features must be copied from sitechatcms first.

**Planned Components**:
- **User Management**: User registration, authentication, profile management
- **Role & Permission Management**: RBAC (Role-Based Access Control) system
- **Organization Management**: Multi-tenant organization structure
- **Subscription & Billing**: Payment processing, subscription tiers, usage tracking
- **Generic Document Management**: File upload, storage, retrieval (non-AI-specific)
- **Admin APIs**: Administrative CRUD operations, system configuration
- **Audit Logging**: System-wide audit trail for compliance
- **Settings Management**: Application-wide configuration interface
- **Onboarding Workflows**: User and organization onboarding processes
- **Data Synchronization**: Cross-system data sync capabilities

**Location**: When implemented, these will be in:
- `src/cms/` - Core CMS functionality
- `src/cms/users/` - User management
- `src/cms/roles/` - Role and permission management
- `src/cms/organizations/` - Organization/tenant management
- `src/cms/billing/` - Subscription and billing
- `src/cms/documents/` - Generic document management
- `src/cms/admin/` - Admin APIs and interfaces
- `src/cms/audit/` - Audit logging
- `src/cms/settings/` - Settings management

**Development Rules**:
1. **Copy First**: All CMS features must be copied from sitechatcms before starting agent-specific development
2. **Keep Generic**: CMS code must remain generic and not contain agent-specific logic
3. **Sync Back**: Any modifications to CMS features must be synchronized back to sitechatcms
4. **Test Independently**: CMS features should have tests that don't depend on agent features
5. **Document Changes**: All CMS changes must be documented for sync purposes

### Agent Domain

**Purpose**: Features unique to the conversational agent that are not shared with the CMS.

**Current State**: Currently implemented core agent functionality.

**Implemented Components**:
- **Conversation Management** (`src/agent/conversation.py`):
  - Session tracking and history
  - Message state management
  - Conversation lifecycle
  
- **Azure AI Integration** (`src/agent/azure_client.py`):
  - Azure OpenAI Service client wrapper
  - API request/response handling
  - Authentication and error handling
  
- **Chat API** (`src/api/app.py`):
  - RESTful endpoints for chat interactions
  - Conversation CRUD operations
  - Real-time chat capabilities
  
- **Agent Configuration** (`src/config/settings.py`, `config.yaml`):
  - AI model parameters (temperature, max_tokens)
  - System prompts
  - Azure service configuration
  - Conversation history limits

**Planned Components**:
- **Chat UI**: Frontend interface for conversations (not yet implemented)
- **Conversational Training**: Custom training data management
- **Feedback Loop**: User feedback collection and model improvement
- **Advanced Context Management**: Multi-turn context handling
- **Prompt Engineering Tools**: Prompt template management
- **Token Usage Analytics**: Cost tracking and optimization

**Location**: Currently in:
- `src/agent/` - Core agent logic
- `src/api/app.py` - Agent-specific API endpoints
- `src/config/settings.py` - Agent configuration (contains some generic config that may move to CMS)

**Development Rules**:
1. **Agent-Specific Only**: This code should only contain features unique to conversational AI
2. **No Generic Logic**: Avoid implementing generic features that belong in CMS domain
3. **Depend on CMS**: Agent features can depend on CMS features, but not vice versa
4. **Independent Testing**: Agent tests should be separate from CMS tests

### Current Project Status

**Phase**: Early Development - Agent Core Only

The current implementation includes only the **Agent Domain** core functionality:
- ✅ Basic conversation management
- ✅ Azure OpenAI integration
- ✅ RESTful API for chat
- ✅ Configuration management (partially generic)
- ❌ CMS domain features (not yet implemented)
- ❌ Advanced agent features (planned)

### Development Workflow

#### For CMS Features (Must Follow This Process)

1. **Initial Copy**: 
   ```bash
   # Copy CMS features from sitechatcms
   # Ensure no agent-specific code is included
   git clone https://github.com/orkinosai25-org/sitechatcms.git ../sitechatcms
   cp -r ../sitechatcms/src/cms ./src/
   ```

2. **Adaptation**:
   - Adapt imports and dependencies
   - Ensure compatibility with agent project structure
   - Maintain generic nature of code

3. **Development**:
   - Make changes only when necessary for integration
   - Keep changes minimal and well-documented
   - Test independently from agent features

4. **Synchronization Back**:
   - Document all changes made
   - Create sync PR to sitechatcms
   - Update both projects to maintain consistency

#### For Agent Features

1. **Check Domain**: Ensure feature truly belongs to Agent domain
2. **Implement Independently**: Develop without modifying CMS code
3. **Use CMS APIs**: Interact with CMS features through defined interfaces
4. **Test Separately**: Create agent-specific tests

### Architecture Decision Records

**ADR-001: Domain Separation**
- **Decision**: Partition project into CMS and Agent domains
- **Rationale**: Enable code reuse with sitechatcms while maintaining agent-specific features
- **Consequences**: 
  - Easier maintenance and synchronization
  - Clear separation of concerns
  - Potential duplication during sync delays

**ADR-002: CMS Features as Foundation**
- **Decision**: Copy all CMS features first, then develop agent features
- **Rationale**: Ensures proper foundation before adding specialized functionality
- **Consequences**:
  - Delayed agent feature development
  - Better architecture and code organization
  - Reduced technical debt

**ADR-003: One-Way Dependency**
- **Decision**: Agent domain can depend on CMS domain, but not vice versa
- **Rationale**: Maintains CMS reusability across projects
- **Consequences**:
  - CMS remains generic and reusable
  - Agent features build on solid foundation
  - May require refactoring if dependencies become complex

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Client Layer                         │
│  (HTTP Clients, Web Apps, Mobile Apps, CLI Tools)          │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       API Layer (Flask)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐   │
│  │  Health  │  │   Chat   │  │Conversation│  │ Other   │   │
│  │  Check   │  │ Endpoint │  │ Management │  │Endpoints│   │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          Conversation Manager                        │   │
│  │  - Session Management                                │   │
│  │  - History Tracking                                  │   │
│  │  - Message Routing                                   │   │
│  └───────────────────────┬─────────────────────────────┘   │
│                          │                                   │
│  ┌───────────────────────▼─────────────────────────────┐   │
│  │          Azure AI Client                             │   │
│  │  - OpenAI API Integration                            │   │
│  │  - Request/Response Handling                         │   │
│  │  - Error Handling & Retry Logic                      │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Configuration Layer                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Settings Manager                                     │  │
│  │  - YAML Configuration                                 │  │
│  │  - Environment Variables                              │  │
│  │  - Type Validation (Pydantic)                         │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │ Azure OpenAI │  │Azure AI Search│  │Azure Cognitive  │ │
│  │   Service    │  │  (Optional)   │  │Services(Optional│ │
│  └──────────────┘  └───────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### API Layer (`src/api/`)

**Purpose**: Provides RESTful HTTP endpoints for client interaction

**Components**:
- `app.py`: Flask application with route definitions
  - `/health`: Health check endpoint
  - `/chat`: Main conversational endpoint
  - `/conversations/<id>`: Conversation management
  - Error handlers for 404, 500, etc.

**Responsibilities**:
- Request validation
- Response formatting
- HTTP error handling
- CORS configuration
- Logging

### Business Logic Layer (`src/agent/`)

**Purpose**: Core conversational AI logic

**Components**:

1. **ConversationManager** (`conversation.py`)
   - Manages multiple conversation sessions
   - Tracks conversation history
   - Enforces history limits
   - Routes messages to Azure AI client
   
2. **AzureAIClient** (`azure_client.py`)
   - Wraps Azure OpenAI SDK
   - Handles API authentication
   - Manages request/response lifecycle
   - Implements error handling

3. **Conversation** (`conversation.py`)
   - Represents individual conversation session
   - Stores messages with roles (user, assistant, system)
   - Provides message filtering by history limit

### Configuration Layer (`src/config/`)

**Purpose**: Centralized configuration management

**Components**:

1. **Settings** (`settings.py`)
   - Pydantic models for type-safe configuration
   - YAML file parsing
   - Environment variable substitution
   - Validation rules

2. **Configuration Models**:
   - `AzureConfig`: Azure service credentials and endpoints
   - `AgentConfig`: AI model parameters (temperature, max_tokens, etc.)
   - `ServerConfig`: API server settings
   - `LoggingConfig`: Logging configuration

### Data Flow

1. **Client Request** → API Layer
2. **API Layer** validates request → forwards to ConversationManager
3. **ConversationManager** retrieves/creates conversation → adds user message
4. **ConversationManager** calls AzureAIClient with message history
5. **AzureAIClient** sends request → Azure OpenAI Service
6. **Azure OpenAI** returns completion → AzureAIClient
7. **AzureAIClient** formats response → ConversationManager
8. **ConversationManager** updates conversation history → returns response
9. **API Layer** formats as JSON → Client

## Design Patterns

### Singleton Pattern
- `get_settings()` uses singleton with thread-safe lazy initialization
- Ensures single configuration instance across application

### Factory Pattern
- `create_app()` factory function creates Flask application
- Allows multiple app instances for testing

### Repository Pattern
- `ConversationManager` acts as repository for conversation sessions
- Abstracts conversation storage and retrieval

### Adapter Pattern
- `AzureAIClient` adapts Azure OpenAI SDK to application's interface
- Provides consistent interface regardless of underlying SDK changes

## Security Considerations

### Credential Management
- Credentials stored in environment variables
- Never committed to source control
- `.env.example` provides template without real values

### API Security
- CORS configured for specific origins
- Rate limiting recommended for production (not implemented)
- Authentication/authorization recommended for production (not implemented)

### Input Validation
- Pydantic validates all configuration
- Request validation in API layer
- SQL injection not applicable (no database)

### Thread Safety
- Settings singleton uses double-check locking
- Conversation manager uses thread-safe dictionary
- Flask handles concurrent requests

## Scalability

### Horizontal Scaling
- Stateless API design
- Conversation state in memory (consider Redis/database for production)
- Azure OpenAI handles backend scaling

### Vertical Scaling
- Configurable worker processes (Gunicorn recommended)
- Async support possible with async Flask

### Bottlenecks
- Azure OpenAI rate limits (tokens per minute)
- Memory usage for conversation history (mitigated by history limit)
- Single-process conversation storage (use external store for multi-instance)

## Future Enhancements

1. **Persistent Storage**
   - Database for conversation history
   - Redis for session caching

2. **Authentication**
   - JWT tokens
   - API keys
   - OAuth integration

3. **Advanced Features**
   - Streaming responses
   - Function calling
   - RAG with Azure AI Search
   - Multi-modal support (images, documents)

4. **Monitoring**
   - Application Insights integration
   - Custom metrics
   - Performance tracking

5. **Rate Limiting**
   - Per-user rate limits
   - Token budget management
   - Queue-based request handling

## Technology Stack

- **Language**: Python 3.8+
- **Web Framework**: Flask
- **Azure SDK**: azure-ai-inference, azure-identity, azure-core
- **OpenAI SDK**: openai
- **Configuration**: PyYAML, python-dotenv, Pydantic
- **Testing**: pytest, pytest-cov
- **Containerization**: Docker, Docker Compose

## Development Workflow

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Configure `.env` file
5. Run tests: `pytest tests/`
6. Start server: `python main.py`
7. Test API: `python examples/simple_chat.py`

## Deployment Options

- **Azure App Service**: Recommended for web apps
- **Azure Container Apps**: For containerized deployments
- **Azure Functions**: For serverless/event-driven
- **Docker**: For any container platform

See `docs/AZURE_DEPLOYMENT.md` for detailed deployment instructions.

## CMS-Agent Synchronization Guidelines

### Overview

This section provides detailed guidelines for maintaining synchronization between the SiteChat Agent and the main sitechatcms project for CMS domain features.

### Synchronization Principles

1. **CMS is the Source of Truth**: sitechatcms is the authoritative source for all CMS domain features
2. **Unidirectional Flow**: Features flow from CMS → Agent, improvements flow back CMS ← Agent
3. **Regular Sync Cycles**: Establish regular sync windows (e.g., weekly, bi-weekly)
4. **Change Documentation**: All CMS modifications must be documented for sync purposes

### Synchronization Process

#### Phase 1: Initial CMS Integration (Not Yet Started)

**Step 1: Feature Inventory**
```bash
# Create a list of CMS features to be copied
# Document in docs/CMS_FEATURES_INVENTORY.md
```

Features to Copy:
- User management system
- Role and permission management
- Organization/multi-tenant infrastructure
- Subscription and billing system
- Generic document management
- Admin APIs and dashboards
- Audit logging system
- Settings management
- Onboarding workflows

**Step 2: Copy CMS Features**
```bash
# Clone sitechatcms
git clone https://github.com/orkinosai25-org/sitechatcms.git ../sitechatcms

# Create CMS directory structure
mkdir -p src/cms

# Copy core CMS modules (example - actual structure may vary)
cp -r ../sitechatcms/src/users src/cms/
cp -r ../sitechatcms/src/roles src/cms/
cp -r ../sitechatcms/src/organizations src/cms/
cp -r ../sitechatcms/src/billing src/cms/
# ... continue for all CMS features
```

**Step 3: Adapt for Agent Project**
- Update import paths
- Integrate with agent configuration
- Ensure compatibility with agent's tech stack
- Add integration tests

**Step 4: Document Sync Points**
```bash
# Create sync tracking file
touch docs/CMS_SYNC_LOG.md
```

Document:
- Date of copy
- Commit hash from sitechatcms
- Features copied
- Modifications made
- Integration notes

#### Phase 2: Ongoing Synchronization

**When to Sync from sitechatcms → Agent**

Sync when:
- New CMS features are released
- Security patches are applied to CMS
- Bug fixes in CMS domain code
- Performance improvements in CMS features

**Process**:
```bash
# 1. Check for updates in sitechatcms
cd ../sitechatcms
git pull origin main
git log --oneline --since="last-sync-date"

# 2. Review changes relevant to copied features
git diff last-sync-commit..HEAD -- src/users src/roles src/organizations

# 3. Cherry-pick or manually apply relevant changes
cd ../sitechat-agent
# Apply changes to src/cms/

# 4. Test integration
pytest tests/cms/

# 5. Update sync log
# Add entry to docs/CMS_SYNC_LOG.md
```

**When to Sync from Agent → sitechatcms**

Sync back when:
- Bug fixes discovered in CMS code while using in agent
- Performance optimizations made to CMS features
- Feature enhancements that benefit all projects
- Security improvements

**Process**:
```bash
# 1. Identify CMS changes in agent project
git log --oneline -- src/cms/

# 2. Extract generic changes (remove agent-specific code)
git diff base-commit..HEAD -- src/cms/ > cms-changes.patch

# 3. Review and clean patch
# Remove any agent-specific modifications
# Ensure changes are generic and reusable

# 4. Create PR in sitechatcms
cd ../sitechatcms
git checkout -b feature/agent-improvements
# Apply cleaned changes
git apply ../sitechat-agent/cms-changes.patch

# 5. Submit PR with clear documentation
# Include: what changed, why, and benefits
```

### Directory Structure After CMS Integration

```
sitechat-agent/
├── src/
│   ├── cms/                      # CMS DOMAIN (copied from sitechatcms)
│   │   ├── __init__.py
│   │   ├── users/               # User management
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   ├── api.py
│   │   │   └── tests/
│   │   ├── roles/               # Role & permission management
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── tests/
│   │   ├── organizations/       # Multi-tenant management
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── tests/
│   │   ├── billing/             # Subscription & billing
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── tests/
│   │   ├── documents/           # Generic document management
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── tests/
│   │   ├── admin/               # Admin APIs
│   │   │   ├── api.py
│   │   │   └── tests/
│   │   ├── audit/               # Audit logging
│   │   │   ├── models.py
│   │   │   ├── services.py
│   │   │   └── tests/
│   │   └── settings/            # Settings management
│   │       ├── models.py
│   │       ├── services.py
│   │       └── tests/
│   │
│   ├── agent/                   # AGENT DOMAIN (unique to this project)
│   │   ├── __init__.py
│   │   ├── azure_client.py     # Azure OpenAI integration
│   │   ├── conversation.py     # Conversation management
│   │   ├── training.py         # (Future) Conversational training
│   │   └── feedback.py         # (Future) Feedback loop
│   │
│   ├── api/                     # API Layer (mix of CMS & Agent endpoints)
│   │   ├── __init__.py
│   │   ├── app.py              # Main Flask app
│   │   ├── cms_routes.py       # (Future) CMS API routes
│   │   └── agent_routes.py     # (Future) Agent API routes
│   │
│   └── config/                  # Configuration (partially CMS, partially Agent)
│       ├── __init__.py
│       └── settings.py
│
├── tests/
│   ├── cms/                     # CMS domain tests
│   │   ├── test_users.py
│   │   ├── test_roles.py
│   │   └── ...
│   └── agent/                   # Agent domain tests
│       ├── test_conversation.py
│       ├── test_azure_client.py
│       └── ...
│
├── docs/
│   ├── CMS_FEATURES_INVENTORY.md    # (Future) List of CMS features
│   ├── CMS_SYNC_LOG.md              # (Future) Sync history
│   └── DOMAIN_INTEGRATION.md        # (Future) Integration guide
│
└── ARCHITECTURE.md              # This file
```

### Code Organization Best Practices

#### 1. Clear Module Boundaries

```python
# ✅ GOOD - Clear separation
from src.cms.users import UserService
from src.agent.conversation import ConversationManager

# ❌ BAD - Mixed concerns
from src.services import UserService, ConversationManager
```

#### 2. One-Way Dependencies

```python
# ✅ GOOD - Agent depends on CMS
# src/agent/conversation.py
from src.cms.users import get_current_user

class ConversationManager:
    def chat(self, user_id: str, message: str):
        user = get_current_user(user_id)  # OK - Agent using CMS
        # ...

# ❌ BAD - CMS depends on Agent
# src/cms/users/models.py
from src.agent.conversation import ConversationManager  # WRONG!
```

#### 3. Generic vs. Specific Code

```python
# ✅ GOOD - Generic CMS code
# src/cms/documents/services.py
class DocumentService:
    def upload(self, file, user_id: str):
        """Generic document upload - works for any file type"""
        # Generic validation, storage, etc.

# ✅ GOOD - Agent-specific extension
# src/agent/training_data.py
from src.cms.documents import DocumentService

class TrainingDataService:
    def __init__(self):
        self.doc_service = DocumentService()
    
    def upload_training_document(self, file, user_id: str):
        """Agent-specific: validates AI training data format"""
        # Agent-specific validation
        return self.doc_service.upload(file, user_id)
```

#### 4. Configuration Separation

```yaml
# config.yaml - Clear domain sections

# CMS Configuration (generic, syncable)
cms:
  database:
    url: "${DATABASE_URL}"
  auth:
    jwt_secret: "${JWT_SECRET}"
    token_expiry: 3600
  multi_tenant:
    enabled: true

# Agent Configuration (agent-specific)
agent:
  name: "SiteChat Agent"
  azure:
    openai:
      endpoint: "${AZURE_OPENAI_ENDPOINT}"
      deployment: "${AZURE_OPENAI_DEPLOYMENT_NAME}"
  max_history: 10
  temperature: 0.7
```

### Migration Checklist

Before declaring CMS integration complete, verify:

- [ ] All CMS features copied from sitechatcms
- [ ] CMS tests adapted and passing
- [ ] CMS code remains generic (no agent-specific logic)
- [ ] Agent code uses CMS features through defined interfaces
- [ ] Documentation updated (sync log, feature inventory)
- [ ] Integration tests created for CMS-Agent interaction
- [ ] Sync process documented and tested
- [ ] Team trained on domain separation principles

### Continuous Integration Considerations

```yaml
# .github/workflows/cms-sync-check.yml (example)
name: CMS Sync Check

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly check
  workflow_dispatch:

jobs:
  check-sync:
    runs-on: ubuntu-latest
    steps:
      - name: Check for CMS updates
        run: |
          # Clone both repos
          # Compare src/cms with sitechatcms source
          # Report drift if found
          
      - name: Create sync reminder issue
        if: ${{ steps.check.outputs.drift == 'true' }}
        # Create GitHub issue reminding team to sync
```

### Contact and Sync Coordination

- **CMS Sync Lead**: [To be assigned]
- **Sync Schedule**: [To be determined - suggest bi-weekly]
- **Sync Meetings**: [To be scheduled]
- **Slack Channel**: #cms-agent-sync (or equivalent)

### References

- Main CMS Repository: https://github.com/orkinosai25-org/sitechatcms
- Agent Repository: https://github.com/orkinosai25-org/sitechat-agent
- Sync Log: `docs/CMS_SYNC_LOG.md` (to be created)
- Feature Inventory: `docs/CMS_FEATURES_INVENTORY.md` (to be created)
