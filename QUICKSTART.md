# Quick Start Guide

Get started with the Papagan - The Chatter Parrot in minutes! **No Azure account required to start!**

## Prerequisites

- Python 3.8+
- (Optional) Azure OpenAI Service account for production use

## 2-Minute Quick Start

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python main.py
```

That's it! The server starts at `http://localhost:5000` and is ready to use.

### 3. Test the Chat

**Option A: Use the Web UI**

Open your browser to `http://localhost:5000` and start chatting!

**Option B: Test via API**

Open a new terminal and run:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

You'll get a response from the demo AI agent immediately!

**Option C: Run the example script**

```bash
python examples/simple_chat.py
```

## What Just Happened?

The application automatically:
- ✅ Created `appsettings.json` with default configuration
- ✅ Started in demo mode with a mock AI client
- ✅ Made the chat interface fully functional
- ✅ Works without any Azure credentials or costs!

## Upgrade to Azure OpenAI (Optional)

When you're ready to use real Azure OpenAI:

### 1. Edit `appsettings.json`

The file was auto-created in your project root. Update these values:

```json
{
  "azure": {
    "openai": {
      "endpoint": "https://your-resource.openai.azure.com/",
      "api_key": "your-api-key-here",
      "deployment_name": "your-gpt4-deployment",
      "api_version": "2024-08-01-preview"
    }
  }
}
```

### 2. Restart the Server

```bash
# Stop with Ctrl+C, then restart
python main.py
```

The app automatically detects your credentials and switches to production mode!

## What's Next?

- **Customize the agent**: Edit `appsettings.json` to adjust temperature, system prompt, etc.
- **Add authentication**: Implement auth middleware in `src/api/app.py`
- **Connect to Azure AI Search**: Enable RAG by configuring search in `appsettings.json`
- **Deploy to Azure**: Use Azure App Service, Azure Functions, or Azure Container Apps

## Common Issues

**Import errors**: Make sure virtual environment is activated and dependencies installed

**Port already in use**: Change the port in `appsettings.json` under `server.port`

**Connection errors (with Azure)**: Verify your Azure endpoint URL and API key in `appsettings.json`

**Deployment name error (with Azure)**: Ensure `deployment_name` matches your Azure OpenAI deployment

## Project Structure

```
├── src/
│   ├── agent/          # Azure AI client and conversation logic
│   ├── api/            # Flask REST API
│   └── config/         # Configuration management
├── tests/              # Unit tests
├── examples/           # Example scripts
├── config.yaml         # App configuration
├── .env               # Your credentials (not in git)
└── main.py            # Entry point
```

## Need Help?

- Read the full [README.md](README.md)
- Check [examples/README.md](examples/README.md)
- Open an issue on GitHub
