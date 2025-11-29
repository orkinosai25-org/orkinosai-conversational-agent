"""Simple example of using the conversational agent."""

import requests
import json


def main():
    """Demonstrate basic chat functionality."""
    base_url = "http://localhost:5000"
    
    # Check health
    print("Checking agent health...")
    response = requests.get(f"{base_url}/health")
    print(f"Health: {response.json()}\n")
    
    # Start a conversation
    conversation_id = "example-conversation"
    
    # Send first message
    print("User: Hello! What can you help me with?")
    response = requests.post(
        f"{base_url}/chat",
        json={
            "conversation_id": conversation_id,
            "message": "Hello! What can you help me with?"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Assistant: {data['assistant_message']}\n")
        print(f"Tokens used: {data['usage']['total_tokens']}\n")
    else:
        print(f"Error: {response.text}")
        return
    
    # Send follow-up message
    print("User: Can you explain what Azure OpenAI is?")
    response = requests.post(
        f"{base_url}/chat",
        json={
            "conversation_id": conversation_id,
            "message": "Can you explain what Azure OpenAI is?"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Assistant: {data['assistant_message']}\n")
    
    # Get conversation info
    print("Getting conversation info...")
    response = requests.get(f"{base_url}/conversations/{conversation_id}")
    if response.status_code == 200:
        print(f"Conversation: {json.dumps(response.json(), indent=2)}\n")
    
    # Clear conversation
    print("Clearing conversation...")
    response = requests.post(f"{base_url}/conversations/{conversation_id}/clear")
    if response.status_code == 200:
        print(f"Result: {response.json()['message']}\n")


if __name__ == "__main__":
    main()
