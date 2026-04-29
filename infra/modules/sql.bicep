// Azure SQL Server + Database module
// Provisions a serverless Azure SQL Database (General Purpose, GP_S_Gen5_1) —
// the most cost-efficient tier for an MVP/SaaS workload that pauses automatically
// when idle and bills only for vCore-seconds consumed.

@description('Base name used to build resource names (e.g. "orkinosai")')
param baseName string

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('SQL administrator login name')
param sqlAdminLogin string

@description('SQL administrator password — supply via Key Vault reference or parameter file; never commit a real value')
@secure()
param sqlAdminPassword string

@description('Name of the SQL database')
param databaseName string = 'sitechat'

// ── SQL Server ────────────────────────────────────────────────────────────────
resource sqlServer 'Microsoft.Sql/servers@2023-05-01-preview' = {
  name: '${baseName}-sql'
  location: location
  properties: {
    administratorLogin: sqlAdminLogin
    administratorLoginPassword: sqlAdminPassword
    // Allow Azure services to reach the server (required for App Service)
    publicNetworkAccess: 'Enabled'
  }
}

// Allow all Azure services through the firewall
resource azureServicesFirewallRule 'Microsoft.Sql/servers/firewallRules@2023-05-01-preview' = {
  parent: sqlServer
  name: 'AllowAllWindowsAzureIps'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// ── SQL Database (serverless — cheapest GP tier) ──────────────────────────────
resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-05-01-preview' = {
  parent: sqlServer
  name: databaseName
  location: location
  sku: {
    name: 'GP_S_Gen5'   // General Purpose Serverless, Gen5
    tier: 'GeneralPurpose'
    family: 'Gen5'
    capacity: 1          // 1 vCore — minimum; auto-scales to 4 vCores under load
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    autoPauseDelay: 60   // Auto-pause after 60 minutes idle (saves cost)
    minCapacity: '0.5'   // Minimum 0.5 vCores when active
    zoneRedundant: false // Single-zone — enable for production HA if needed
    requestedBackupStorageRedundancy: 'Local' // Cheapest backup option
  }
}

// ── Outputs ───────────────────────────────────────────────────────────────────
@description('Fully-qualified domain name of the SQL server')
output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName

@description('ADO.NET connection string for the database (password omitted — inject at runtime)')
output connectionStringTemplate string = 'Server=tcp:${sqlServer.properties.fullyQualifiedDomainName},1433;Initial Catalog=${databaseName};Persist Security Info=False;User ID=${sqlAdminLogin};Password=<your-password>;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;'
