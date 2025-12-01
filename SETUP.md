# Orkinosai CMS Setup Guide

This guide will help you set up the Orkinosai Conversational Agent CMS from scratch.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **pip**: Python package installer (usually comes with Python)
- **PostgreSQL** (optional): For production use. [Download PostgreSQL](https://www.postgresql.org/download/)
- **Git**: For version control

## Quick Start (Development)

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/orkinosai25-org/orkinosai-conversational-agent.git
cd orkinosai-conversational-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# For quick start with SQLite, you can leave DATABASE_URL as is
```

### 3. Initialize Database

```bash
# Create database tables
python init_db.py
```

### 4. Run the Application

```bash
# Start the server
python run.py
```

The API will be running at `http://localhost:8000`

### 5. Test the API

Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Production Setup

### 1. PostgreSQL Configuration

```bash
# Create PostgreSQL database
createdb orkinosai_cms

# Update .env file
DATABASE_URL=postgresql://username:password@localhost:5432/orkinosai_cms
```

### 2. Security Configuration

Update `.env` with secure values:

```env
# Generate a secure secret key
SECRET_KEY=<generate-a-secure-random-string-here>

# Recommended: Use python to generate a key
# python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Azure Configuration (Optional)

If using Azure services:

```env
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER_NAME=orkinosai-documents
AZURE_AI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_AI_KEY=your-azure-ai-key
```

### 4. Production Server

For production deployment, use a production ASGI server:

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Testing the Setup

### 1. Create a User

```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "SecurePass123",
    "full_name": "Test User"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

### 3. Create an Account

```bash
curl -X POST "http://localhost:8000/api/v1/accounts/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Organization",
    "slug": "my-org",
    "subscription_tier": "free"
  }'
```

### 4. Create an Agent

```bash
curl -X POST "http://localhost:8000/api/v1/agents/?owner_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My First Agent",
    "description": "A helpful conversational agent",
    "agent_type": "conversational"
  }'
```

## Common Issues and Solutions

### Issue: ModuleNotFoundError

**Solution**: Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Database Connection Error

**Solution**: Check your `DATABASE_URL` in `.env`. For development, use SQLite:
```env
DATABASE_URL=sqlite:///./orkinosai.db
```

### Issue: Port Already in Use

**Solution**: Change the port in `run.py` or stop the process using port 8000:
```bash
# Find process on port 8000
lsof -ti:8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Issue: Azure Services Not Working

**Solution**: Azure integration is placeholder-only by default. To enable:
1. Uncomment Azure SDK code in `app/services/azure_storage.py` and `app/services/azure_ai.py`
2. Ensure Azure credentials are correct in `.env`
3. Verify Azure resources are created and accessible

## Development Tools

### Database Management

```bash
# View SQLite database
sqlite3 orkinosai.db

# Common SQL commands
.tables          # List tables
.schema users    # View table schema
SELECT * FROM users;  # Query data
```

### API Testing Tools

- **Postman**: Import OpenAPI spec from http://localhost:8000/openapi.json
- **curl**: Command-line testing (examples above)
- **httpie**: Alternative to curl: `http POST localhost:8000/api/v1/users/register email=test@test.com ...`

## Next Steps

1. **Explore the API**: Use the Swagger UI at http://localhost:8000/docs
2. **Configure Azure**: Set up Azure services for production features
3. **Customize**: Modify models, routes, and schemas for your needs
4. **Add Tests**: Create tests in a `tests/` directory
5. **Deploy**: Set up production hosting (see Production Setup above)

## Getting Help

- Check the main README.md for detailed information
- Review API documentation at http://localhost:8000/docs
- Open an issue on GitHub for bugs or questions

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| DATABASE_URL | Database connection string | Yes | sqlite:///./orkinosai.db |
| SECRET_KEY | JWT secret key | Yes | (change in production) |
| ALGORITHM | JWT algorithm | No | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time | No | 30 |
| AZURE_STORAGE_CONNECTION_STRING | Azure Storage connection | No | None |
| AZURE_STORAGE_CONTAINER_NAME | Azure container name | No | orkinosai-documents |
| AZURE_AI_ENDPOINT | Azure AI endpoint URL | No | None |
| AZURE_AI_KEY | Azure AI API key | No | None |
| APP_NAME | Application name | No | Orkinosai CMS |
| ENVIRONMENT | Environment (dev/prod) | No | development |
| DEBUG | Debug mode | No | True |
