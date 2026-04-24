# Stripe Integration Setup Guide

This guide will walk you through setting up Stripe payment processing for the SiteChat Agent CMS subscription tiers.

## Prerequisites

1. A Stripe account (sign up at https://stripe.com)
2. Access to your Stripe Dashboard
3. .NET 10.0 SDK installed

## Step 1: Get Your Stripe API Keys

1. Log in to your Stripe Dashboard at https://dashboard.stripe.com
2. Navigate to **Developers** > **API keys**
3. Copy your **Publishable key** and **Secret key**
   - For testing, use the test mode keys (they start with `pk_test_` and `sk_test_`)
   - For production, switch to live mode and use live keys (they start with `pk_live_` and `sk_live_`)

## Step 2: Create Products and Prices in Stripe

You need to create products and prices for each subscription tier in Stripe:

### Using Stripe Dashboard

1. Navigate to **Products** in your Stripe Dashboard
2. Click **+ Add Product**
3. Create products for each tier:

#### Starter Tier
- **Name:** Starter
- **Description:** Great for personal projects and small businesses
- Click **Add price**
  - **Monthly:** $12.00 USD, Recurring: Monthly
  - **Yearly:** $120.00 USD, Recurring: Yearly
- Copy the Price IDs (e.g., `price_1ABC...`)

#### Pro Tier
- **Name:** Pro
- **Description:** For growing businesses and agencies
- Click **Add price**
  - **Monthly:** $35.00 USD, Recurring: Monthly
  - **Yearly:** $350.00 USD, Recurring: Yearly
- Copy the Price IDs

#### Business Tier
- **Name:** Business
- **Description:** Enterprise-grade features and support
- Click **Add price**
  - **Monthly:** $250.00 USD, Recurring: Monthly
  - **Yearly:** $2,500.00 USD, Recurring: Yearly
- Copy the Price IDs

### Using Stripe CLI (Alternative)

```bash
# Install Stripe CLI
# https://stripe.com/docs/stripe-cli

# Login
stripe login

# Create Starter tier
stripe products create --name="Starter" --description="Great for personal projects"
stripe prices create --product=prod_XXXXX --unit-amount=1200 --currency=usd --recurring[interval]=month
stripe prices create --product=prod_XXXXX --unit-amount=12000 --currency=usd --recurring[interval]=year

# Repeat for Pro and Business tiers
```

## Step 3: Configure Application Settings

### Development (User Secrets)

Use .NET user secrets for local development:

```bash
cd src/cms/Server

# Initialize user secrets
dotnet user-secrets init

# Set Stripe keys
dotnet user-secrets set "Payment:Stripe:SecretKey" "sk_test_YOUR_SECRET_KEY"
dotnet user-secrets set "Payment:Stripe:PublishableKey" "pk_test_YOUR_PUBLISHABLE_KEY"
dotnet user-secrets set "Payment:Stripe:WebhookSecret" "whsec_YOUR_WEBHOOK_SECRET"

# Set price IDs
dotnet user-secrets set "Payment:Stripe:PriceIds:Starter_Monthly" "price_XXXXX"
dotnet user-secrets set "Payment:Stripe:PriceIds:Starter_Yearly" "price_XXXXX"
dotnet user-secrets set "Payment:Stripe:PriceIds:Pro_Monthly" "price_XXXXX"
dotnet user-secrets set "Payment:Stripe:PriceIds:Pro_Yearly" "price_XXXXX"
dotnet user-secrets set "Payment:Stripe:PriceIds:Business_Monthly" "price_XXXXX"
dotnet user-secrets set "Payment:Stripe:PriceIds:Business_Yearly" "price_XXXXX"

# List all secrets
dotnet user-secrets list
```

### Production (Environment Variables or Azure Key Vault)

#### Option 1: Environment Variables

Set these environment variables in your hosting environment:

```bash
Payment__Stripe__SecretKey=sk_live_YOUR_SECRET_KEY
Payment__Stripe__PublishableKey=pk_live_YOUR_PUBLISHABLE_KEY
Payment__Stripe__WebhookSecret=whsec_YOUR_WEBHOOK_SECRET
Payment__Stripe__PriceIds__Starter_Monthly=price_XXXXX
Payment__Stripe__PriceIds__Starter_Yearly=price_XXXXX
Payment__Stripe__PriceIds__Pro_Monthly=price_XXXXX
Payment__Stripe__PriceIds__Pro_Yearly=price_XXXXX
Payment__Stripe__PriceIds__Business_Monthly=price_XXXXX
Payment__Stripe__PriceIds__Business_Yearly=price_XXXXX
```

#### Option 2: Azure Key Vault (Recommended for Production)

```bash
# Create Key Vault
az keyvault create --name your-keyvault --resource-group your-rg --location eastus

# Add secrets
az keyvault secret set --vault-name your-keyvault --name StripeSecretKey --value "sk_live_YOUR_SECRET_KEY"
az keyvault secret set --vault-name your-keyvault --name StripePublishableKey --value "pk_live_YOUR_PUBLISHABLE_KEY"
az keyvault secret set --vault-name your-keyvault --name StripeWebhookSecret --value "whsec_YOUR_WEBHOOK_SECRET"

# Add price IDs
az keyvault secret set --vault-name your-keyvault --name StripePrice-Starter-Monthly --value "price_XXXXX"
# ... repeat for all price IDs
```

## Step 4: Set Up Webhook Endpoint

Webhooks allow Stripe to notify your application about important events (e.g., successful payments, subscription cancellations).

### 1. Configure Webhook in Stripe Dashboard

1. Navigate to **Developers** > **Webhooks** in Stripe Dashboard
2. Click **+ Add endpoint**
3. Set the endpoint URL:
   - Development: Use Stripe CLI for local testing (see below)
   - Production: `https://yourdomain.com/api/webhooks/stripe`
4. Select events to listen to:
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
5. Click **Add endpoint**
6. Copy the **Signing secret** (starts with `whsec_`)

### 2. Test Webhooks Locally with Stripe CLI

```bash
# Forward webhooks to your local server
stripe listen --forward-to localhost:5000/api/webhooks/stripe

# In another terminal, trigger test events
stripe trigger customer.subscription.created
stripe trigger invoice.paid
```

The CLI will display the webhook signing secret - use this for local development.

## Step 5: Update appsettings.json

Your `appsettings.json` should look like this (without sensitive values):

```json
{
  "Payment": {
    "Stripe": {
      "PublishableKey": "",
      "SecretKey": "",
      "WebhookSecret": "",
      "ApiVersion": "2024-11-20.acacia",
      "Currency": "usd",
      "EnableTestMode": true,
      "PriceIds": {
        "Starter_Monthly": "",
        "Starter_Yearly": "",
        "Pro_Monthly": "",
        "Pro_Yearly": "",
        "Business_Monthly": "",
        "Business_Yearly": ""
      }
    }
  }
}
```

**Important:** Never commit actual API keys to source control!

## Step 6: Test the Integration

### 1. Start the Application

```bash
cd src/cms/Server
dotnet run
```

### 2. Test Stripe Test Cards

Use these test card numbers in test mode:
- **Success:** 4242 4242 4242 4242
- **Decline:** 4000 0000 0000 0002
- **Requires Authentication:** 4000 0025 0000 3155

Any future expiration date and any 3-digit CVC will work.

### 3. Test the Flow

1. Navigate to `/pricing` in your application
2. Click "Subscribe Now" on a paid tier
3. Complete the Stripe Checkout form with a test card
4. Verify redirection to `/subscription/success`
5. Check `/subscription` to see your active subscription
6. Test the billing portal from the subscription page
7. Test cancellation functionality

### 4. Monitor Stripe Dashboard

- Check **Payments** to see test payments
- Check **Customers** to see created customer records
- Check **Subscriptions** to see active subscriptions
- Check **Logs** > **Webhooks** to see webhook deliveries

## Step 7: Go Live Checklist

Before going to production:

- [ ] Switch from test mode to live mode in Stripe Dashboard
- [ ] Update all API keys to live keys
- [ ] Create live products and prices
- [ ] Update price IDs in configuration
- [ ] Set up live webhook endpoint
- [ ] Test with real payment methods (use small amounts)
- [ ] Enable Stripe Radar for fraud protection
- [ ] Set up payment retry logic
- [ ] Configure customer emails in Stripe
- [ ] Review Stripe's compliance requirements
- [ ] Enable 3D Secure authentication
- [ ] Set up tax collection if required

## Troubleshooting

### Common Issues

1. **"Stripe SecretKey not configured" error**
   - Ensure API keys are set in user secrets or environment variables
   - Check that the configuration key names match exactly

2. **"Price ID not configured" error**
   - Verify all 6 price IDs are set (3 tiers × 2 intervals)
   - Check that the tier names and intervals match exactly

3. **Webhook signature verification failed**
   - Ensure webhook secret is correct
   - For local development, use Stripe CLI webhook secret
   - Check that webhook endpoint URL is correct

4. **Checkout session creation fails**
   - Verify customer creation is successful
   - Check that price IDs are valid in Stripe
   - Ensure success and cancel URLs are absolute URLs

### Enable Detailed Logging

Update `appsettings.Development.json`:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "SiteChatCMS.Infrastructure.Services.Subscriptions": "Debug"
    }
  }
}
```

## Security Best Practices

1. **Never expose secret keys**
   - Use user secrets for development
   - Use environment variables or Key Vault for production
   - Never commit keys to source control

2. **Verify webhook signatures**
   - Always validate webhook signatures (already implemented)
   - Reject unsigned webhook requests

3. **Use HTTPS in production**
   - Stripe requires HTTPS for webhook endpoints
   - Enable HSTS in production

4. **Implement rate limiting**
   - Protect API endpoints from abuse
   - Configure in Program.cs (already available)

5. **Handle PCI compliance**
   - Never store card details directly
   - Use Stripe Checkout or Stripe Elements
   - Let Stripe handle sensitive data

## Additional Resources

- [Stripe Documentation](https://stripe.com/docs)
- [Stripe API Reference](https://stripe.com/docs/api)
- [Stripe Testing](https://stripe.com/docs/testing)
- [Stripe CLI](https://stripe.com/docs/stripe-cli)
- [Webhook Best Practices](https://stripe.com/docs/webhooks/best-practices)
- [SCA/3D Secure](https://stripe.com/docs/strong-customer-authentication)

## Support

For issues specific to this integration:
1. Check the application logs
2. Review Stripe Dashboard logs
3. Consult this documentation
4. Contact the development team

For Stripe-specific questions:
- Stripe Support: https://support.stripe.com
- Stripe Discord: https://stripe.com/discord
