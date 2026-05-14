# Opening Orkinosai Conversational Agent in Visual Studio

## Important: Technology Stack Clarification

**This is a Python Flask web application, NOT a .NET Blazor project.**

While the problem statement mentions Visual Studio 2026 and Blazor, this repository uses:
- **Python 3.8+** as the programming language
- **Flask** as the web framework
- **HTML/CSS/JavaScript** for the frontend UI
- **Azure OpenAI** for AI capabilities

There are **no .csproj, .sln, or .razor files** because this is not a .NET/Blazor application.

## Recommended Development Environments

### Option 1: Visual Studio Code (Recommended for Python)
**Best choice for Python development** - lightweight, fast, excellent Python support.

### Option 2: PyCharm (Professional Python IDE)
**Best for advanced Python development** - powerful IDE specifically designed for Python.

### Option 3: Visual Studio 2022/2026 with Python Tools
**If you prefer Visual Studio** - requires Python Development workload.

## Opening the Project in Visual Studio 2022/2026

If you prefer to use Visual Studio (2022 or later), follow these steps:

### Prerequisites

1. **Install Visual Studio 2022 or 2026**
   - Download from: https://visualstudio.microsoft.com/

2. **Install Python Development Workload**
   - Open Visual Studio Installer
   - Click "Modify" on your Visual Studio installation
   - Check "Python development" workload
   - Click "Modify" to install

3. **Install Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

### Step-by-Step Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/orkinosai25-org/orkinosai-conversational-agent.git
cd orkinosai-conversational-agent
```

#### 2. Open in Visual Studio

Since this is a Python project without Visual Studio solution files, you have three options:

**Option A: Open as Folder (Recommended)**
1. Launch Visual Studio
2. Click **"Open a local folder"** on the start window
3. Navigate to the cloned repository folder
4. Select the `orkinosai-conversational-agent` folder
5. Click **"Select Folder"**

Visual Studio will automatically detect it's a Python project and configure accordingly.

**Option B: Create a Python Project**
1. Launch Visual Studio
2. Click **"Create a new project"**
3. Search for **"Python Application"**
4. Choose **"From Existing Python Code"**
5. Navigate to the repository folder
6. Select `main.py` as the startup file
7. Click **"Finish"**

**Option C: Open main.py Directly**
1. Launch Visual Studio
2. Go to **File → Open → File**
3. Navigate to the repository folder
4. Open `main.py`
5. Visual Studio will prompt to create a workspace

#### 3. Configure Python Environment

1. **Open Solution Explorer** (View → Solution Explorer)
2. **Right-click on "Python Environments"**
3. **Select "Add Environment"**
4. Choose:
   - **"Virtual environment"** (recommended)
   - Location: Inside your project folder as `venv`
5. Click **"Create"**

#### 4. Install Dependencies

1. **Open Terminal** (View → Terminal or Ctrl+`)
2. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```
3. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

#### 5. Run the Application (F5 Equivalent)

**Method 1: Debug Mode (F5)**
1. Set `main.py` as the startup file (right-click → Set as Startup File)
2. Press **F5** or click **"Start Debugging"** (green arrow)
3. The Flask server will start
4. Open browser to: http://localhost:5000

**Method 2: Without Debugging (Ctrl+F5)**
1. Press **Ctrl+F5** or click **"Start Without Debugging"**
2. Server starts in the terminal
3. Open browser to: http://localhost:5000

**Method 3: Terminal**
1. Open Terminal in Visual Studio
2. Run:
   ```bash
   python main.py
   ```
3. Open browser to: http://localhost:5000

### 6. Access the Full Chat UI

Once the server is running:

1. **Open your web browser**
2. **Navigate to:** `http://localhost:5000`
3. **You should see:** The Orkinosai Conversational Agent welcome screen
4. **Click:** "Start Chatting" button
5. **Type a message** and press Enter or click Send

**Demo Mode**: The app works immediately without Azure credentials using a mock AI client for testing.

## Locating Project Files

Since this is a Python project, there are no traditional `.sln` or `.csproj` files. Instead:

### Main Entry Point
- **File:** `main.py`
- **Location:** Root of the repository
- **Purpose:** Application entry point - run this to start the server

### Project Structure
```
orkinosai-conversational-agent/
├── main.py                    # ← MAIN ENTRY POINT (Run this!)
├── requirements.txt           # Python dependencies
├── appsettings.json          # Configuration file (auto-generated)
├── config.yaml               # Legacy configuration
├── src/
│   ├── agent/                # AI conversation logic
│   │   ├── azure_client.py   # Azure OpenAI integration
│   │   └── conversation.py   # Conversation management
│   ├── api/
│   │   └── app.py           # Flask REST API endpoints
│   └── config/
│       └── settings.py       # Configuration loader
├── static/                   # Frontend assets (CSS, JS)
├── templates/                # HTML templates
├── tests/                    # Unit tests
└── docs/                     # Documentation
```

### Key Files to Know

| File | Purpose |
|------|---------|
| `main.py` | **Start here** - Entry point to run the application |
| `requirements.txt` | Lists all Python dependencies |
| `appsettings.json` | Configuration (auto-created on first run) |
| `src/api/app.py` | Flask application and API routes |
| `src/agent/azure_client.py` | Azure OpenAI client |
| `templates/index.html` | Main chat UI template |
| `README.md` | Comprehensive project documentation |

## What to Do If Files Are Missing

### Scenario 1: No appsettings.json File
**This is normal!** The file is auto-generated on first run.

**Solution:**
1. Run the application once:
   ```bash
   python main.py
   ```
2. The application will automatically create `appsettings.json` with default values
3. Stop the server (Ctrl+C)
4. Edit `appsettings.json` if you need to configure Azure OpenAI

### Scenario 2: Project Files in a Subfolder
If you cloned into a subfolder accidentally:

**Check your current location:**
```bash
cd orkinosai-conversational-agent
ls -la  # Should see main.py, requirements.txt, etc.
```

**If files are nested deeper (only applies if accidentally cloned into a subdirectory):**

Sometimes when cloning, you might accidentally create nested directories with the same name. This is not standard but can happen.

```bash
# Only do this if main.py is not in the current directory
cd orkinosai-conversational-agent/orkinosai-conversational-agent
```

**Verify you're in the right place:**
```bash
# You should see main.py in the current directory
ls main.py
```

### Scenario 3: Missing Dependencies
If imports fail or modules are not found:

**Solution:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Troubleshooting Common Issues

### Issue 1: "Python was not found"

**Symptoms:**
- Error when running `python main.py`
- Command not recognized

**Solution:**
1. Verify Python is installed:
   ```bash
   python --version
   # or
   python3 --version
   ```
2. If not installed, download from https://python.org
3. During installation, check "Add Python to PATH"
4. Restart Visual Studio after installing Python

### Issue 2: "No module named 'flask'" or Import Errors

**Symptoms:**
- ModuleNotFoundError when running the app
- Dependencies not found

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Issue 3: Port 5000 Already in Use

**Symptoms:**
- "Address already in use" error
- Server won't start

**Solution:**

**Option A: Change the port**
1. Edit `appsettings.json`:
   ```json
   {
     "server": {
       "port": 5001
     }
   }
   ```
   Note: Change `5001` to any available port number.
2. Restart the application
3. Access at http://localhost:5001 (or your chosen port)

**Option B: Kill the existing process**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Issue 4: Chat UI Doesn't Load

**Symptoms:**
- Blank page or 404 error
- Static files not loading

**Solution:**
1. Verify server is running:
   ```bash
   curl http://localhost:5000/health
   ```
2. Check browser console for errors (F12)
3. Verify `templates/` and `static/` folders exist
4. Check `logs/agent.log` for server errors

### Issue 5: Chat Doesn't Respond

**Symptoms:**
- Can open UI but messages don't get responses
- Spinner keeps loading

**Solution:**

**For Demo Mode (no Azure):**
- The app should work immediately with mock responses
- Check browser console (F12) for JavaScript errors
- Check `logs/agent.log` for Python errors

**For Azure OpenAI Mode:**
1. Verify `appsettings.json` has valid credentials (not placeholders):
   ```json
   {
     "azure": {
       "openai": {
         "endpoint": "https://your-resource.openai.azure.com/",
         "api_key": "your-actual-key",
         "deployment_name": "your-deployment",
         "api_version": "2024-08-01-preview"
       }
     }
   }
   ```
   **Important:** Replace the example values with your actual Azure credentials.
2. Test Azure connection:
   ```bash
   curl -X POST http://localhost:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "test"}'
   ```
3. Check logs for Azure API errors

### Issue 6: Visual Studio Doesn't Recognize Python

**Symptoms:**
- Can't select Python environment
- No Python options in menus
- Intellisense doesn't work

**Solution:**
1. Open Visual Studio Installer
2. Click "Modify"
3. Check "Python development" workload
4. Install additional components:
   - Python language support
   - Python web support
5. Restart Visual Studio

### Issue 7: Can't Debug/Set Breakpoints

**Symptoms:**
- Breakpoints are hollow (not filled)
- Debugger doesn't attach
- F5 doesn't work

**Solution:**
1. Ensure `main.py` is set as startup file:
   - Right-click `main.py` → "Set as Startup File"
2. Select correct Python environment:
   - Solution Explorer → Python Environments
   - Right-click your `venv` → "Activate Environment"
3. Verify debug configuration:
   - Project → Properties → Debug
   - Script: `main.py`
   - Interpreter: Select your virtual environment

### Issue 8: Missing appsettings.json After First Run

**Symptoms:**
- File should be created but isn't
- App keeps using defaults

**Solution:**
1. Check file permissions - ensure you can write to the directory
2. Run as administrator if needed
3. Manually create `appsettings.json`:
   ```json
   {
     "azure": {
       "openai": {
         "endpoint": "https://your-resource.openai.azure.com/",
         "api_key": "your-api-key",
         "deployment_name": "your-deployment",
         "api_version": "2024-08-01-preview",
         "model": "gpt-4"
       }
     },
     "agent": {
       "name": "Orkinosai Conversational Agent",
       "version": "1.0.0",
       "max_history": 10,
       "temperature": 0.7,
       "max_tokens": 1000,
       "system_prompt": "You are a helpful AI assistant."
     },
     "server": {
       "host": "0.0.0.0",
       "port": 5000,
       "debug": false
     },
     "logging": {
       "file": "logs/agent.log",
       "level": "INFO",
       "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
     }
   }
   ```

## Running Tests

### Run All Tests
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run tests
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_api.py -v
```

### Run in Visual Studio
1. Open **Test Explorer** (View → Test Explorer)
2. Click **"Run All Tests"**
3. View results in the Test Explorer window

## Configuration for Development

### Enable Debug Mode

Edit `appsettings.json` to enable auto-reload and detailed errors:
```json
{
  "server": {
    "debug": true
  }
}
```

### Customize System Prompt

Edit `appsettings.json`:
```json
{
  "agent": {
    "system_prompt": "You are a specialized assistant for..."
  }
}
```

### Adjust AI Parameters

Edit `appsettings.json` to customize AI behavior:
```json
{
  "agent": {
    "temperature": 0.7,
    "max_tokens": 1000,
    "max_history": 10
  }
}
```

Parameter descriptions:
- **temperature**: Controls response creativity (0.0 = focused, 2.0 = creative)
- **max_tokens**: Maximum response length
- **max_history**: Number of conversation messages to keep in context

## Next Steps After Setup

Once you have the application running:

1. **Test the Demo Mode**
   - Open http://localhost:5000
   - Send a message - you should get a demo response

2. **Configure Azure OpenAI (Optional)**
   - Get credentials from Azure Portal
   - Update `appsettings.json`
   - Restart the application

3. **Explore the Code**
   - `src/api/app.py` - API endpoints
   - `src/agent/azure_client.py` - AI integration
   - `templates/index.html` - Frontend UI

4. **Run Tests**
   - Execute `pytest tests/ -v`
   - All tests should pass

5. **Read Documentation**
   - [README.md](README.md) - Project overview
   - [SETUP.md](SETUP.md) - Detailed setup guide
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [QUICKSTART.md](QUICKSTART.md) - 2-minute quick start

## Alternative IDEs

### Visual Studio Code (Recommended)

**Advantages:**
- Lightweight and fast
- Excellent Python extension
- Built-in terminal
- Free and open-source

**Setup:**
1. Install VS Code: https://code.visualstudio.com/
2. Install Python extension by Microsoft
3. Open folder: File → Open Folder
4. Select Python interpreter: Ctrl+Shift+P → "Python: Select Interpreter"
5. Run: Press F5 or use integrated terminal

### PyCharm

**Advantages:**
- Professional Python IDE
- Advanced debugging and profiling
- Excellent code completion
- Database tools

**Setup:**
1. Install PyCharm: https://www.jetbrains.com/pycharm/
2. Open project: File → Open
3. Configure interpreter: File → Settings → Project → Python Interpreter
4. Run: Right-click `main.py` → Run 'main'

## Additional Resources

- **Official Documentation:** [README.md](README.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Full Setup Guide:** [SETUP.md](SETUP.md)
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Azure Deployment:** [docs/AZURE_DEPLOYMENT.md](docs/AZURE_DEPLOYMENT.md)

## Summary

### Key Points to Remember

1. ✅ **This is a Python Flask app, not a .NET Blazor project**
2. ✅ **No .sln or .csproj files exist (this is normal)**
3. ✅ **Run `main.py` to start the server**
4. ✅ **Works out of the box in demo mode (no Azure required)**
5. ✅ **Access the UI at http://localhost:5000**
6. ✅ **F5 in Visual Studio works for debugging**
7. ✅ **VS Code or PyCharm are recommended alternatives**

### Quick Command Reference

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Run
python main.py

# Test
pytest tests/ -v

# Access
http://localhost:5000
```

## Getting Help

If you encounter issues not covered in this guide:

1. Check [SETUP.md](SETUP.md) for detailed configuration
2. Review [README.md](README.md) for project overview
3. Check `logs/agent.log` for error messages
4. Open an issue on GitHub with:
   - Steps to reproduce
   - Error messages
   - Your environment (OS, Python version, Visual Studio version)

---

**Happy Coding! 🚀**
