# Configuration Guide

## Overview

The Orkinosai Conversational Agent uses `appsettings.json` as its primary configuration file. This file is automatically created with default values when you first run the application.

## How It Works

1. **First Run**: When you run `python main.py` for the first time, the application automatically creates `appsettings.json` with placeholder values
2. **Demo Mode**: With the default placeholder values, the app runs in demo mode using a mock AI client
3. **Production Mode**: When you add real Azure OpenAI credentials, the app automatically switches to production mode

## Configuration File: appsettings.json

### Azure OpenAI Settings

```json
{
  "azure": {
    "openai": {
      "endpoint": "https://your-resource-name.openai.azure.com/",
      "api_key": "your-api-key-here",
      "api_version": "2024-08-01-preview",
      "deployment_name": "your-deployment-name",
      "model": "gpt-4"
    }
  }
}
```

**How to get these values:**

1. Log in to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. **Endpoint**: Found in "Keys and Endpoint" section (e.g., `https://my-resource.openai.azure.com/`)
4. **API Key**: Found in "Keys and Endpoint" section (either Key 1 or Key 2)
5. **Deployment Name**: Found in "Model deployments" section (the name you gave when deploying the model)
6. **API Version**: Use `2024-08-01-preview` or check Azure documentation for latest version
7. **Model**: The model you deployed (e.g., `gpt-4`, `gpt-35-turbo`)

### Agent Settings

```json
{
  "agent": {
    "name": "Orkinosai Conversational Agent",
    "version": "1.0.0",
    "max_history": 10,
    "temperature": 0.7,
    "max_tokens": 1000,
    "system_prompt": "You are a helpful AI assistant."
  }
}
```

**Settings explained:**

- `name`: Display name of your agent
- `version`: Version number for tracking
- `max_history`: Number of previous messages to include in context (affects memory usage)
- `temperature`: Controls randomness in responses (0.0 = deterministic, 2.0 = very creative)
- `max_tokens`: Maximum length of generated responses
- `system_prompt`: Instructions that define your agent's personality and behavior

### Server Settings

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false,
    "cors_origins": ["*"]
  }
}
```

**Settings explained:**

- `host`: Network interface to bind to (`0.0.0.0` = all interfaces, `127.0.0.1` = localhost only)
- `port`: Port number for the web server
- `debug`: Enable Flask debug mode (set to `true` for development, `false` for production)
- `cors_origins`: Allowed CORS origins (`["*"]` = all origins, useful for development)

### Logging Settings

```json
{
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/agent.log"
  }
}
```

**Settings explained:**

- `level`: Minimum log level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- `format`: Log message format (Python logging format string)
- `file`: Path to log file (relative to project root)

### Optional: Azure AI Search (for RAG)

```json
{
  "azure": {
    "search": {
      "endpoint": "https://your-search-service.search.windows.net",
      "api_key": "your-search-api-key",
      "index_name": "your-index-name"
    }
  }
}
```

These settings are optional and only needed if you want to use Azure AI Search for Retrieval-Augmented Generation (RAG).

### Optional: Azure Cognitive Services

```json
{
  "azure": {
    "cognitive_services": {
      "endpoint": "https://your-cognitive-service.cognitiveservices.azure.com/",
      "api_key": "your-cognitive-services-key"
    }
  }
}
```

These settings are optional and only needed if you want to use additional Azure Cognitive Services.

## Environment Variables

Environment variables **override** settings in `appsettings.json`. This is useful for:

- Docker deployments
- CI/CD pipelines
- Keeping secrets out of config files

### Supported Environment Variables

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-08-01-preview

# Azure AI Search (optional)
AZURE_SEARCH_ENDPOINT=https://your-search-service.search.windows.net
AZURE_SEARCH_API_KEY=your-search-api-key
AZURE_SEARCH_INDEX_NAME=your-index-name

# Azure Cognitive Services (optional)
AZURE_COGNITIVE_SERVICES_ENDPOINT=https://your-cognitive-service.cognitiveservices.azure.com/
AZURE_COGNITIVE_SERVICES_API_KEY=your-cognitive-services-key
```

### Using .env file

Create a `.env` file in the project root:

```bash
cp .env.example .env
# Edit .env with your values
```

The application automatically loads variables from `.env` using python-dotenv.

## Demo Mode vs Production Mode

### Demo Mode (Default)

The application runs in demo mode when:
- Placeholder values are in `appsettings.json` (e.g., `"your-api-key-here"`)
- Azure credentials are not set
- Azure credentials fail to connect

**Features in demo mode:**
- ✅ Chat interface works
- ✅ All UI features available
- ✅ Mock AI responses (predefined, not real AI)
- ✅ No Azure costs
- ✅ Perfect for development and testing

### Production Mode

The application runs in production mode when:
- Valid Azure OpenAI credentials are configured
- Credentials successfully connect to Azure

**Features in production mode:**
- ✅ Real Azure OpenAI responses
- ✅ Full AI capabilities
- ✅ Customizable models and parameters
- ⚠️ Azure usage costs apply

## Configuration Priority

Settings are loaded in this order (later overrides earlier):

1. `appsettings.json` (or `config.yaml` for legacy support)
2. `.env` file
3. System environment variables

## Legacy config.yaml Support

For backward compatibility, the application still supports `config.yaml`. However, `appsettings.json` is now the recommended format.

If both files exist, `appsettings.json` takes precedence.

## Troubleshooting

### Application won't start

- Check that `appsettings.json` is valid JSON (use a JSON validator)
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Azure credentials not working

- Verify endpoint URL format (should end with `.openai.azure.com/`)
- Check that API key is correct (no extra spaces)
- Ensure deployment name matches your Azure deployment exactly
- Confirm your Azure OpenAI resource is active and not suspended

### Port already in use

Change the port in `appsettings.json`:

```json
{
  "server": {
    "port": 5001
  }
}
```

### Chat not responding

- Check browser console for errors (F12)
- Verify server is running: `curl http://localhost:5000/health`
- Check logs at `logs/agent.log`

## Best Practices

### For Development

```json
{
  "server": {
    "debug": true,
    "cors_origins": ["*"]
  },
  "logging": {
    "level": "DEBUG"
  }
}
```

### For Production

```json
{
  "server": {
    "debug": false,
    "cors_origins": ["https://your-domain.com"]
  },
  "logging": {
    "level": "INFO"
  }
}
```

### Security Tips

1. **Never commit real API keys to git**
   - Use `.env` for local development
   - Use environment variables in production
   - Add `.env` to `.gitignore`

2. **Rotate credentials regularly**
   - Azure Portal > Keys and Endpoint > Regenerate Key

3. **Use managed identities in production**
   - Consider Azure Managed Identity instead of API keys
   - Reduces credential exposure risk

4. **Restrict CORS in production**
   - Set specific origins instead of `"*"`
   - Prevents unauthorized API access

## Examples

### Example 1: Development Setup

```json
{
  "azure": {
    "openai": {
      "endpoint": "https://your-resource-name.openai.azure.com/",
      "api_key": "your-api-key-here",
      "deployment_name": "your-deployment-name"
    }
  },
  "server": {
    "debug": true,
    "port": 5000
  },
  "logging": {
    "level": "DEBUG"
  }
}
```

### Example 2: Production Setup with Environment Variables

Create `.env`:
```bash
AZURE_OPENAI_ENDPOINT=https://prod-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=sk-xxxxxxxxxxxxx
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4-prod
```

Keep `appsettings.json` with placeholders for structure:
```json
{
  "azure": {
    "openai": {
      "endpoint": "https://your-resource-name.openai.azure.com/",
      "api_key": "your-api-key-here",
      "deployment_name": "your-deployment-name"
    }
  },
  "server": {
    "debug": false,
    "cors_origins": ["https://myapp.com"]
  }
}
```

## Need Help?

- Read the [README.md](README.md) for general information
- Check [SETUP.md](SETUP.md) for detailed setup instructions
- See [QUICKSTART.md](QUICKSTART.md) for a quick start guide
- Open an issue on GitHub for support
