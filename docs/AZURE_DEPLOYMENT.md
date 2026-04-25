# Azure Deployment Guide

This guide covers deploying the Orkinosai Conversational Agent to Azure, including all
required Azure AI services.

## Required Azure Resources

Before deploying, create the following resources in your Azure subscription.

### 1. Azure OpenAI Service (AI)

The conversational agent requires an **Azure OpenAI** resource to power its AI responses.

```bash
# Register the OpenAI provider (one-time per subscription)
az provider register --namespace Microsoft.CognitiveServices

# Create a resource group (if not already done)
az group create --name sitechat-rg --location eastus

# Create the Azure OpenAI resource
az cognitiveservices account create \
  --name orkinosai-openai \
  --resource-group sitechat-rg \
  --kind OpenAI \
  --sku S0 \
  --location eastus

# Deploy a GPT-4o model (adjust model/version as available in your region)
az cognitiveservices account deployment create \
  --name orkinosai-openai \
  --resource-group sitechat-rg \
  --deployment-name gpt-4o \
  --model-name gpt-4o \
  --model-version "2024-08-06" \
  --model-format OpenAI \
  --capacity 10
```

Once created, retrieve the endpoint and key:
```bash
# Endpoint
az cognitiveservices account show \
  --name orkinosai-openai \
  --resource-group sitechat-rg \
  --query properties.endpoint -o tsv

# API key
az cognitiveservices account keys list \
  --name orkinosai-openai \
  --resource-group sitechat-rg \
  --query key1 -o tsv
```

Set these as environment variables (see **Configure Environment Variables** below):
- `AZURE_AI_ENDPOINT` — the endpoint URL
- `AZURE_AI_API_KEY` — the API key
- `AZURE_OPENAI_DEPLOYMENT` — the model deployment name (e.g. `gpt-4o`)
- `AZURE_OPENAI_API_VERSION` — the API version (e.g. `2024-08-01-preview`)

### 2. Azure App Service

The web app host for both the conversational agent (Python) and the CMS (.NET).

```bash
# Create App Service plan (Linux, B1 tier is sufficient for dev/test)
az appservice plan create \
  --name orkinosai-plan \
  --resource-group sitechat-rg \
  --sku B1 \
  --is-linux

# Create the web app for the conversational agent (Python)
az webapp create \
  --name orkinosai-agent \
  --resource-group sitechat-rg \
  --plan orkinosai-plan \
  --runtime "PYTHON:3.11"

# Create the web app for the CMS (.NET)
az webapp create \
  --name sitechat \
  --resource-group sitechat-rg \
  --plan orkinosai-plan \
  --runtime "DOTNETCORE:8.0"
```

### 3. Download the Publish Profile

The GitHub Actions workflow authenticates to Azure using a **publish profile**.

1. Go to the [Azure Portal](https://portal.azure.com).
2. Open the App Service (`sitechat` or `orkinosai-agent`).
3. Click **Overview** → **Get publish profile** (downloads a `.PublishSettings` file).
4. In your GitHub repository, go to **Settings → Secrets and variables → Actions**.
5. Create a new secret named **`CMS_PUBLISH_PROFILE`** (for the `sitechat` CMS) or
   **`AGENT_PUBLISH_PROFILE`** (for the `orkinosai-agent` Python app) and paste the full
   contents of the downloaded `.PublishSettings` file as the value.

> **Tip:** Each App Service has its own publish profile. If you deploy both the CMS
> and the Python agent from GitHub Actions, create separate secrets for each
> (e.g. `CMS_PUBLISH_PROFILE` for the CMS, `AGENT_PUBLISH_PROFILE` for the Python app).

---

## Deployment Options

### Option 1: Azure App Service (Recommended)

Best for: Production web applications with auto-scaling

#### Prerequisites
- Azure CLI installed
- Azure subscription
- Azure OpenAI resource

#### Steps

1. **Create App Service**
   ```bash
   # Login to Azure
   az login
   
   # Create resource group
   az group create --name sitechat-rg --location eastus
   
   # Create App Service plan
   az appservice plan create \
     --name orkinosai-plan \
     --resource-group sitechat-rg \
     --sku B1 \
     --is-linux
   
   # Create web app
   az webapp create \
     --name orkinosai-agent \
     --resource-group sitechat-rg \
     --plan orkinosai-plan \
     --runtime "PYTHON:3.11"
   ```

2. **Configure Environment Variables**
   ```bash
   az webapp config appsettings set \
     --name orkinosai-agent \
     --resource-group sitechat-rg \
     --settings \
       AZURE_AI_ENDPOINT="https://your-resource.openai.azure.com/" \
       AZURE_AI_API_KEY="your-api-key" \
       AZURE_OPENAI_DEPLOYMENT="your-deployment" \
       AZURE_OPENAI_API_VERSION="2024-08-01-preview"
   ```

3. **Deploy Application**
   ```bash
   # Using ZIP deployment
   zip -r app.zip . -x "*.git*" -x "venv/*" -x "*.pyc"
   
   az webapp deployment source config-zip \
     --name orkinosai-agent \
     --resource-group sitechat-rg \
     --src app.zip
   ```

### Option 2: Azure Container Apps

Best for: Microservices, containerized applications

#### Steps

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   EXPOSE 5000
   
   CMD ["python", "main.py"]
   ```

2. **Build and Push Container**
   ```bash
   # Create container registry
   az acr create \
     --name orkinosaiacr \
     --resource-group sitechat-rg \
     --sku Basic
   
   # Build and push
   az acr build \
     --registry orkinosaiacr \
     --image orkinosai-agent:v1 .
   ```

3. **Deploy Container App**
   ```bash
   az containerapp create \
     --name orkinosai-agent \
     --resource-group sitechat-rg \
     --image orkinosaiacr.azurecr.io/orkinosai-agent:v1 \
     --environment mycontainerenv \
     --target-port 5000 \
     --ingress external \
     --env-vars \
       AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
       AZURE_OPENAI_API_KEY="secretref:openai-key" \
       AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment"
   ```

### Option 3: Azure Functions

Best for: Event-driven, serverless workloads

1. **Install Azure Functions Core Tools**
   ```bash
   npm install -g azure-functions-core-tools@4
   ```

2. **Create Function App**
   ```bash
   func init --python
   func new --name chat --template "HTTP trigger"
   ```

3. **Deploy**
   ```bash
   func azure functionapp publish orkinosai-functions
   ```

## Security Best Practices

### Use Managed Identity

Instead of API keys, use Azure Managed Identity:

```python
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
```

Enable managed identity in Azure:
```bash
az webapp identity assign \
  --name orkinosai-agent \
  --resource-group sitechat-rg
```

### Use Azure Key Vault

Store secrets in Key Vault:

```bash
# Create Key Vault
az keyvault create \
  --name orkinosai-kv \
  --resource-group sitechat-rg \
  --location eastus

# Add secrets
az keyvault secret set \
  --vault-name orkinosai-kv \
  --name openai-api-key \
  --value "your-api-key"

# Grant access to App Service
az keyvault set-policy \
  --name orkinosai-kv \
  --object-id <app-identity-id> \
  --secret-permissions get list
```

Reference in App Service:
```bash
az webapp config appsettings set \
  --name orkinosai-agent \
  --resource-group sitechat-rg \
  --settings \
    AZURE_OPENAI_API_KEY="@Microsoft.KeyVault(SecretUri=https://orkinosai-kv.vault.azure.net/secrets/openai-api-key/)"
```

## Monitoring and Logging

### Application Insights

1. **Create Application Insights**
   ```bash
   az monitor app-insights component create \
     --app orkinosai-insights \
     --location eastus \
     --resource-group sitechat-rg
   ```

2. **Connect to App Service**
   ```bash
   az webapp config appsettings set \
     --name orkinosai-agent \
     --resource-group sitechat-rg \
     --settings \
       APPLICATIONINSIGHTS_CONNECTION_STRING="your-connection-string"
   ```

### Log Analytics

Monitor logs in real-time:
```bash
az webapp log tail \
  --name orkinosai-agent \
  --resource-group sitechat-rg
```

## Scaling

### Auto-scaling Rules

```bash
az monitor autoscale create \
  --resource-group sitechat-rg \
  --resource orkinosai-agent \
  --resource-type Microsoft.Web/sites \
  --name autoscale-rules \
  --min-count 1 \
  --max-count 5 \
  --count 1

az monitor autoscale rule create \
  --resource-group sitechat-rg \
  --autoscale-name autoscale-rules \
  --condition "CpuPercentage > 70 avg 5m" \
  --scale out 1
```

## Cost Optimization

1. **Use appropriate pricing tiers**
   - Development: B1 (Basic)
   - Production: P1V2 (Premium) or higher

2. **Configure auto-scaling** to scale down during low usage

3. **Monitor Azure OpenAI usage** to optimize token consumption

4. **Use Azure Cost Management** to track spending

## Continuous Deployment

### GitHub Actions

The repository's `.github/workflows/main_papagan.yml` deploys the CMS to the `sitechat`
Azure Web App automatically on every push to `main`.

**Required secret:** Add `CMS_PUBLISH_PROFILE` in your repository's
**Settings → Secrets and variables → Actions** (see **Download the Publish Profile** above).

The repository's `.github/workflows/main_orkinosai-agent.yml` deploys the Python agent to the
`orkinosai-agent` Azure Web App automatically on every push to `main`.

**Required secret:** Add `AGENT_PUBLISH_PROFILE` in your repository's
**Settings → Secrets and variables → Actions** (see **Download the Publish Profile** above for
the `orkinosai-agent` App Service).

## Troubleshooting

### Check Logs
```bash
az webapp log tail --name orkinosai-agent --resource-group sitechat-rg
```

### SSH into Container
```bash
az webapp ssh --name orkinosai-agent --resource-group sitechat-rg
```

### Restart Application
```bash
az webapp restart --name orkinosai-agent --resource-group sitechat-rg
```

## Support

For Azure-specific issues:
- [Azure Support](https://azure.microsoft.com/support/)
- [Azure Documentation](https://docs.microsoft.com/azure/)
- [Azure Community](https://techcommunity.microsoft.com/azure)
