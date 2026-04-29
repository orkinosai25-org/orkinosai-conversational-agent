// Orkinosai Conversational Agent — Azure Infrastructure (MVP)
// Deploys: Azure SQL Database (serverless GP) + Azure Blob Storage
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

// ── Modules ───────────────────────────────────────────────────────────────────
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
