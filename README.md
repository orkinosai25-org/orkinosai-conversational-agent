# SiteChat Agent

*An AI chat agent for your website. Test it instantly. Embed it or just share a link.*

An Azure AI-powered conversational agent with a modern, colorful dockable UI and RESTful API interface. This project provides a complete scaffolding for building conversational AI applications using Azure OpenAI Service, designed to help startups and founders automate SaaS operations quickly.

## ⚡ Quick Start

### Option 1: Python Web UI (Original)

**Get started in 2 minutes with zero configuration!**

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app - it works immediately!
python main.py
```

Open `http://localhost:5000`, type "hello" and start chatting! The app runs in demo mode without requiring any Azure credentials. See [QUICKSTART.md](QUICKSTART.md) for more details.

### Option 2: Blazor CMS (New - Visual Studio)

**Run the modern Blazor CMS with integrated chat agent!**

1. **Start the backend** (in terminal 1):
   ```bash
   python main.py
   ```

2. **Open in Visual Studio**:
   - Open `src/cms/SiteChatCMS.sln` in Visual Studio 2022/2026
   - Press **F5** to run

The CMS will open in your browser with the chat agent integrated on the home page! See [src/cms/README.md](src/cms/README.md) for more details.

## Features

### Core Features
- 🚀 **Works out of the box** - No configuration required to start!
- 🤖 Azure OpenAI Service integration (with automatic demo mode fallback)
- 💬 Conversation management with history
- 🔧 Flexible configuration via `appsettings.json` and environment variables
- 🌐 RESTful API endpoints
- 📝 Comprehensive logging
- 🔒 Secure credential management
- 🎯 Type-safe with Pydantic models

### New UI Features
- 🦜 **SiteChat Agent Branded UI** - Colorful, friendly interface with parrot mascot
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 👤 **User Authentication** - Built-in login and registration
- 🧠 **URL Learning** - Train the agent by providing web URLs
- 📄 **Document Upload** - Upload and process documents for training
- ⚙️ **Dockable Panels** - Top bar, left/right sidebars, and floating panels
- 💬 **Real-time Chat** - Interactive chat interface with message history
- 🎛️ **Settings Panel** - Adjustable temperature and token limits

### Blazor CMS Features ✨ NEW
- 🌐 **Modern Blazor Web Application** - Built with .NET 10 and Blazor
- 🦜 **Integrated SiteChat Agent** - AI assistant embedded directly in the CMS home page
- 🎨 **SiteChat Agent-Style Dockable Panel** - Colorful, friendly UI with parrot branding
- 🔄 **Dynamic Dock Positioning** - Dock to top, right, bottom, or left with smooth animations
- 📄 **Content Management** - Full-featured CMS for managing content
- 👥 **User Management** - Role-based access control and permissions
- 📊 **Analytics Dashboard** - Track content performance
- ⚡ **Real-time Updates** - Blazor's SignalR for instant updates
- 🎯 **Visual Studio Integration** - Open and run with F5
- 🔄 **Auto & Server Rendering** - Optimal performance with hybrid rendering
- 📦 **Embeddable SaaS Widget** - Reusable chat component for external websites

See [Blazor CMS Documentation](src/cms/README.md) for detailed information on running the CMS in Visual Studio 2022/2026.

### Embeddable SaaS Widget 🔌

SiteChat Agent includes a **reusable, embeddable chat widget** that can be integrated into any website as a SaaS offering. The widget is built as a self-contained Blazor component with SiteChat Agent branding.

#### Key Features of the Widget:
- **🦜 SiteChat Agent Branding** - Friendly, colorful look with the parrot mascot
- **🔄 Dockable Interface** - Users can dock the chat to any screen edge (top, right, bottom, left)
- **⚡ Out-of-the-Box Functionality** - Works immediately with demo mode, no Azure credentials required
- **📱 Fully Responsive** - Optimized for desktop, tablet, and mobile devices
- **🎯 Easy Integration** - Add to any website with minimal configuration
- **🔒 Secure Backend** - All AI processing happens on your secure backend server

#### How to Use the Widget:

**1. As Integrated Component (Current Implementation)**

The widget is fully integrated into the SiteChat Agent CMS home page:

```razor
<!-- In your Blazor page -->
<DockableChatPanel IsOpen="isChatOpen" IsOpenChanged="HandleChatOpenChanged" />

@code {
    private bool isChatOpen = false;
    
    private void HandleChatOpenChanged(bool isOpen)
    {
        isChatOpen = isOpen;
    }
}
```

**2. As Embeddable Widget for External Websites**

To embed the chat widget on external websites:

1. **Host the Backend API** - Deploy the Python backend (`main.py`) to your server
   ```bash
   python main.py
   ```
   The backend will be available at `http://your-domain.com:5000`

2. **Configure CORS** - Ensure the backend allows requests from your customer domains
   ```python
   # In src/api/app.py
   CORS(app, resources={r"/*": {"origins": ["https://customer-site.com"]}})
   ```

3. **Embed the Widget** - Customers can add the widget to their website:

   **Option A: Direct Blazor Component** (for .NET sites)
   ```razor
   @using SiteChatCMS.Components.Pages
   
   <DockableChatPanel IsOpen="true" IsOpenChanged="@((open) => {})" />
   ```

   **Option B: IFrame Embed** (for any website)
   ```html
   <!-- Add to any HTML page -->
   <iframe 
       src="https://your-cms-domain.com/chat-widget" 
       width="100%" 
       height="600px"
       style="border: none; position: fixed; bottom: 20px; right: 20px; 
              width: 420px; height: 600px; z-index: 9999;">
   </iframe>
   ```

   **Option C: JavaScript Widget** (coming soon)
   ```html
   <script src="https://your-domain.com/sitechat-widget.js"></script>
   <script>
     SiteChatWidget.init({
       apiUrl: 'https://your-backend.com',
       dockPosition: 'right',
       theme: 'sitechat'
     });
   </script>
   ```

**3. Widget Configuration Options**

The widget supports various configuration parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `IsOpen` | bool | false | Initial open/closed state |
| `DockPosition` | enum | Right | Initial dock position (Top, Right, Bottom, Left) |
| `Temperature` | double | 0.7 | AI response creativity (0.0 - 1.0) |
| `MaxTokens` | int | 1000 | Maximum response length |
| `ApiUrl` | string | http://localhost:5000 | Backend API URL |

**4. Styling and Branding**

The widget uses SiteChat Agent design system colors and can be customized:

```css
/* Override widget styles */
:root {
    --sitechat-green: #4CAF50;
    --sitechat-green-dark: #2E7D32;
    --sitechat-cyan: #00BCD4;
    --sitechat-teal: #0097A7;
}
```

**5. Mobile Optimization**

The widget is fully responsive and optimized for mobile devices:
- Automatically fills the screen width on mobile
- Touch-friendly controls
- Optimized message bubbles
- Adaptive dock controls (hidden on very small screens)

#### Use Cases for the Widget:

1. **Customer Support** - Add AI-powered support to any website
2. **SaaS Product** - Offer the chat agent as a white-label SaaS service
3. **Internal Tools** - Integrate into corporate portals and intranets
4. **E-commerce** - Provide shopping assistance on online stores
5. **Documentation Sites** - Help users navigate documentation

#### Demo Mode

The widget works out-of-the-box in demo mode without requiring Azure OpenAI credentials, making it perfect for:
- Testing and development
- Demonstrations to clients
- Prototyping before Azure setup
- Development environments

## SaaS Pricing & Product Roadmap

This project is being developed as **SiteChat Agent** - a commercial SaaS offering with multiple pricing tiers. Our product documentation includes:

- 📋 **[PRICING.md](PRICING.md)** - Complete SaaS pricing tiers (Free, Starter, Pro, Business, Enterprise) with detailed feature breakdowns for:
  - Knowledge sources and limits
  - Supported AI models (GPT-4o, Gemini, Claude, BYOK, on-prem LLMs)
  - Integrations (M365/SharePoint, Salesforce, HubSpot, Shopify, etc.)
  - Conversation, usage, and seat limits
  - Branding and customization options
  - Compliance, support, and SLA guarantees

- 🛠️ **[ENGINEERING_BACKLOG.md](ENGINEERING_BACKLOG.md)** - Comprehensive engineering backlog with 12 epics and 60+ user stories:
  - SharePoint/M365 Integration
  - AI Model Support & Management
  - Anti-Hallucination & Citation System
  - Multi-Tenant Analytics
  - Team Management & Collaboration
  - Advanced Embed & Widget Features
  - Bring-Your-Own-Model Support
  - White-Labeling & Customization
  - SSO & Advanced Authentication
  - Audit Logs & Compliance
  - Enterprise Onboarding
  - Public/Private API with SLAs

These documents provide a clear roadmap for implementation teams and define how features align with pricing tiers.

## Architecture

This project follows a **domain-partitioned architecture** separating:
- **CMS Domain**: Generic, reusable features (user management, roles, billing, etc.) - to be synced with sitechatcms
- **Agent Domain**: AI-specific features (chat, Azure OpenAI, conversations)

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation, including:
- Domain separation strategy
- CMS-Agent synchronization guidelines
- Development workflow and best practices
- Integration patterns

**Important**: All CMS domain features must be copied from [sitechatcms](https://github.com/orkinosai25-org/sitechatcms) before implementing agent-specific features.

## Prerequisites

- Python 3.8 or higher
- (Optional) Azure OpenAI Service account and deployment for production use

## IDE Setup

**New to the project?** Choose your preferred development environment:

- **[Visual Studio 2022/2026 Setup Guide](VISUAL_STUDIO_GUIDE.md)** - Step-by-step instructions for opening and running this Python Flask project in Visual Studio
- **[Quick Start Guide](QUICKSTART.md)** - Get running in 2 minutes with any IDE
- **[Full Setup Guide](SETUP.md)** - Comprehensive setup and configuration

**Note:** This is a Python Flask application, not a .NET Blazor project. See the Visual Studio Guide for clarification and proper setup instructions.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/orkinosai25-org/sitechat-agent.git
cd sitechat-agent
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

4. **Optional**: Configure Azure OpenAI credentials (see Configuration section below)

## Configuration

### Quick Setup (Works Out of the Box!)

The application works immediately after installation with **no configuration required**! 

When you first run the application, it automatically creates an `appsettings.json` file with default placeholder values and runs in **demo mode** using a mock AI client. This means:

- ✅ Chat interface works immediately
- ✅ You can test the UI without Azure credentials
- ✅ Perfect for development and demonstrations
- ✅ No Azure costs during testing

### Connecting to Azure OpenAI

To enable full AI capabilities with Azure OpenAI, edit the auto-generated `appsettings.json` file:

```json
{
  "azure": {
    "openai": {
      "endpoint": "https://your-resource-name.openai.azure.com/",
      "api_key": "your-api-key-here",
      "deployment_name": "your-deployment-name",
      "api_version": "2024-08-01-preview",
      "model": "gpt-4"
    }
  }
}
```

**To get your Azure OpenAI credentials:**

1. Log in to [Azure Portal](https://portal.azure.com)
2. Navigate to your Azure OpenAI resource
3. Go to "Keys and Endpoint" section
4. Copy the endpoint URL and API key
5. Go to "Model deployments" to find your deployment name
6. Update the values in `appsettings.json`
7. Restart the application

### Alternative: Environment Variables

You can also use environment variables (which override `appsettings.json`):

```bash
cp .env.example .env
# Edit .env with your Azure credentials
```

```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-08-01-preview
```

### Legacy Configuration

The application still supports the legacy `config.yaml` format for backward compatibility. However, `appsettings.json` is now the recommended configuration method and takes precedence when present.

## Usage

### Starting the Server

Run the API server:

```bash
python main.py
```

The server will start on `http://localhost:5000` by default.

### Accessing the Web UI

Open your browser and navigate to `http://localhost:5000` to access the modern Azure-style UI.

**Demo Mode**: The application works in demo mode without Azure credentials, using a mock AI client for testing the interface. To enable full Azure OpenAI capabilities, configure your `.env` file with valid Azure credentials.

#### UI Features:

1. **Welcome Screen**: Overview of features with "Start Chatting" button
2. **Chat Interface**: Real-time conversational interface with message history
3. **Left Panel (Menu)**: Access conversation history and create new conversations
4. **Right Panel (Settings)**: Adjust temperature and max tokens
5. **Training Panel**: Learn from web URLs by entering the URL
6. **Documents Panel**: Upload documents (PDF, DOC, DOCX, TXT) for training
7. **Top Navigation**: Quick access to all features, login/register
8. **Bottom Status Bar**: Connection status and system messages

### API Endpoints

#### Health Check
```bash
GET /health
```

Response:
```json
{
  "status": "healthy",
  "agent": "SiteChat Agent",
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

#### User Registration
```bash
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure-password"
}
```

Response:
```json
{
  "message": "User registered successfully",
  "token": "auth-token",
  "user": {
    "id": "user-id",
    "email": "john@example.com",
    "name": "John Doe"
  }
}
```

#### User Login
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure-password"
}
```

#### Train from URL
```bash
POST /training/url
Content-Type: application/json

{
  "url": "https://example.com/documentation"
}
```

Response:
```json
{
  "message": "Successfully learned from URL: https://example.com/documentation",
  "training_id": "training-id"
}
```

#### Upload Documents
```bash
POST /training/documents
Content-Type: multipart/form-data

documents: [file1.pdf, file2.docx]
```

Response:
```json
{
  "message": "Successfully uploaded 2 document(s)",
  "documents": [
    {"id": "doc-id-1", "name": "file1.pdf"},
    {"id": "doc-id-2", "name": "file2.docx"}
  ]
}
```

#### Get Documents
```bash
GET /training/documents
```

#### Delete Document
```bash
DELETE /training/documents/{document_id}
```

## Project Structure

```
sitechat-agent/
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
│   └── cms/                     # CMS DOMAIN (Blazor Web Application)
│       ├── SiteChatCMS.sln      # Visual Studio solution
│       ├── Server/             # Blazor server project
│       │   ├── Components/     # Razor components and pages
│       │   └── wwwroot/        # Static web assets
│       └── Client/             # Blazor WebAssembly client
├── tests/                       # Test directory
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # Architecture and domain partitioning
│   ├── CMS_FEATURES_INVENTORY.md # CMS features to be copied
│   ├── CMS_SYNC_LOG.md          # Sync history with sitechatcms
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

**Note**: The `src/cms/` directory contains a complete Blazor CMS application with integrated chat agent. See [src/cms/README.md](src/cms/README.md) for details on running the CMS.

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