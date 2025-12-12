"""Mock AI client for demo purposes without Azure credentials."""

import logging
import time
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class MockAIClient:
    """Mock client that simulates Azure OpenAI responses."""
    
    def __init__(self, settings):
        """Initialize mock client.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.agent_config = settings.agent
        logger.info("Initialized Mock AI client (demo mode)")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Generate a mock chat completion.
        
        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            stream: Whether to stream
            
        Returns:
            Mock response dictionary
        """
        try:
            # Get the last user message
            user_message = ""
            for msg in reversed(messages):
                if msg["role"] == "user":
                    user_message = msg["content"]
                    break
            
            # Generate a simple response
            response_content = self._generate_mock_response(user_message)
            
            # Simulate token usage
            prompt_tokens = sum(len(msg["content"].split()) for msg in messages)
            completion_tokens = len(response_content.split())
            
            result = {
                "id": f"mock-{int(time.time())}",
                "model": "mock-gpt-4",
                "created": int(time.time()),
                "content": response_content,
                "role": "assistant",
                "finish_reason": "stop",
                "usage": {
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": prompt_tokens + completion_tokens
                }
            }
            
            logger.info(f"Generated mock completion with {result['usage']['total_tokens']} tokens")
            return result
            
        except Exception as e:
            logger.error(f"Error generating mock completion: {str(e)}")
            raise
    
    def _generate_mock_response(self, user_message: str) -> str:
        """Generate a contextual mock response.
        
        Args:
            user_message: The user's message
            
        Returns:
            Mock response string
        """
        message_lower = user_message.lower()
        
        # Contextual responses
        if "hello" in message_lower or "hi" in message_lower:
            return "Hello! I'm Papagan, The Chatter Parrot! I'm currently running in demo mode without Azure OpenAI credentials. How can I help you today?"
        
        elif "help" in message_lower or "what can you do" in message_lower:
            return """I'm an AI-powered conversational agent designed to help automate SaaS operations. I can:

• Chat with you and maintain conversation context
• Learn from web URLs you provide
• Process and learn from uploaded documents
• Help with onboarding and operational workflows
• Provide assistance with various tasks

Currently running in demo mode. To unlock full capabilities, configure Azure OpenAI credentials in your .env file."""
        
        elif "train" in message_lower or "learn" in message_lower:
            return "You can train me by uploading documents or providing URLs through the Training panel. I'll process the content and use it to provide better responses tailored to your needs."
        
        elif "document" in message_lower or "upload" in message_lower:
            return "To upload documents for training, click the 'Documents' button in the top navigation bar. I can process various document formats including PDF, DOC, DOCX, and TXT files."
        
        elif "url" in message_lower or "website" in message_lower:
            return "To train me from a website, click the 'Training' button in the top navigation and enter the URL. I'll fetch and learn from the content on that page."
        
        elif "azure" in message_lower or "openai" in message_lower:
            return "I'm designed to work with Azure OpenAI Service for advanced AI capabilities. To enable full functionality, add your Azure OpenAI credentials to the .env file. Currently, I'm running in demo mode with simulated responses."
        
        elif "thank" in message_lower:
            return "You're welcome! Feel free to ask me anything else or explore the training features to customize my responses."
        
        elif "bye" in message_lower or "goodbye" in message_lower:
            return "Goodbye! Feel free to come back anytime. I'm here to help 24/7!"
        
        else:
            # Generic response for other queries
            return f"I understand you're asking about: '{user_message}'. In full mode with Azure OpenAI, I would provide a detailed, intelligent response. Currently running in demo mode. You can still explore the UI features like document upload and URL training!"
    
    def get_system_message(self) -> Dict[str, str]:
        """Get the system message.
        
        Returns:
            System message dictionary
        """
        return {
            "role": "system",
            "content": self.agent_config.system_prompt
        }
