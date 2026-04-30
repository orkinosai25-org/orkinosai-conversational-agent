// Azure Blob Storage module
// Provisions a general-purpose v2 storage account with one container for
// bot training documents (file uploads) and one for raw ingested artefacts.

@description('Base name used to build resource names (e.g. "orkinosai")')
param baseName string

@description('Azure region for all resources')
param location string = resourceGroup().location

// Storage account names must be 3-24 lowercase alphanumeric characters; strip
// hyphens and truncate to 22 chars to leave room for the "st" suffix.
var storageAccountName = '${take(toLower(replace(baseName, '-', '')), 22)}st'

// ── Storage Account ───────────────────────────────────────────────────────────
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'  // Locally-redundant — cheapest option; upgrade to GRS for prod HA
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
    supportsHttpsTrafficOnly: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false // All blobs are private; access via SAS or Managed Identity
  }
}

// ── Blob Service ──────────────────────────────────────────────────────────────
resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
}

// ── Containers ────────────────────────────────────────────────────────────────
// training-docs: uploaded files used to train / ground the bot
resource trainingDocsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'training-docs'
  properties: {
    publicAccess: 'None'
  }
}

// raw-ingested: raw artefacts ingested by the pipeline (HTML, crawled pages, etc.)
// Used by future Azure AI Search indexer
resource rawIngestedContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'raw-ingested'
  properties: {
    publicAccess: 'None'
  }
}

// ── Outputs ───────────────────────────────────────────────────────────────────
@description('Storage account resource ID')
output storageAccountId string = storageAccount.id

@description('Storage account name')
output storageAccountName string = storageAccount.name

@description('Primary blob endpoint')
output blobEndpoint string = storageAccount.properties.primaryEndpoints.blob

@description('Name of the training-docs container')
output trainingDocsContainer string = trainingDocsContainer.name

@description('Name of the raw-ingested container')
output rawIngestedContainer string = rawIngestedContainer.name
