# Examples

This directory contains example scripts demonstrating how to use the Orkinosai Conversational Agent.

## Prerequisites

1. Start the agent server:
   ```bash
   python main.py
   ```

2. Ensure the server is running on `http://localhost:5000`

## Running Examples

### Simple Chat Example

Demonstrates basic conversation functionality:

```bash
python examples/simple_chat.py
```

This example shows:
- Health check
- Sending messages
- Managing conversations
- Viewing conversation info
- Clearing conversation history

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

See the main README for complete API documentation.
