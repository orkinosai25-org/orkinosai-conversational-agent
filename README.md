# Orkinosai Conversational Agent CMS

A comprehensive Content Management System (CMS) for managing conversational AI agents, built with FastAPI and designed for SaaS operations.

## Features

- **User Management**: Complete CRUD operations for user accounts with authentication
- **Account Management**: Multi-tenant account system with subscription tiers
- **Agent Management**: Create, manage, and configure conversational AI agents
- **Onboarding Flow**: Step-by-step onboarding process for new users
- **Training System**: Upload documents and URLs to train agents (Azure AI integration ready)
- **Azure Integration**: Placeholder configuration for Azure Blob Storage and Azure AI services
- **RESTful API**: Comprehensive API endpoints for all operations

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Initialize database
python init_db.py

# Run the application
python run.py
```

Visit http://localhost:8000/docs for API documentation.

## Documentation

- [Setup Guide](SETUP.md) - Detailed installation and configuration instructions
- [API Documentation](http://localhost:8000/docs) - Interactive API documentation (when running)

## Project Structure

```
orkinosai-conversational-agent/
├── app/
│   ├── core/           # Core configuration and utilities
│   ├── models/         # SQLAlchemy database models (User, Account, Agent)
│   ├── schemas/        # Pydantic schemas for validation
│   ├── routes/         # API route handlers
│   ├── services/       # External service integrations (Azure)
│   ├── utils/          # Utility functions
│   └── main.py         # Application entry point
├── requirements.txt    # Python dependencies
├── .env.example       # Example environment variables
└── run.py             # Application runner
```

## Key Features

### User & Account Management
- User registration and authentication with JWT tokens
- Multi-tenant account system with subscription tiers
- User onboarding flow with progress tracking

### Agent Management
- Create and manage conversational AI agents
- Agent activation/deactivation controls
- Azure AI deployment configuration

### Training System
- Train agents from URLs and documents
- Azure Blob Storage integration for document uploads
- Training status tracking and knowledge source management

### Azure Integration (Placeholder)
- Azure Blob Storage for document storage
- Azure AI services for document analysis and model training
- Ready for production deployment with Azure credentials

## API Endpoints

### Authentication & Users
- `POST /api/v1/users/register` - Register new user
- `POST /api/v1/users/login` - Login and get token
- `GET /api/v1/users/` - List users
- `GET /api/v1/users/{id}` - Get user details
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Accounts
- `POST /api/v1/accounts/` - Create account
- `GET /api/v1/accounts/` - List accounts
- `GET /api/v1/accounts/{id}` - Get account
- `PUT /api/v1/accounts/{id}` - Update account

### Agents
- `POST /api/v1/agents/` - Create agent
- `GET /api/v1/agents/` - List agents
- `GET /api/v1/agents/{id}` - Get agent
- `PUT /api/v1/agents/{id}` - Update agent
- `POST /api/v1/agents/{id}/activate` - Activate agent
- `POST /api/v1/agents/{id}/deactivate` - Deactivate agent

### Onboarding
- `GET /api/v1/onboarding/status/{user_id}` - Get onboarding status
- `POST /api/v1/onboarding/step/{user_id}` - Complete step
- `POST /api/v1/onboarding/complete/{user_id}` - Complete onboarding

### Training
- `POST /api/v1/training/{agent_id}/train` - Train agent
- `POST /api/v1/training/{agent_id}/train/url` - Add URL source
- `POST /api/v1/training/{agent_id}/train/document` - Upload document
- `GET /api/v1/training/{agent_id}/training-status` - Get status

## Configuration

Key environment variables in `.env`:

```env
# Database
DATABASE_URL=sqlite:///./orkinosai.db

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Azure (Optional)
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_AI_ENDPOINT=your-ai-endpoint
AZURE_AI_KEY=your-ai-key
```

## License

Copyright (c) 2024 Orkinosai