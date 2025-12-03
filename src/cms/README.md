# Orkinosai CMS - Blazor Web Application

A modern Blazor-based Content Management System with an integrated AI Chat Agent.

## Overview

This is a complete, runnable Blazor CMS project that integrates with the Orkinosai Conversational Agent. The CMS provides a full-featured web interface with an embedded chat agent powered by Azure OpenAI.

## Project Structure

```
src/cms/
├── OrkinosaiCMS.sln          # Visual Studio solution file
├── Server/                    # Server-side Blazor project
│   ├── OrkinosaiCMS.csproj   # Project file
│   ├── Program.cs            # Application entry point
│   ├── Components/           # Blazor components
│   │   ├── Pages/           # Razor pages
│   │   │   ├── Home.razor   # Home page with integrated chat
│   │   │   ├── ChatAgent.razor  # Chat agent component
│   │   │   └── ...
│   │   ├── Layout/          # Layout components
│   │   └── App.razor        # Root application component
│   └── wwwroot/             # Static assets
│       ├── app.css          # Application styles
│       └── ...
└── Client/                   # Client-side WebAssembly project
    └── OrkinosaiCMS.Client.csproj
```

## Requirements

- .NET 10.0 SDK or higher
- Visual Studio 2022 (v17.12+) or Visual Studio 2026
- Python 3.8+ (for the backend chat agent service)

## Getting Started

### Option 1: Visual Studio 2022/2026

1. **Open in Visual Studio**:
   - Double-click `OrkinosaiCMS.sln` to open the solution in Visual Studio
   - Or from Visual Studio: File → Open → Project/Solution → Select `OrkinosaiCMS.sln`

2. **Start the Backend Chat Service** (in a separate terminal):
   ```bash
   # From the repository root
   python main.py
   ```
   This starts the Python Flask backend on http://localhost:5000

3. **Run the Blazor CMS**:
   - Press **F5** or click the "Run" button in Visual Studio
   - The CMS will start and open in your default browser
   - Default URL: https://localhost:7XXX (port may vary)

### Option 2: Command Line

1. **Start the Backend Chat Service** (in terminal 1):
   ```bash
   # From the repository root
   cd /home/runner/work/orkinosai-conversational-agent/orkinosai-conversational-agent
   python main.py
   ```

2. **Run the Blazor CMS** (in terminal 2):
   ```bash
   cd src/cms
   dotnet run --project Server/OrkinosaiCMS.csproj
   ```

3. **Open your browser**:
   - Navigate to the URL shown in the terminal (usually https://localhost:5001)

## Features

### CMS Features
- **Content Management**: Create, edit, and organize content
- **User Management**: Manage users, roles, and permissions
- **Analytics**: Track and analyze content performance
- **Settings**: Customize your CMS experience

### Integrated Chat Agent
- **Real-time Chat**: Interactive conversational interface
- **AI-Powered Responses**: Powered by Azure OpenAI Service
- **Adjustable Settings**: Control temperature and token limits
- **Conversation History**: Track your chat history
- **Demo Mode**: Works without Azure credentials for testing

## Configuration

### Blazor CMS Configuration

The CMS uses standard ASP.NET Core configuration:
- `appsettings.json` - Default settings
- `appsettings.Development.json` - Development settings

### Chat Agent Configuration

The chat agent connects to the Python backend. Configure the backend by editing:
- `appsettings.json` in the repository root
- Or `.env` file for environment variables

See the main [README.md](../../README.md) for detailed backend configuration.

## Building the Project

```bash
# Build the entire solution
cd src/cms
dotnet build

# Restore dependencies
dotnet restore

# Clean build artifacts
dotnet clean
```

## Publishing

To publish the application for deployment:

```bash
cd src/cms
dotnet publish Server/OrkinosaiCMS.csproj -c Release -o ../../publish
```

The published files will be in the `publish` directory.

## Architecture

This Blazor application uses:
- **Blazor Server** for server-side rendering
- **Blazor WebAssembly** for client-side interactivity
- **Auto render mode** for optimal performance
- **HTTP client** to communicate with the Python backend

### Communication Flow

```
User Browser
    ↓
Blazor CMS (Port 5001/7xxx)
    ↓ (HTTP requests)
Python Flask Backend (Port 5000)
    ↓
Azure OpenAI Service
```

## Development

### Adding New Pages

1. Create a new `.razor` file in `Server/Components/Pages/`
2. Add the `@page` directive with the route
3. The page will be automatically available

Example:
```razor
@page "/mypage"

<PageTitle>My Page</PageTitle>

<h1>My New Page</h1>
```

### Modifying the Chat Agent

Edit `Server/Components/Pages/ChatAgent.razor` to customize:
- UI appearance
- API endpoints
- Message formatting
- Settings and controls

### Styling

- Global styles: `Server/wwwroot/app.css`
- Component-specific styles: Use `<style>` blocks in `.razor` files
- Bootstrap is included by default

## Troubleshooting

### Chat Agent Not Working

**Problem**: Chat messages return errors

**Solution**: 
1. Ensure the Python backend is running on http://localhost:5000
2. Check that `python main.py` is running in another terminal
3. Verify Azure OpenAI credentials (or use demo mode)

### Build Errors

**Problem**: Build fails with reference errors

**Solution**:
1. Clean the solution: `dotnet clean`
2. Restore packages: `dotnet restore`
3. Rebuild: `dotnet build`

### Port Conflicts

**Problem**: Port already in use

**Solution**:
1. Change the port in `Server/Properties/launchSettings.json`
2. Or kill the process using the port

## Testing

The application works in **demo mode** without Azure credentials:
1. Start the Python backend: `python main.py`
2. Run the CMS: Press F5 in Visual Studio
3. Navigate to the home page
4. Try the chat interface - it will use mock responses

To test with real AI:
1. Configure Azure OpenAI credentials in `appsettings.json`
2. Restart both the Python backend and the CMS

## License

MIT License - See [LICENSE](../../LICENSE) for details

## Support

For issues and questions:
- Repository Issues: https://github.com/orkinosai25-org/orkinosai-conversational-agent/issues
- Main Documentation: [../../README.md](../../README.md)

## Next Steps

1. Explore the CMS interface
2. Try the chat agent
3. Customize the pages and components
4. Add your own features
5. Deploy to production

Enjoy using Orkinosai CMS! 🚀
