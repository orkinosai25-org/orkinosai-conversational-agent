# Architecture Overview

This document describes the architecture and design of the Orkinosai Conversational Agent.

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
