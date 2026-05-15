// Orkinosai Conversational Agent — Azure Infrastructure
// Deploys: App Service Plan + CMS App Service + Agent App Service
//          + Azure SQL Database (serverless GP) + Azure Blob Storage
//
// NOTE — Azure AI Search (future)
// When you are ready to add retrieval-augmented generation (RAG), provision an
// Azure AI Search resource (sku: 'basic' is the cheapest paid tier that supports
// semantic search).  A minimal Bicep snippet is included below as a comment so
// you can uncomment and deploy it when needed.
//
//   resource aiSearch 'Microsoft.Search/searchServices@2023-11-01' = {
//     name: '${baseName}-search'
//     location: location
//     sku: { name: 'basic' }
//     properties: {
//       replicaCount: 1
//       partitionCount: 1
//       hostingMode: 'default'
//       publicNetworkAccess: 'enabled'
//     }
//   }
//
// The search service endpoint and admin key should be set as App Service
// application settings:
//   AzureSearch__Endpoint = https://<name>.search.windows.net
//   AzureSearch__ApiKey   = <admin-key>  (or use Managed Identity)

// ── Parameters ────────────────────────────────────────────────────────────────
@description('Short base name applied to all resources (e.g. "orkinosai"). Must be lowercase, 3-20 chars.')
@minLength(3)
@maxLength(20)
param baseName string = 'orkinosai'

@description('Azure region for all resources. Defaults to the resource group location.')
param location string = resourceGroup().location

@description('SQL administrator login name')
param sqlAdminLogin string = 'sqladmin'

@description('SQL administrator password — REQUIRED. Pass via --parameters or Key Vault; never hard-code.')
@secure()
param sqlAdminPassword string

@description('Name of the SQL database')
param databaseName string = 'sitechat'

@description('Name of the CMS Azure App Service (.NET). Must be globally unique.')
param cmsAppName string = 'site-chat-agent'

@description('Name of the Agent Azure App Service (Python). Must be globally unique.')
param agentAppName string = 'orkinosai-agent'

@description('App Service Plan SKU. B1 (Basic) is the default — it does not consume Free VM quota and is production-ready. Use S1/P1v3 for higher scale, or F1 only if you need the Free tier.')
@allowed(['F1', 'B1', 'B2', 'B3', 'S1', 'S2', 'S3', 'P1v3', 'P2v3', 'P3v3'])
param appServicePlanSku string = 'B1'

// ── Modules ───────────────────────────────────────────────────────────────────
module appservice 'modules/appservice.bicep' = {
  name: 'appservice'
  params: {
    baseName: baseName
    location: location
    planSku: appServicePlanSku
    cmsAppName: cmsAppName
    agentAppName: agentAppName
    // Build the full ADO.NET connection string from SQL outputs + supplied credentials.
    // This is injected automatically as the "Default" connection string in the CMS App Service,
    // so no manual portal step is required after deployment.
    sqlConnectionString: 'Server=tcp:${sql.outputs.sqlServerFqdn},1433;Initial Catalog=${databaseName};Persist Security Info=False;User ID=${sqlAdminLogin};Password=${sqlAdminPassword};MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'
  }
}

module sql 'modules/sql.bicep' = {
  name: 'sql'
  params: {
    baseName: baseName
    location: location
    sqlAdminLogin: sqlAdminLogin
    sqlAdminPassword: sqlAdminPassword
    databaseName: databaseName
  }
}

module storage 'modules/storage.bicep' = {
  name: 'storage'
  params: {
    baseName: baseName
    location: location
  }
}

// ── Outputs ───────────────────────────────────────────────────────────────────
@description('Azure SQL server fully-qualified domain name')
output sqlServerFqdn string = sql.outputs.sqlServerFqdn

@description('ADO.NET connection string template (replace <your-password> with the real value)')
output sqlConnectionStringTemplate string = sql.outputs.connectionStringTemplate

@description('Primary blob storage endpoint')
output blobEndpoint string = storage.outputs.blobEndpoint

@description('Storage account name (used to retrieve connection string or keys via az CLI)')
output storageAccountName string = storage.outputs.storageAccountName

@description('Resource name of the CMS App Service')
output cmsAppName string = appservice.outputs.cmsAppName

@description('Default hostname of the CMS App Service')
output cmsDefaultHostname string = appservice.outputs.cmsDefaultHostname

@description('Resource name of the Agent App Service')
output agentAppName string = appservice.outputs.agentAppName

@description('Default hostname of the Agent App Service')
output agentDefaultHostname string = appservice.outputs.agentDefaultHostname

@description('Resource name of the App Service Plan')
output appServicePlanName string = appservice.outputs.appServicePlanName
