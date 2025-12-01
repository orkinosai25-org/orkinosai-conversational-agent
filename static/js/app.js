// Application State
const appState = {
    currentConversationId: null,
    conversations: new Map(),
    isAuthenticated: false,
    user: null,
    settings: {
        temperature: 0.7,
        maxTokens: 1000
    }
};

// API Base URL
const API_BASE = window.location.origin;

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    checkAuthStatus();
});

function initializeApp() {
    // Load saved settings
    const savedSettings = localStorage.getItem('agentSettings');
    if (savedSettings) {
        appState.settings = JSON.parse(savedSettings);
        document.getElementById('temperature').value = appState.settings.temperature;
        document.getElementById('max-tokens').value = appState.settings.maxTokens;
        updateTemperatureDisplay();
    }
    
    // Check health status
    checkHealth();
}

function setupEventListeners() {
    // Chat input listeners
    const chatInput = document.getElementById('chat-input');
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Settings listeners
    document.getElementById('temperature').addEventListener('input', (e) => {
        appState.settings.temperature = parseFloat(e.target.value);
        updateTemperatureDisplay();
        saveSettings();
    });
    
    document.getElementById('max-tokens').addEventListener('input', (e) => {
        appState.settings.maxTokens = parseInt(e.target.value);
        saveSettings();
    });
}

function updateTemperatureDisplay() {
    document.getElementById('temperature-value').textContent = 
        appState.settings.temperature.toFixed(1);
}

function saveSettings() {
    localStorage.setItem('agentSettings', JSON.stringify(appState.settings));
}

// Panel Management
function togglePanel(panelId) {
    const panel = document.getElementById(`${panelId}-panel`);
    if (panel) {
        panel.classList.toggle('active');
    }
}

function showPanel(panelName) {
    const panel = document.getElementById(`${panelName}-panel`);
    if (panel) {
        panel.style.display = 'block';
    }
}

function closePanel(panelId) {
    const panel = document.getElementById(panelId);
    if (panel) {
        panel.style.display = 'none';
    }
}

// Modal Management
function showLogin() {
    document.getElementById('login-modal').style.display = 'flex';
}

function showRegister() {
    document.getElementById('register-modal').style.display = 'flex';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Authentication
function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('user');
    
    if (token && user) {
        appState.isAuthenticated = true;
        appState.user = JSON.parse(user);
        updateUIForAuthState();
    }
}

function updateUIForAuthState() {
    const userControls = document.getElementById('user-controls');
    const userInfo = document.getElementById('user-info');
    
    if (appState.isAuthenticated) {
        userControls.style.display = 'none';
        userInfo.style.display = 'flex';
        document.getElementById('username-display').textContent = appState.user.name || appState.user.email;
    } else {
        userControls.style.display = 'flex';
        userInfo.style.display = 'none';
    }
}

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            appState.isAuthenticated = true;
            appState.user = data.user;
            updateUIForAuthState();
            closeModal('login-modal');
            showStatus('Logged in successfully', 'success');
        } else {
            const error = await response.json();
            showStatus(error.error || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showStatus('Login failed. Using guest mode.', 'error');
        // Allow guest mode for now
        closeModal('login-modal');
    }
}

async function handleRegister(event) {
    event.preventDefault();
    
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    
    try {
        const response = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('user', JSON.stringify(data.user));
            appState.isAuthenticated = true;
            appState.user = data.user;
            updateUIForAuthState();
            closeModal('register-modal');
            showStatus('Registered successfully', 'success');
        } else {
            const error = await response.json();
            showStatus(error.error || 'Registration failed', 'error');
        }
    } catch (error) {
        console.error('Registration error:', error);
        showStatus('Registration failed. Using guest mode.', 'error');
        // Allow guest mode for now
        closeModal('register-modal');
    }
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    appState.isAuthenticated = false;
    appState.user = null;
    updateUIForAuthState();
    showStatus('Logged out successfully', 'success');
}

// Chat Functions
function newConversation() {
    const conversationId = `conv-${Date.now()}`;
    appState.currentConversationId = conversationId;
    appState.conversations.set(conversationId, {
        id: conversationId,
        messages: [],
        createdAt: new Date()
    });
    
    // Show chat interface
    document.getElementById('welcome-screen').style.display = 'none';
    document.getElementById('chat-interface').style.display = 'flex';
    document.getElementById('conversation-title').textContent = 'New Conversation';
    document.getElementById('chat-messages').innerHTML = '';
    
    // Update conversation list
    updateConversationList();
    
    // Focus input
    document.getElementById('chat-input').focus();
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    if (!appState.currentConversationId) {
        newConversation();
    }
    
    // Clear input and disable send button
    input.value = '';
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    
    // Add user message to UI
    addMessageToUI('user', message);
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
            },
            body: JSON.stringify({
                conversation_id: appState.currentConversationId,
                message: message,
                temperature: appState.settings.temperature,
                max_tokens: appState.settings.maxTokens
            })
        });
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (response.ok) {
            const data = await response.json();
            addMessageToUI('assistant', data.assistant_message);
            
            // Update conversation in state
            const conversation = appState.conversations.get(appState.currentConversationId);
            if (conversation) {
                conversation.messages.push(
                    { role: 'user', content: message, timestamp: new Date() },
                    { role: 'assistant', content: data.assistant_message, timestamp: new Date() }
                );
            }
            
            showStatus('Message sent', 'success');
        } else {
            const error = await response.json();
            showStatus(error.error || 'Failed to send message', 'error');
            addMessageToUI('system', 'Sorry, there was an error processing your message. Please try again.');
        }
    } catch (error) {
        console.error('Send message error:', error);
        removeTypingIndicator(typingId);
        showStatus('Network error', 'error');
        addMessageToUI('system', 'Sorry, there was a connection error. Please check your connection and try again.');
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

function addMessageToUI(role, content) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    
    if (role === 'user') {
        avatar.innerHTML = '<i class="fas fa-user"></i>';
    } else if (role === 'assistant') {
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
    } else {
        avatar.innerHTML = '<i class="fas fa-info-circle"></i>';
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString();
    contentDiv.appendChild(timeDiv);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addTypingIndicator() {
    const messagesContainer = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    const typingId = `typing-${Date.now()}`;
    typingDiv.id = typingId;
    typingDiv.className = 'message assistant-message';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="loading"></div>
            Thinking...
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return typingId;
}

function removeTypingIndicator(typingId) {
    const typingDiv = document.getElementById(typingId);
    if (typingDiv) {
        typingDiv.remove();
    }
}

async function clearChat() {
    if (!appState.currentConversationId) return;
    
    if (!confirm('Are you sure you want to clear this conversation?')) {
        return;
    }
    
    try {
        const response = await fetch(
            `${API_BASE}/conversations/${appState.currentConversationId}/clear`,
            {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
                }
            }
        );
        
        if (response.ok) {
            document.getElementById('chat-messages').innerHTML = '';
            const conversation = appState.conversations.get(appState.currentConversationId);
            if (conversation) {
                conversation.messages = [];
            }
            showStatus('Conversation cleared', 'success');
        }
    } catch (error) {
        console.error('Clear chat error:', error);
        showStatus('Failed to clear conversation', 'error');
    }
}

function updateConversationList() {
    const listContainer = document.getElementById('conversation-list');
    listContainer.innerHTML = '';
    
    appState.conversations.forEach((conv, id) => {
        const item = document.createElement('div');
        item.className = 'conversation-item';
        if (id === appState.currentConversationId) {
            item.classList.add('active');
        }
        
        const title = conv.messages.length > 0 
            ? conv.messages[0].content.substring(0, 30) + '...'
            : 'New Conversation';
        
        item.textContent = title;
        item.onclick = () => switchConversation(id);
        listContainer.appendChild(item);
    });
}

function switchConversation(conversationId) {
    appState.currentConversationId = conversationId;
    const conversation = appState.conversations.get(conversationId);
    
    if (!conversation) return;
    
    // Clear and repopulate messages
    document.getElementById('chat-messages').innerHTML = '';
    conversation.messages.forEach(msg => {
        addMessageToUI(msg.role, msg.content);
    });
    
    // Update UI
    document.getElementById('welcome-screen').style.display = 'none';
    document.getElementById('chat-interface').style.display = 'flex';
    updateConversationList();
}

// Training Functions
async function trainFromURL() {
    const urlInput = document.getElementById('training-url');
    const url = urlInput.value.trim();
    
    if (!url) {
        showStatus('Please enter a URL', 'error');
        return;
    }
    
    try {
        showStatus('Learning from URL...', 'info');
        
        const response = await fetch(`${API_BASE}/training/url`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
            },
            body: JSON.stringify({ url })
        });
        
        if (response.ok) {
            const data = await response.json();
            showStatus(data.message || 'Successfully learned from URL', 'success');
            urlInput.value = '';
        } else {
            const error = await response.json();
            showStatus(error.error || 'Failed to learn from URL', 'error');
        }
    } catch (error) {
        console.error('Train from URL error:', error);
        showStatus('Failed to process URL', 'error');
    }
}

async function uploadDocuments() {
    const fileInput = document.getElementById('document-upload');
    const files = fileInput.files;
    
    if (files.length === 0) {
        showStatus('Please select files to upload', 'error');
        return;
    }
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('documents', files[i]);
    }
    
    try {
        showStatus('Uploading documents...', 'info');
        
        const response = await fetch(`${API_BASE}/training/documents`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
            },
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            showStatus(data.message || 'Documents uploaded successfully', 'success');
            fileInput.value = '';
            loadDocumentList();
        } else {
            const error = await response.json();
            showStatus(error.error || 'Failed to upload documents', 'error');
        }
    } catch (error) {
        console.error('Upload documents error:', error);
        showStatus('Failed to upload documents', 'error');
    }
}

async function loadDocumentList() {
    try {
        const response = await fetch(`${API_BASE}/training/documents`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            displayDocuments(data.documents || []);
        }
    } catch (error) {
        console.error('Load documents error:', error);
    }
}

function displayDocuments(documents) {
    const listContainer = document.getElementById('document-list');
    listContainer.innerHTML = '';
    
    if (documents.length === 0) {
        listContainer.innerHTML = '<p style="color: var(--text-secondary);">No documents uploaded yet</p>';
        return;
    }
    
    documents.forEach(doc => {
        const item = document.createElement('div');
        item.className = 'document-item';
        item.innerHTML = `
            <span><i class="fas fa-file"></i> ${doc.name}</span>
            <button class="icon-btn" onclick="deleteDocument('${doc.id}')">
                <i class="fas fa-trash"></i>
            </button>
        `;
        listContainer.appendChild(item);
    });
}

async function deleteDocument(documentId) {
    if (!confirm('Are you sure you want to delete this document?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/training/documents/${documentId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('authToken') || ''}`
            }
        });
        
        if (response.ok) {
            showStatus('Document deleted', 'success');
            loadDocumentList();
        } else {
            showStatus('Failed to delete document', 'error');
        }
    } catch (error) {
        console.error('Delete document error:', error);
        showStatus('Failed to delete document', 'error');
    }
}

// Health Check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        if (response.ok) {
            const data = await response.json();
            showStatus(`Connected to ${data.agent}`, 'success');
            document.getElementById('connection-status').innerHTML = 
                '<i class="fas fa-circle status-online"></i> Connected';
        } else {
            showStatus('Service unavailable', 'error');
            document.getElementById('connection-status').innerHTML = 
                '<i class="fas fa-circle" style="color: var(--error);"></i> Disconnected';
        }
    } catch (error) {
        console.error('Health check error:', error);
        document.getElementById('connection-status').innerHTML = 
            '<i class="fas fa-circle" style="color: var(--error);"></i> Disconnected';
    }
}

// Status Display
function showStatus(message, type = 'info') {
    const statusText = document.getElementById('status-text');
    statusText.textContent = message;
    
    // Reset color
    statusText.style.color = 'var(--text-secondary)';
    
    if (type === 'success') {
        statusText.style.color = 'var(--success)';
    } else if (type === 'error') {
        statusText.style.color = 'var(--error)';
    }
    
    // Auto-clear after 5 seconds
    setTimeout(() => {
        statusText.textContent = 'Ready';
        statusText.style.color = 'var(--text-secondary)';
    }, 5000);
}

// Periodic health check
setInterval(checkHealth, 30000); // Check every 30 seconds
