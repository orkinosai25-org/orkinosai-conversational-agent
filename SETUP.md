# Orkinosai Conversational Agent - Setup Guide

## Overview

This guide provides comprehensive setup and configuration instructions for the Orkinosai Conversational Agent. The agent can run in two modes:
- **Demo Mode**: Uses a mock AI client for testing without Azure credentials
- **Production Mode**: Connects to Azure OpenAI for full AI capabilities

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Azure OpenAI Service account (for production mode)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/orkinosai25-org/orkinosai-conversational-agent.git
   cd orkinosai-conversational-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

1. **Copy the example environment file**
   ```bash
   cp .env.example .env
   ```

2. **Configure Azure OpenAI (Production Mode)**
   
   Edit `.env` and set the following variables:
   ```bash
   # Azure OpenAI Configuration
   AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key-here
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   ```

   **To obtain these values:**
   - Log in to [Azure Portal](https://portal.azure.com)
   - Navigate to your Azure OpenAI resource
   - Go to "Keys and Endpoint" section
   - Copy the endpoint URL and API key
   - Go to "Model deployments" to find your deployment name

3. **Demo Mode (No Azure Credentials Required)**
   
   If you don't set the Azure credentials or leave them as placeholder values, the application will automatically run in demo mode using the mock AI client. This is perfect for:
   - Testing the UI
   - Development without Azure costs
   - Demonstrations

### Application Configuration

The main configuration file is `config.yaml`. You can customize:

```yaml
agent:
  name: "Orkinosai Conversational Agent"
  version: "1.0.0"
  max_history: 10          # Number of messages to keep in context
  temperature: 0.7         # AI response creativity (0.0-2.0)
  max_tokens: 1000         # Maximum response length
  system_prompt: "You are a helpful AI assistant."

server:
  host: "0.0.0.0"
  port: 5000
  debug: false             # Set to true for development
```

## Running the Application

### Start the Server

```bash
python main.py
```

The server will start on `http://localhost:5000`

You should see output like:
```
Starting Orkinosai Conversational Agent v1.0.0
Server running on http://0.0.0.0:5000
Logs: logs/agent.log
```

### Access the UI

Open your web browser and navigate to:
```
http://localhost:5000
```

## Testing the Setup

### 1. Health Check

Test if the server is running:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "agent": "Orkinosai Conversational Agent",
  "version": "1.0.0"
}
```

### 2. Chat Endpoint Test

Send a test message:
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World"}'
```

Expected response:
```json
{
  "conversation_id": "default",
  "user_message": "Hello World",
  "assistant_message": "Hello! I'm your Orkinosai Conversational Agent...",
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 22,
    "total_tokens": 30
  },
  "timestamp": "2025-12-02T07:28:06.417861"
}
```

### 3. UI Test

1. Open http://localhost:5000 in your browser
2. Click "Start Chatting" button
3. Type "Hello World" and press Enter or click Send
4. You should receive a response from the agent

**Demo Mode Response:**
> "Hello! I'm your Orkinosai Conversational Agent. I'm currently running in demo mode without Azure OpenAI credentials. How can I help you today?"

**Production Mode Response:**
> Will vary based on Azure OpenAI model response

## Running Tests

Execute the test suite:
```bash
pytest tests/ -v
```

All tests should pass:
```
75 passed, 1 skipped, 82 warnings
```

## Features

### Working Features

✅ **Basic Chat Functionality**
- Send and receive messages
- Conversation history management
- Multiple conversation support
- Adjustable temperature and max tokens

✅ **Authentication (Demo)**
- User registration
- User login
- Session management

✅ **Training Features (Scaffolded)**
- Learn from URLs
- Document upload
- Document management

✅ **UI Components**
- Responsive chat interface
- Side panels for conversations and settings
- Status indicators
- Real-time updates

### Mode Detection

The application automatically detects which mode to run in:

**Demo Mode runs when:**
- No `.env` file exists
- Azure credentials are not set
- Azure credentials are set to placeholder values (e.g., `${AZURE_OPENAI_API_KEY}`)

**Production Mode runs when:**
- Valid Azure OpenAI credentials are configured in `.env`
- All required environment variables are set

## API Endpoints

### Chat
- `POST /chat` - Send a message and get a response
  ```json
  {
    "conversation_id": "optional-id",
    "message": "Your message here",
    "temperature": 0.7,
    "max_tokens": 1000
  }
  ```

### Conversations
- `GET /conversations/<id>` - Get conversation details
- `DELETE /conversations/<id>` - Delete a conversation
- `POST /conversations/<id>/clear` - Clear conversation history

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login a user

### Training
- `POST /training/url` - Learn from a URL
- `POST /training/documents` - Upload documents
- `GET /training/documents` - List uploaded documents
- `DELETE /training/documents/<id>` - Delete a document

### System
- `GET /health` - Health check endpoint
- `GET /` - Serve the chat UI

## Troubleshooting

### Issue: Server won't start
- Check if port 5000 is already in use
- Verify Python version: `python --version` (should be 3.8+)
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Issue: Chat doesn't respond
- Check browser console for errors (F12)
- Verify server is running: `curl http://localhost:5000/health`
- Check logs in `logs/agent.log`

### Issue: Azure OpenAI errors
- Verify your API key is valid
- Check endpoint URL format: should end with `.openai.azure.com/`
- Ensure deployment name matches your Azure deployment
- Check API version is supported: `2024-08-01-preview` or later

### Issue: CORS errors in browser
- Check `config.yaml` `server.cors_origins` setting
- In development, it should be set to `["*"]`

## Security Notes

⚠️ **IMPORTANT: This implementation includes demo features for development only**

Before deploying to production:
1. Replace plain-text password storage with bcrypt hashing
2. Implement JWT tokens with expiration
3. Use a proper database instead of in-memory storage
4. Add rate limiting for API endpoints
5. Enable HTTPS/TLS
6. Add CSRF protection
7. Implement proper session management
8. Add input validation and sanitization
9. Use environment-specific configuration
10. Add security headers (HSTS, CSP, etc.)

See comments in `src/api/app.py` for detailed security recommendations.

## Docker Deployment

Build and run with Docker:
```bash
docker-compose up --build
```

The application will be available at http://localhost:5000

## Next Steps

After successful setup:
1. ✅ Verify the "Hello World" conversation works
2. Configure Azure OpenAI credentials for full functionality
3. Customize the system prompt in `config.yaml`
4. Test document upload and URL learning features
5. Implement additional security measures for production
6. Add custom training data for your use case

## Support

For issues or questions:
- Check the [ARCHITECTURE.md](ARCHITECTURE.md) for system design details
- Review [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines
- Open an issue on GitHub

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.
