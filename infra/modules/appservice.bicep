// App Service Plan + App Services for CMS (.NET) and Agent (Python)
// Provisions a shared Linux App Service Plan with two web apps:
//   - CMS        : ASP.NET Core 8.0 (Blazor / Papagan CMS)
//   - Agent      : Python 3.11 (Orkinosai conversational agent)

@description('Base name used to build resource names (e.g. "orkinosai")')
param baseName string

@description('Azure region for all resources')
param location string = resourceGroup().location

@description('App Service Plan SKU. B1 is sufficient for dev/test; use P1v3 for production.')
@allowed(['B1', 'B2', 'B3', 'P1v3', 'P2v3', 'P3v3'])
param planSku string = 'B1'

@description('Name of the CMS Azure App Service (.NET)')
param cmsAppName string = 'site-chat-agent'

@description('Name of the Agent Azure App Service (Python)')
param agentAppName string = 'orkinosai-agent'

// ── App Service Plan (Linux) ──────────────────────────────────────────────────
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${baseName}-plan'
  location: location
  kind: 'linux'
  sku: {
    name: planSku
  }
  properties: {
    reserved: true // Required for Linux-hosted apps
  }
}

// ── CMS App Service (.NET 8) ──────────────────────────────────────────────────
resource cmsApp 'Microsoft.Web/sites@2023-01-01' = {
  name: cmsAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOTNETCORE|8.0'
      alwaysOn: false // Disabled on B1 (no always-on support); enable on P1v3+
      // SCM_DO_BUILD_DURING_DEPLOYMENT is NOT set here — publish-profile deploys
      // a pre-built artifact so Oryx build is not needed.
    }
  }
}

// ── Agent App Service (Python 3.11) ──────────────────────────────────────────
resource agentApp 'Microsoft.Web/sites@2023-01-01' = {
  name: agentAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      alwaysOn: false
      appCommandLine: 'gunicorn --bind=0.0.0.0:8000 --timeout 120 wsgi:app'
      // SCM_DO_BUILD_DURING_DEPLOYMENT=true is set in the deploy workflow so that
      // Oryx installs pip dependencies on the platform side.
    }
  }
}

// ── Outputs ───────────────────────────────────────────────────────────────────
@description('Resource name of the CMS App Service')
output cmsAppName string = cmsApp.name

@description('Resource name of the Agent App Service')
output agentAppName string = agentApp.name

@description('Default hostname of the CMS App Service (without https://)')
output cmsDefaultHostname string = cmsApp.properties.defaultHostName

@description('Default hostname of the Agent App Service (without https://)')
output agentDefaultHostname string = agentApp.properties.defaultHostName

@description('Resource name of the App Service Plan')
output appServicePlanName string = appServicePlan.name
