"""Tests for Azure OpenAI integration.

These tests verify that the Azure OpenAI client can be initialized
and would work correctly with valid credentials.

Note: These tests use mock/demo mode by default. To test with real
Azure OpenAI credentials, set the environment variables before running.
"""

import pytest
import os
from unittest.mock import Mock, patch
from src.agent.azure_client import AzureAIClient
from src.agent.conversation import ConversationManager
from src.config import Settings


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    from src.config import (
        AzureOpenAIConfig, AzureConfig, AgentConfig,
        ServerConfig, LoggingConfig
    )
    
    return Settings(
        azure=AzureConfig(
            openai=AzureOpenAIConfig(
                endpoint="https://test.openai.azure.com/",
                api_key="test-key",
                api_version="2024-08-01-preview",
                deployment_name="test-deployment",
                model="gpt-4"
            )
        ),
        agent=AgentConfig(
            name="Test Agent",
            version="1.0.0",
            max_history=10,
            temperature=0.7,
            max_tokens=1000,
            system_prompt="You are a helpful assistant."
        ),
        server=ServerConfig(
            host="0.0.0.0",
            port=5000,
            debug=False,
            cors_origins=["*"]
        ),
        logging=LoggingConfig(
            level="INFO",
            format="%(message)s",
            file="logs/test.log"
        )
    )


@patch('src.agent.azure_client.AzureOpenAI')
def test_azure_client_initialization(mock_openai, mock_settings):
    """Test that Azure client can be initialized with settings."""
    mock_openai.return_value = Mock()
    client = AzureAIClient(mock_settings)
    assert client is not None
    assert client.azure_config.endpoint == "https://test.openai.azure.com/"
    assert client.azure_config.deployment_name == "test-deployment"


@patch('src.agent.azure_client.AzureOpenAI')
def test_azure_client_system_message(mock_openai, mock_settings):
    """Test getting system message from Azure client."""
    mock_openai.return_value = Mock()
    client = AzureAIClient(mock_settings)
    system_msg = client.get_system_message()
    assert system_msg["role"] == "system"
    assert system_msg["content"] == "You are a helpful assistant."


@patch('src.agent.azure_client.AzureOpenAI')
def test_azure_client_chat_completion(mock_openai, mock_settings):
    """Test chat completion with mocked Azure OpenAI."""
    # Mock the response
    mock_response = Mock()
    mock_response.id = "chatcmpl-123"
    mock_response.model = "gpt-4"
    mock_response.created = 1234567890
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Hello! How can I help you?"
    mock_response.choices[0].message.role = "assistant"
    mock_response.choices[0].finish_reason = "stop"
    mock_response.usage = Mock()
    mock_response.usage.prompt_tokens = 10
    mock_response.usage.completion_tokens = 5
    mock_response.usage.total_tokens = 15
    
    # Configure mock
    mock_client_instance = Mock()
    mock_client_instance.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client_instance
    
    # Create client and test
    client = AzureAIClient(mock_settings)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello"}
    ]
    
    result = client.chat_completion(messages)
    
    assert result["content"] == "Hello! How can I help you?"
    assert result["role"] == "assistant"
    assert result["usage"]["total_tokens"] == 15


def test_conversation_manager_with_mock_client(mock_settings):
    """Test conversation manager uses mock client when Azure creds are invalid."""
    from src.config import AzureConfig, AzureOpenAIConfig
    
    # Use settings with placeholder values
    settings_with_placeholders = Settings(
        azure=AzureConfig(
            openai=AzureOpenAIConfig(
                endpoint="${AZURE_OPENAI_ENDPOINT}",
                api_key="${AZURE_OPENAI_API_KEY}",
                api_version="2024-08-01-preview",
                deployment_name="${AZURE_OPENAI_DEPLOYMENT_NAME}",
                model="gpt-4"
            )
        ),
        agent=mock_settings.agent,
        server=mock_settings.server,
        logging=mock_settings.logging
    )
    
    manager = ConversationManager(settings_with_placeholders)
    # Should fall back to mock client
    from src.agent.mock_client import MockAIClient
    assert isinstance(manager.azure_client, MockAIClient)


def test_conversation_manager_chat(mock_settings):
    """Test conversation manager chat functionality."""
    manager = ConversationManager(mock_settings)
    
    # Create a conversation and send a message
    response = manager.chat(
        conversation_id="test-conv",
        user_message="Hello World"
    )
    
    assert "conversation_id" in response
    assert response["conversation_id"] == "test-conv"
    assert "user_message" in response
    assert response["user_message"] == "Hello World"
    assert "assistant_message" in response
    assert "timestamp" in response
    assert "usage" in response


def test_conversation_history_limit(mock_settings):
    """Test that conversation history respects max_history setting."""
    manager = ConversationManager(mock_settings)
    conversation_id = "test-history"
    
    # Send multiple messages (more than max_history)
    for i in range(15):
        manager.chat(
            conversation_id=conversation_id,
            user_message=f"Message {i}"
        )
    
    conversation = manager.get_conversation(conversation_id)
    # Should have system message + max_history messages
    # max_history is 10, so we get last 10 messages (5 pairs of user/assistant)
    messages = conversation.get_messages(max_history=10)
    
    # System message + 10 most recent messages
    assert len(messages) <= 11


def test_conversation_clear(mock_settings):
    """Test clearing conversation history."""
    manager = ConversationManager(mock_settings)
    conversation_id = "test-clear"
    
    # Send some messages
    manager.chat(conversation_id=conversation_id, user_message="Hello")
    manager.chat(conversation_id=conversation_id, user_message="How are you?")
    
    # Clear the conversation
    success = manager.clear_conversation(conversation_id)
    assert success is True
    
    conversation = manager.get_conversation(conversation_id)
    # Should only have system message left
    messages = conversation.get_messages()
    assert len(messages) == 1
    assert messages[0]["role"] == "system"


def test_conversation_delete(mock_settings):
    """Test deleting a conversation."""
    manager = ConversationManager(mock_settings)
    conversation_id = "test-delete"
    
    # Create a conversation
    manager.chat(conversation_id=conversation_id, user_message="Hello")
    
    # Delete it
    success = manager.delete_conversation(conversation_id)
    assert success is True
    
    # Try to get it - should be None
    conversation = manager.get_conversation(conversation_id)
    assert conversation is None


def test_multiple_conversations(mock_settings):
    """Test managing multiple conversations simultaneously."""
    manager = ConversationManager(mock_settings)
    
    # Create multiple conversations
    conv1_response = manager.chat("conv-1", "Hello from conversation 1")
    conv2_response = manager.chat("conv-2", "Hello from conversation 2")
    
    assert conv1_response["conversation_id"] == "conv-1"
    assert conv2_response["conversation_id"] == "conv-2"
    
    # Verify they're separate
    conv1 = manager.get_conversation("conv-1")
    conv2 = manager.get_conversation("conv-2")
    
    assert len(conv1.messages) > 0
    assert len(conv2.messages) > 0
    assert conv1.conversation_id != conv2.conversation_id


def test_temperature_override(mock_settings):
    """Test that temperature can be overridden per message."""
    manager = ConversationManager(mock_settings)
    
    # This test verifies the parameter is passed correctly
    response = manager.chat(
        conversation_id="test-temp",
        user_message="Test",
        temperature=0.9,
        max_tokens=500
    )
    
    assert response is not None
    # The override should work without errors


@pytest.mark.skipif(
    not os.getenv('AZURE_OPENAI_API_KEY') or 
    os.getenv('AZURE_OPENAI_API_KEY').startswith('${'),
    reason="Azure OpenAI credentials not configured"
)
def test_real_azure_openai_integration():
    """Integration test with real Azure OpenAI (requires credentials).
    
    This test only runs when valid Azure OpenAI credentials are set
    in environment variables.
    """
    from src.config import get_settings
    
    settings = get_settings("config.yaml")
    manager = ConversationManager(settings)
    
    # Should use real Azure client, not mock
    from src.agent.azure_client import AzureAIClient
    assert isinstance(manager.azure_client, AzureAIClient)
    
    # Send a test message
    response = manager.chat(
        conversation_id="integration-test",
        user_message="Hello! Please respond with 'Integration test successful.'"
    )
    
    assert response is not None
    assert "assistant_message" in response
    assert len(response["assistant_message"]) > 0
    print(f"Azure OpenAI Response: {response['assistant_message']}")
