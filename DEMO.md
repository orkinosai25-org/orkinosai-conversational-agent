# Hello World Demo - SiteChat Agent

This document provides a quick start guide to demonstrate the basic conversation functionality of the SiteChat Agent.

## Quick Start (No Azure Credentials Required)

The agent works out-of-the-box in **demo mode** without any Azure OpenAI credentials. This is perfect for testing the UI and basic functionality.

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python main.py
```

You should see:
```
Starting SiteChat Agent v1.0.0
Server running on http://0.0.0.0:5000
Logs: logs/agent.log
```

### 3. Open the Web Interface

Navigate to: **http://localhost:5000**

### 4. Hello World Test

1. Click the **"Start Chatting"** button on the welcome screen
2. Type **"Hello World"** in the message input box
3. Press **Enter** or click the **Send** button (paper plane icon)
4. You should receive a response from the agent

**Expected Response in Demo Mode:**
> "Hello! I'm your SiteChat Agent. I'm currently running in demo mode without Azure OpenAI credentials. How can I help you today?"

## Testing via Command Line

You can also test the API directly using curl:

### Health Check
```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "agent": "SiteChat Agent",
  "version": "1.0.0"
}
```

### Chat Endpoint Test
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World"}'
```

**Expected Response:**
```json
{
  "conversation_id": "default",
  "user_message": "Hello World",
  "assistant_message": "Hello! I'm your SiteChat Agent. I'm currently running in demo mode without Azure OpenAI credentials. How can I help you today?",
  "usage": {
    "prompt_tokens": 8,
    "completion_tokens": 22,
    "total_tokens": 30
  },
  "timestamp": "2025-12-02T07:28:06.417861"
}
```

### Multi-Turn Conversation
```bash
# First message
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "demo-1", "message": "Hello"}'

# Second message in same conversation
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "demo-1", "message": "What can you do?"}'
```

## Demo Features Available

### ✅ Chat Interface
- Real-time message sending and receiving
- Conversation history display
- Multiple conversation support
- Message timestamps

### ✅ Settings Panel
- Adjustable temperature (0.0 - 1.0)
- Configurable max tokens (100 - 4000)
- Settings persist in browser localStorage

### ✅ Training Features (UI Available)
- Learn from URLs
- Document upload
- Document management

### ✅ Authentication (Demo Implementation)
- User registration
- User login/logout
- Session management

## UI Features Walkthrough

### Navigation Bar
- **Menu**: Opens conversation list sidebar
- **Training**: Opens training panel for URL learning
- **Documents**: Opens document upload panel
- **Login/Register**: Authentication options

### Chat Interface
After clicking "Start Chatting":
- **Chat Header**: Shows conversation title
- **Clear Button**: Clears current conversation
- **Settings Button**: Opens settings panel
- **Message Input**: Type your messages here
- **Send Button**: Sends your message

### Right Panel (Settings)
- **Temperature Slider**: Controls response creativity
- **Max Tokens Input**: Controls response length

### Bottom Status Bar
- **Status Text**: Shows current operation status
- **Connection Status**: Shows server connection state

## Running Tests

Verify everything is working:

```bash
# Run all tests
pytest tests/ -v

# Run only Azure integration tests
pytest tests/test_azure_integration.py -v

# Run only UI endpoint tests
pytest tests/test_ui_endpoints.py -v
```

**Expected:** All tests should pass (75 tests, 1 skipped)

## Enabling Azure OpenAI (Production Mode)

To enable full AI capabilities with Azure OpenAI:

1. **Create a `.env` file:**
   ```bash
   cp .env.example .env
   ```

2. **Configure Azure credentials in `.env`:**
   ```bash
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-actual-api-key
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   AZURE_OPENAI_API_VERSION=2024-08-01-preview
   ```

3. **Restart the server:**
   ```bash
   python main.py
   ```

Now the agent will use Azure OpenAI for intelligent responses instead of the demo mock client.

## Demo Mode vs Production Mode

| Feature | Demo Mode | Production Mode |
|---------|-----------|-----------------|
| **Credentials Required** | None | Azure OpenAI credentials |
| **AI Responses** | Predefined contextual responses | Real Azure OpenAI responses |
| **Cost** | Free | Azure OpenAI usage costs |
| **Best For** | Testing, UI development, demos | Real use cases, production |
| **Conversation Context** | Maintains conversation history | Maintains conversation history |
| **All UI Features** | ✅ Available | ✅ Available |

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use a different port
# Edit config.yaml and change server.port
```

### Cannot Access UI
1. Check server is running: `curl http://localhost:5000/health`
2. Check firewall settings
3. Try accessing via: `http://127.0.0.1:5000`

### No Response from Chat
1. Open browser console (F12) and check for errors
2. Check server logs: `tail -f logs/agent.log`
3. Verify server status: `curl http://localhost:5000/health`

## Demo Conversation Examples

Try these prompts in demo mode to see contextual responses:

- **"Hello"** - Get a welcome message
- **"What can you do?"** - Learn about agent capabilities
- **"How do I train you?"** - Information about training features
- **"Tell me about documents"** - Document upload information
- **"What about Azure OpenAI?"** - Configuration instructions
- **"Thank you"** - Polite acknowledgment
- **"Goodbye"** - Farewell message

## Screenshot

![Chat UI Working](https://github.com/user-attachments/assets/d7dca51c-93be-455a-ad6d-bbe902fd8776)

## Next Steps

After verifying the "Hello World" demo works:

1. ✅ Test multiple conversation threads
2. ✅ Try adjusting temperature and max tokens
3. ✅ Test the training and document features
4. Configure Azure OpenAI credentials for production
5. Customize system prompts in `config.yaml`
6. Implement additional features as needed

## Support

- **Setup Guide**: See [SETUP.md](SETUP.md) for detailed configuration
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

## Summary

✅ **The SiteChat Agent is fully functional and ready for testing!**

- Chat UI is working correctly
- Backend API responds to messages
- Mock client provides demo responses
- Azure OpenAI integration is ready (when credentials are provided)
- All tests pass (75+ tests)
- Documentation is complete
