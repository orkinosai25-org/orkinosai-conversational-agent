# Azure Deployment Guide

This guide covers deploying the Orkinosai Conversational Agent to Azure, including all
required Azure AI services.

## Required Azure Resources

Before deploying, create the following resources in your Azure subscription.

### 0. Full Azure Infrastructure (via Bicep — recommended)

All required Azure resources are provisioned by the Bicep templates in the `infra/`
directory.  A single `az deployment group create` call (or the
`Provision Azure Infrastructure (Full)` GitHub Actions workflow) creates:

- App Service Plan (`orkinosai-plan`)
- CMS App Service — `site-chat-agent` (.NET 8)
- Agent App Service — `orkinosai-agent` (Python 3.11)
- Azure SQL Server + Database
- Azure Blob Storage account (two containers: `training-docs`, `raw-ingested`)

#### Automated provisioning (recommended)

Run the **Provision Azure Infrastructure (Full)** workflow from
**Actions → Provision Azure Infrastructure (Full) → Run workflow**.

Required GitHub Secrets (add in **Settings → Secrets and variables → Actions**):

| Secret | Purpose |
|--------|---------|
| `AZURE_CREDENTIALS` | Service principal JSON (`az ad sp create-for-rbac --sdk-auth`) |
| `SQL_ADMIN_PASSWORD` | Strong password for the SQL administrator account |
| `AZURE_AI_API_KEY` | Azure OpenAI API key |
| `AZURE_AI_ENDPOINT` | Azure OpenAI endpoint URL |
| `AZURE_OPENAI_DEPLOYMENT` | Model deployment name (e.g. `gpt-4o`) |
| `AZURE_OPENAI_API_VERSION` | API version (e.g. `2024-08-01-preview`) |

The workflow provisions every resource, wires connection strings into both App
Services, and runs EF Core migrations — no manual Azure Portal clicks required.

#### Manual provisioning (alternative)

```bash
# 1. Login & select subscription
az login
az account set --subscription "<your-subscription-id>"

# 2. Create (or reuse) a resource group
az group create --name sitechat-rg --location uksouth

# 3. Deploy all resources — App Services, SQL, Blob Storage
az deployment group create \
  --resource-group sitechat-rg \
  --template-file infra/main.bicep \
  --parameters \
      baseName=orkinosai \
      sqlAdminLogin=sqladmin \
      sqlAdminPassword="<your-password>" \
      cmsAppName=site-chat-agent \
      agentAppName=orkinosai-agent \
      appServicePlanSku=B1 \
  --query "properties.outputs"
```

The deployment outputs `sqlServerFqdn`, `sqlConnectionStringTemplate`,
`blobEndpoint`, `storageAccountName`, `cmsAppName`, `cmsDefaultHostname`,
`agentAppName`, `agentDefaultHostname`, and `appServicePlanName`.

#### Retrieve the Blob Storage connection string (manual provisioning only)

When provisioning manually, retrieve the Blob connection string to configure App
Services yourself:

```bash
STORAGE_NAME=$(az deployment group show \
  --resource-group sitechat-rg \
  --name main \
  --query "properties.outputs.storageAccountName.value" -o tsv)

az storage account show-connection-string \
  --name "$STORAGE_NAME" \
  --resource-group sitechat-rg \
  --query connectionString -o tsv
```

#### Configure Azure App Services (manual provisioning only)

When provisioning manually, set the following values in
**Azure App Service → Configuration** for each app:

| Type | Name | Value |
|------|------|-------|
| Connection string | `Default` | Full ADO.NET connection string for the SQL database |
| Application setting | `Azure__BlobStorage__ConnectionString` | Blob Storage connection string from step above |

> **Note:** App Service connection strings named `Default` are exposed to .NET as
> `ConnectionStrings:Default`. Application settings with `__` become `:` in .NET
> configuration (e.g. `Azure__BlobStorage__ConnectionString` →
> `Azure:BlobStorage:ConnectionString`).

#### Run database migrations

After deploying and configuring connection strings, run the EF Core migration to
create the schema:

```bash
# From the repository root — requires the real SQL connection string in the environment
cd src/cms/Server
ASPNETCORE_ENVIRONMENT=Production \
  CONNECTIONSTRINGS__DEFAULT="<your-connection-string>" \
  dotnet ef database update
```

Or via the Azure CLI using App Service SSH / Kudu console:

```bash
dotnet ef database update
```

> **Tip:** The `InitialCreate` migration is already in
> `src/cms/Server/Infrastructure/Data/Migrations/`. No additional scaffold step
> is needed unless the schema changes.

---

### ⚠️ Security Action Item — Hardcoded SQL Password

`src/cms/Server/appsettings.Development.json` contains a hardcoded SQL password
that was committed for early development. **This credential must be rotated and
removed before the application goes live.**

**Before going live you must:**

1. **Rotate the password** on the Azure SQL Server:
   ```bash
   az sql server update \
     --name orkinosai-sql \
     --resource-group sitechat-rg \
     --admin-password "<new-strong-password>"
   ```
2. **Remove the hardcoded value** from `appsettings.Development.json` and replace
   it with `""` or use [.NET User Secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets)
   for local development.
3. **Move the secret** to Azure Key Vault:
   ```bash
   az keyvault secret set \
     --vault-name orkinosai-kv \
     --name SqlAdminPassword \
     --value "<new-strong-password>"
   ```
4. Reference it from App Service via a Key Vault reference instead of a plain value:
   ```
   @Microsoft.KeyVault(SecretUri=https://orkinosai-kv.vault.azure.net/secrets/SqlAdminPassword/)
   ```

---

### Future: Azure AI Search (not yet implemented)

When you are ready to add retrieval-augmented generation (RAG), uncomment the
`aiSearch` resource in `infra/main.bicep` and deploy.  The `raw-ingested` Blob
container created above is already ready to serve as the indexer data source.

Minimal application settings to add at that point:

| Setting | Value |
|---------|-------|
| `AzureSearch__Endpoint` | `https://<name>.search.windows.net` |
| `AzureSearch__ApiKey` | Admin key (or use Managed Identity) |

---

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

### 2. Azure App Service (provisioned automatically by Bicep)

The App Service Plan and both App Services (CMS and Agent) are now provisioned
by the Bicep templates — **no manual `az webapp create` steps are required**.

When you run the `Provision Azure Infrastructure (Full)` workflow (or the
manual `az deployment group create` command above), the following are created:

| Resource | Name | Runtime |
|----------|------|---------|
| App Service Plan | `orkinosai-plan` | Linux B1 |
| CMS App Service | `site-chat-agent` | .NET 8 |
| Agent App Service | `orkinosai-agent` | Python 3.11 |

### 3. Download the Publish Profile

The GitHub Actions deploy workflows authenticate to Azure using a **publish profile**.
Download these **after** the provisioning workflow has created the App Services.

1. Go to the [Azure Portal](https://portal.azure.com).
2. Open the **`site-chat-agent`** App Service.
3. Click **Overview** → **Get publish profile** (downloads a `.PublishSettings` file).
4. In your GitHub repository, go to **Settings → Secrets and variables → Actions**.
5. Create a secret named **`PUBLISH_PROFILE`** and paste the full contents of the downloaded file.
6. Repeat steps 2–5 for the **`orkinosai-agent`** App Service, saving as **`AGENT_PUBLISH_PROFILE`**.

> **Tip:** Each App Service has its own publish profile. Both secrets must be set before
> the respective deploy workflow can succeed.

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

Three workflows handle the full lifecycle:

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `Provision Azure Infrastructure (Full)` | Manual (`workflow_dispatch`) | Create/update all Azure resources via Bicep |
| `Build and deploy ASP.Net Core app` (`main_papagan.yml`) | Push to `main` | Deploy CMS to `site-chat-agent` |
| `Build and deploy Python app` (`main_orkinosai-agent.yml`) | Push to `main` | Deploy agent to `orkinosai-agent` |

**Recommended first-time setup order:**
1. Add all required secrets (see table in section 0 above, plus `PUBLISH_PROFILE` and `AGENT_PUBLISH_PROFILE`).
2. Run **Provision Azure Infrastructure (Full)** — this creates everything and wires config.
3. Download publish profiles from the newly created App Services and save as secrets.
4. Push to `main` — both deploy workflows will fire automatically.

**Required secrets for deploy workflows:**
- `PUBLISH_PROFILE` — publish profile for the `site-chat-agent` CMS App Service
- `AGENT_PUBLISH_PROFILE` — publish profile for the `orkinosai-agent` Python App Service

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
