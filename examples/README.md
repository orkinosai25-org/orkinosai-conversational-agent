# Examples

This directory contains example scripts and test pages demonstrating how to use and embed the SiteChat Agent chat widget.

## Prerequisites

1. Start the agent server:
   ```bash
   python main.py
   ```

2. Ensure the server is running on `http://localhost:5000`

## Running Examples

### 1. Widget Test Page (Recommended for Quick Testing)

Open `widget-test.html` in your browser to see a beautiful test page for the chat widget:

```bash
# Open directly in browser
open examples/widget-test.html  # macOS
start examples/widget-test.html  # Windows
xdg-open examples/widget-test.html  # Linux
```

**Features:**
- Beautiful landing page showcasing the widget
- Instructions on how to test the chat
- Connection status indicator
- Examples of how to embed the widget on your website
- "Open Chat" button to launch the widget in a new window

**Perfect for:** Quick demos, testing, and understanding how to embed the widget.

### 2. Embedded Widget Demo

Open `widget-embed-demo.html` in your browser to see the chat widget embedded directly on a webpage:

```bash
# Open directly in browser
open examples/widget-embed-demo.html  # macOS
start examples/widget-embed-demo.html  # Windows
xdg-open examples/widget-embed-demo.html  # Linux
```

**Features:**
- Live embedded chat widget using iframe
- Integration code examples (iframe, popup, full-page)
- Configuration instructions
- Getting started guide
- Real-time connection status

**Perfect for:** Seeing how the widget looks when embedded on a customer website.

### 3. Simple Chat Example (Python Script)

Demonstrates basic conversation functionality via API:

```bash
python examples/simple_chat.py
```

This example shows:
- Health check
- Sending messages
- Managing conversations
- Viewing conversation info
- Clearing conversation history

**Perfect for:** Backend integration and API testing.

## Testing the Chat Widget

### Quick Start Test

1. **Start the backend server:**
   ```bash
   python main.py
   ```
   The server will start on `http://localhost:5000`

2. **Open a test page:**
   - For a quick demo: Open `widget-test.html` in your browser
   - For embedded demo: Open `widget-embed-demo.html` in your browser

3. **Test the chat:**
   - Type "Hello" to get a friendly greeting
   - Try "What can you do?" to learn about features
   - Ask "Help" for assistance
   - Explore document upload and URL training features

### Demo Mode vs Production Mode

**Demo Mode (Default):**
- Works immediately without any configuration
- Uses mock AI responses (simulated)
- Perfect for testing UI and integration
- No Azure OpenAI credentials needed

**Production Mode:**
- Requires Azure OpenAI credentials
- Configure in `appsettings.json` or `.env`
- Provides real AI-powered responses
- Full Azure OpenAI capabilities

## Creating Your Own Scripts

You can create your own scripts using the API endpoints:

```python
import requests

# Send a chat message
response = requests.post(
    "http://localhost:5000/chat",
    json={
        "conversation_id": "my-conversation",
        "message": "Hello, AI!",
        "temperature": 0.8,
        "max_tokens": 500
    }
)

result = response.json()
print(result["assistant_message"])
```

## Embedding on External Websites

### Option 1: IFrame Embed
```html
<iframe 
    src="http://localhost:5000" 
    width="100%" 
    height="600px"
    style="border: none; border-radius: 12px;">
</iframe>
```

### Option 2: Popup/Modal
```javascript
function openChat() {
    window.open('http://localhost:5000', 'sitechat-chat', 'width=1200,height=800');
}
```

### Option 3: Full Page Link
```html
<a href="http://localhost:5000">Chat with SiteChat Agent</a>
```

## Configuration

Customize the chat widget in `appsettings.json`:

```json
{
  "agent": {
    "temperature": 0.7,
    "max_tokens": 1000,
    "system_prompt": "You are SiteChat Agent, a helpful AI assistant..."
  },
  "server": {
    "cors_origins": ["*"]  // Configure for production
  }
}
```

See the main README for complete API documentation and deployment instructions.
