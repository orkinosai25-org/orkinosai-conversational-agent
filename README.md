# Orkinosai Conversational Agent

An Azure AI-powered conversational agent with a RESTful API interface. This project provides a complete scaffolding for building conversational AI applications using Azure OpenAI Service.

## Features

- 🤖 Azure OpenAI Service integration
- 💬 Conversation management with history
- 🔧 Flexible configuration via YAML and environment variables
- 🌐 RESTful API endpoints
- 📝 Comprehensive logging
- 🔒 Secure credential management
- 🎯 Type-safe with Pydantic models

## Architecture

This project follows a **domain-partitioned architecture** separating:
- **CMS Domain**: Generic, reusable features (user management, roles, billing, etc.) - to be synced with orkinosaicms
- **Agent Domain**: AI-specific features (chat, Azure OpenAI, conversations)

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation, including:
- Domain separation strategy
- CMS-Agent synchronization guidelines
- Development workflow and best practices
- Integration patterns

**Important**: All CMS domain features must be copied from [orkinosaicms](https://github.com/orkinosai25-org/orkinosaicms) before implementing agent-specific features.

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI Service account
- Azure OpenAI deployment (e.g., GPT-4, GPT-3.5-turbo)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/orkinosai25-org/orkinosai-conversational-agent.git
cd orkinosai-conversational-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

### Configuration File

The `config.yaml` file contains application settings:

- **Azure Configuration**: OpenAI endpoint, API keys, deployment settings
- **Agent Settings**: Model parameters, system prompts, conversation history limits
- **Server Settings**: Host, port, CORS configuration
- **Logging**: Log level, format, and file location

See `config.yaml` for detailed configuration options.

## Usage

### Starting the Server

Run the API server:

```bash
python main.py
```

The server will start on `http://localhost:5000` by default.

### API Endpoints

#### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "agent": "Orkinosai Conversational Agent",
  "version": "1.0.0"
}
```

#### Chat
```bash
POST /chat
Content-Type: application/json

{
  "conversation_id": "optional-id",
  "message": "Hello, how are you?",
  "temperature": 0.7,
  "max_tokens": 1000
}
```

Response:
```json
{
  "conversation_id": "optional-id",
  "user_message": "Hello, how are you?",
  "assistant_message": "I'm doing well, thank you! How can I help you today?",
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 15,
    "total_tokens": 35
  },
  "timestamp": "2025-11-29T22:00:00.000000"
}
```

#### Get Conversation
```bash
GET /conversations/{conversation_id}
```

#### Clear Conversation
```bash
POST /conversations/{conversation_id}/clear
```

#### Delete Conversation
```bash
DELETE /conversations/{conversation_id}
```

## Project Structure

```
orkinosai-conversational-agent/
├── src/
│   ├── __init__.py
│   ├── agent/                   # AGENT DOMAIN (AI-specific features)
│   │   ├── __init__.py
│   │   ├── azure_client.py      # Azure OpenAI client wrapper
│   │   └── conversation.py      # Conversation management
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py              # Flask API endpoints
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration management
│   └── cms/                     # CMS DOMAIN (to be implemented)
│       └── (generic features copied from orkinosaicms)
├── tests/                       # Test directory
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # Architecture and domain partitioning
│   ├── CMS_FEATURES_INVENTORY.md # CMS features to be copied
│   ├── CMS_SYNC_LOG.md          # Sync history with orkinosaicms
│   ├── DOMAIN_INTEGRATION.md    # Integration guidelines
│   └── AZURE_DEPLOYMENT.md      # Azure deployment guide
├── logs/                        # Log files
├── config.yaml                  # Application configuration
├── .env.example                 # Example environment variables
├── requirements.txt             # Python dependencies
├── setup.py                     # Package setup
├── main.py                      # Application entry point
└── README.md                    # This file
```

**Note**: The `src/cms/` directory will be populated with generic features copied from the main orkinosaicms project. See [docs/CMS_FEATURES_INVENTORY.md](docs/CMS_FEATURES_INVENTORY.md) for details.

## Development

### Adding Custom System Prompts

Edit the `system_prompt` in `config.yaml`:

```yaml
agent:
  system_prompt: "You are a helpful assistant specialized in..."
```

### Extending the API

Add new endpoints in `src/api/app.py`:

```python
@app.route("/your-endpoint", methods=["POST"])
def your_endpoint():
    # Your implementation
    pass
```

### Using Azure AI Search (Optional)

Configure Azure AI Search in `config.yaml` and `.env` to enable RAG (Retrieval Augmented Generation) capabilities.

## Security

- Never commit `.env` files or secrets to version control
- Use Azure Key Vault for production credential management
- Rotate API keys regularly
- Implement proper authentication for production deployments

## Troubleshooting

### Connection Errors
- Verify Azure OpenAI endpoint and API key
- Check network connectivity and firewall settings
- Ensure deployment name matches your Azure configuration

### Import Errors
- Verify virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Configuration Errors
- Check `.env` file has all required variables
- Verify `config.yaml` syntax is valid YAML

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on GitHub.