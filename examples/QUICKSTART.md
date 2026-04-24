# SiteChat Agent Widget - Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Start the Server
```bash
python main.py
```
The server will start on `http://localhost:5000`

### Step 2: Test "Hello World"
Open one of these test pages in your browser:
- **Widget Test Page**: `examples/widget-test.html`
- **Embedded Demo**: `examples/widget-embed-demo.html`

### Step 3: Chat with SiteChat Agent
1. Click "Open Chat" or "Start Chatting"
2. Type: **"Hello"**
3. Get response: *"Hello! I'm SiteChat Agent! I'm currently running in demo mode..."*

## ✨ What Works Out of the Box
- ✅ Chat UI with beautiful interface
- ✅ Azure AI integration (demo mode by default)
- ✅ "Hello World" functionality
- ✅ Conversation history
- ✅ Document upload UI
- ✅ URL training UI

## 🔧 Demo Mode vs Production Mode

### Demo Mode (Default - No Setup)
- Works immediately
- Uses mock AI responses
- Perfect for testing
- No Azure credentials needed
- No Azure costs

### Production Mode (Optional)
1. Get Azure OpenAI credentials
2. Edit `appsettings.json`:
```json
{
  "azure": {
    "openai": {
      "endpoint": "https://your-resource.openai.azure.com/",
      "api_key": "your-api-key-here",
      "deployment_name": "your-deployment-name"
    }
  }
}
```
3. Restart server: `python main.py`

## 📦 Embed on Your Website

### Option 1: IFrame (Recommended)
```html
<iframe 
    src="http://localhost:5000" 
    width="100%" 
    height="600px"
    style="border: none; border-radius: 12px;">
</iframe>
```

### Option 2: Popup Window
```html
<button onclick="openChat()">Chat with Us</button>
<script>
function openChat() {
    window.open('http://localhost:5000', 'sitechat-chat', 'width=1200,height=800');
}
</script>
```

### Option 3: Full Page
```html
<a href="http://localhost:5000">Open Chat</a>
```

## 🧪 Test Messages to Try

| Message | Purpose |
|---------|---------|
| `Hello` | Get a friendly greeting |
| `What can you do?` | Learn about features |
| `Help` | Get assistance |
| `How do I train you?` | Learn about training |
| `Tell me about Azure OpenAI` | Learn about AI setup |

## 📱 Features Available

### Core Features
- ✅ Real-time chat
- ✅ Conversation history
- ✅ Message persistence
- ✅ Settings panel (temperature, max tokens)
- ✅ Responsive design

### Training Features (UI Available)
- ✅ Document upload panel
- ✅ URL training panel
- ✅ Training history
- ⚠️ Backend processing (implement as needed)

## 🎨 Customization

### Change AI Personality
Edit `appsettings.json`:
```json
{
  "agent": {
    "system_prompt": "You are a helpful assistant...",
    "temperature": 0.7,
    "max_tokens": 1000
  }
}
```

### Change Colors/Branding
Edit `static/css/style.css`:
```css
:root {
    --primary: #4CAF50;    /* Your brand color */
    --accent: #00BCD4;     /* Your accent color */
}
```

## 🐛 Troubleshooting

### Server won't start
```bash
# Install dependencies
pip install -r requirements.txt

# Try again
python main.py
```

### Chat not responding
1. Check server is running: `http://localhost:5000/health`
2. Check console for errors (F12 in browser)
3. Verify CORS settings in `appsettings.json`

### Test pages won't load
1. Serve via HTTP: `cd examples && python -m http.server 8000`
2. Open: `http://localhost:8000/widget-test.html`

## 📚 More Information

- **Main README**: `../README.md`
- **Examples README**: `README.md`
- **Architecture**: `../ARCHITECTURE.md`
- **Configuration**: `../CONFIGURATION.md`

## 🎯 Next Steps

1. ✅ Test "Hello World" functionality
2. ✅ Explore the test pages
3. ⬜ Configure Azure OpenAI (optional)
4. ⬜ Customize branding
5. ⬜ Implement document processing
6. ⬜ Deploy to production
7. ⬜ Embed on customer websites

## 💡 Tips

- Start with demo mode to test everything
- Use test pages to understand embedding
- Configure Azure for production AI
- Customize system prompt for your use case
- Add your branding to match your website
- Use CORS settings to whitelist customer domains

## 🤝 Support

For issues and questions:
- Check main README.md
- Review TROUBLESHOOTING section
- Check configuration files
- Test with demo mode first

---

Made with ❤️ by SiteChat Agent
