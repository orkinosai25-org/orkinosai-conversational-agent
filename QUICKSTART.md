# Quick Start Guide

Get started with the Orkinosai Conversational Agent in minutes!

## Prerequisites

- Python 3.8+
- Azure OpenAI Service account with a deployed model

## 5-Minute Setup

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Azure Credentials

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your Azure credentials:

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-gpt4-deployment
```

### 3. Start the Server

```bash
python main.py
```

The server starts at `http://localhost:5000`

### 4. Test the API

Open a new terminal and run:

```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello! Tell me about Azure AI."}'
```

Or run the example script:

```bash
python examples/simple_chat.py
```

## What's Next?

- **Customize the agent**: Edit `config.yaml` to adjust temperature, system prompt, etc.
- **Add authentication**: Implement auth middleware in `src/api/app.py`
- **Connect to Azure AI Search**: Enable RAG by configuring search in `.env`
- **Deploy to Azure**: Use Azure App Service, Azure Functions, or Azure Container Apps

## Common Issues

**Import errors**: Make sure virtual environment is activated and dependencies installed

**Connection errors**: Verify your Azure endpoint URL and API key in `.env`

**Deployment name error**: Ensure `AZURE_OPENAI_DEPLOYMENT_NAME` matches your Azure deployment

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
