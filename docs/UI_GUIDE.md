# SiteChat Agent - UI Guide

## Overview

The SiteChat Agent features a modern, Azure-style dockable interface designed for intuitive interaction and easy customization. This guide will help you understand and use all the UI features.

## Main Interface Components

### 1. Top Navigation Bar

The top bar provides quick access to all major features:

- **Brand Logo & Name**: Always visible, shows "SiteChat Agent Agent"
- **Menu Button**: Opens/closes the left conversation panel
- **Training Button**: Opens the training panel for URL learning
- **Documents Button**: Opens the document upload panel
- **Login/Register**: Access user authentication (right side)
- **User Info**: Shows logged-in user name and logout option

### 2. Left Sidebar - Conversations Panel

Access your conversation history and manage chats:

- **Toggle**: Click "Menu" button in top nav or close button
- **New Conversation**: Create a fresh conversation
- **Conversation List**: View all your conversations
- **Active Indicator**: Currently selected conversation is highlighted
- **Click to Switch**: Select any conversation to load its history

### 3. Main Chat Area

The central workspace for your conversations:

#### Welcome Screen (Initial View)
- Feature cards showing Self-Learning, Automation, and Quick Setup
- "Start Chatting" button to begin
- Clean, modern design

#### Chat Interface (Active Conversation)
- **Chat Header**: Shows conversation title and actions
- **Message Area**: Scrollable conversation history
- **User Messages**: Appear on the right with blue background
- **Assistant Messages**: Appear on the left with gray background
- **Timestamps**: Each message shows the time sent
- **Input Area**: Multi-line text box for typing messages
- **Send Button**: Paper plane icon to send messages

### 4. Right Sidebar - Settings Panel

Configure your conversation preferences:

- **Toggle**: Click settings icon in chat header or close button
- **Temperature Slider**: Adjust response creativity (0.0 - 1.0)
  - Lower values: More focused and deterministic
  - Higher values: More creative and varied
- **Max Tokens**: Control response length (100 - 4000)
- **Settings persist**: Saved to browser's localStorage

### 5. Training Panel (Floating)

Train the agent with web content:

- **Access**: Click "Training" button in top nav
- **URL Input**: Enter any web URL
- **Learn Button**: Submit URL for processing
- **Status**: Shows success/error messages in bottom bar
- **Close**: X button in panel header

### 6. Documents Panel (Floating)

Upload documents for training:

- **Access**: Click "Documents" button in top nav
- **File Selection**: Choose multiple files
- **Supported Formats**: PDF, DOC, DOCX, TXT
- **Upload Button**: Process and upload selected files
- **Document List**: View previously uploaded documents
- **Delete Option**: Remove documents you no longer need
- **Close**: X button in panel header

### 7. Bottom Status Bar

System status and notifications:

- **Left Side**: Status messages and notifications
- **Right Side**: Connection status indicator
  - Green dot: Connected
  - Red dot: Disconnected
- **Auto-clear**: Status messages clear after 5 seconds

## UI Features in Detail

### Responsive Design

The UI adapts to different screen sizes:

- **Desktop**: All panels visible, full layout
- **Tablet**: Side panels overlay main content when opened
- **Mobile**: Panels stack, optimized for touch

### Docking Behavior

Panels can be opened/closed independently:

- **Left Panel**: Slides in/out from left
- **Right Panel**: Slides in/out from right
- **Floating Panels**: Appear centered, can be closed
- **Smooth Animations**: All transitions are animated

### Keyboard Shortcuts

Improve productivity with keyboard controls:

- **Enter**: Send message (in chat input)
- **Shift + Enter**: New line (in chat input)
- **ESC**: Close modals and panels (planned feature)

## User Authentication

### Registration Flow

1. Click "Register" button in top nav
2. Fill in your name, email, and password
3. Click "Register" button in modal
4. Automatically logged in on success
5. UI updates to show your name

### Login Flow

1. Click "Login" button in top nav
2. Enter your email and password
3. Click "Login" button in modal
4. UI updates to show you're logged in
5. Access to personalized features

### Guest Mode

- Works without logging in
- Limited to demo features
- No conversation persistence
- Perfect for testing

## Chat Interface Usage

### Starting a Conversation

1. Click "Start Chatting" from welcome screen, OR
2. Click "New Conversation" in left panel
3. Type your message in the input box
4. Click send button or press Enter
5. Watch for the assistant's response

### Managing Conversations

- **Clear History**: Click trash icon in chat header
- **Switch Conversations**: Click on any conversation in left panel
- **Delete Conversation**: Clear and close (planned feature)

### Message Features

- **Timestamps**: See when each message was sent
- **Scrollable**: Automatic scroll to latest message
- **Copy-Paste**: Full support for text operations
- **Long Messages**: Scrollable within message bubbles

## Training the Agent

### URL Learning

1. Click "Training" button in top nav
2. Enter a valid URL (e.g., https://example.com)
3. Click "Learn from URL"
4. Wait for confirmation message
5. The agent will use this content in responses

**Use Cases:**
- Company documentation
- Product information
- FAQ pages
- Blog articles
- Technical documentation

### Document Upload

1. Click "Documents" button in top nav
2. Click "Choose Files" and select documents
3. Click "Upload Documents"
4. Wait for confirmation
5. View uploaded documents in the list

**Supported Formats:**
- PDF documents
- Microsoft Word (DOC, DOCX)
- Plain text (TXT)
- More formats coming soon

**Best Practices:**
- Upload relevant documents only
- Keep file sizes reasonable
- Use clear, well-formatted documents
- Organize documents by topic

## Settings and Customization

### Temperature Setting

Controls response creativity:

- **0.0**: Very focused, deterministic responses
- **0.3-0.5**: Balanced, consistent responses
- **0.7**: Default, good mix of creativity and focus
- **0.8-1.0**: More creative, varied responses

**Recommended Values:**
- Technical queries: 0.3
- General conversation: 0.7
- Creative tasks: 0.9

### Max Tokens Setting

Controls response length:

- **100-500**: Short, concise responses
- **1000**: Default, balanced length
- **1500-2000**: Detailed responses
- **2000-4000**: Very comprehensive responses

**Note**: Higher values use more API credits

## Tips and Best Practices

### Getting Better Responses

1. **Be Specific**: Clear questions get better answers
2. **Provide Context**: Share relevant background information
3. **Break Down Complex Questions**: Ask one thing at a time
4. **Use Follow-ups**: Build on previous responses
5. **Adjust Settings**: Experiment with temperature and tokens

### Organizing Conversations

1. **Use Descriptive Names**: Name conversations by topic
2. **Create Separate Chats**: Different topics in different conversations
3. **Clear Old Conversations**: Remove outdated chats
4. **Reference Previous Chats**: Agent remembers conversation history

### Training Effectively

1. **Quality Over Quantity**: Upload relevant, high-quality content
2. **Organize by Topic**: Group related documents
3. **Update Regularly**: Keep training data current
4. **Test Results**: Verify the agent learned correctly

## Troubleshooting

### UI Issues

**Panels Not Opening:**
- Check browser console for errors
- Refresh the page
- Clear browser cache

**Chat Not Responding:**
- Check connection status in bottom bar
- Verify server is running
- Check network connectivity

**Login Not Working:**
- Verify credentials
- Check server logs
- Try guest mode for testing

### Performance Tips

**Slow Loading:**
- Clear browser cache
- Close unnecessary browser tabs
- Check internet connection

**High Memory Usage:**
- Clear old conversations
- Limit message history
- Restart browser

## Accessibility

The UI includes accessibility features:

- **Keyboard Navigation**: Tab through elements
- **Screen Reader Support**: ARIA labels (planned)
- **High Contrast**: Readable color scheme
- **Responsive Text**: Scalable fonts
- **Focus Indicators**: Visible focus states

## Browser Support

Recommended browsers:

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ⚠️ Mobile browsers (basic support)
- ❌ Internet Explorer (not supported)

## Customization

### Theme Customization (Future)

The UI uses CSS variables for easy theming:

```css
:root {
    --primary-color: #0078d4;
    --background: #f3f2f1;
    --surface: #ffffff;
    /* More variables in style.css */
}
```

### Local Development

For UI development:

1. Files are in `/templates` and `/static`
2. Edit HTML: `templates/index.html`
3. Edit CSS: `static/css/style.css`
4. Edit JS: `static/js/app.js`
5. Refresh browser to see changes
6. No build step required!

## Support and Feedback

- **GitHub Issues**: Report bugs and request features
- **Documentation**: See README.md and ARCHITECTURE.md
- **Security**: See SECURITY.md for security concerns
- **Community**: Join discussions on GitHub

## What's Next?

Planned UI improvements:

- [ ] Dark mode theme
- [ ] Mobile app
- [ ] Voice input/output
- [ ] Conversation search
- [ ] Export conversations
- [ ] Rich text formatting
- [ ] Code syntax highlighting
- [ ] File attachments in chat
- [ ] Emoji support
- [ ] Notification system

Stay tuned for updates!
