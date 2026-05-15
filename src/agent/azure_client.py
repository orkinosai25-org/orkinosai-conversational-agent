"""Azure AI client for conversational agent."""

import logging
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI

from src.config import Settings

logger = logging.getLogger(__name__)


class AzureAIClient:
    """Client for interacting with Azure OpenAI Service."""
    
    def __init__(self, settings: Settings):
        """Initialize Azure AI client.
        
        Args:
            settings: Application settings containing Azure configuration
        """
        self.settings = settings
        self.azure_config = settings.azure.openai
        self.agent_config = settings.agent
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=self.azure_config.api_key,
            api_version=self.azure_config.api_version,
            azure_endpoint=self.azure_config.endpoint
        )
        
        logger.info(f"Initialized Azure AI client with endpoint: {self.azure_config.endpoint}")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        model: Optional[str] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Generate a chat completion.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature (overrides config if provided)
            max_tokens: Maximum tokens to generate (overrides config if provided)
            stream: Whether to stream the response
            
        Returns:
            Response dictionary containing the generated message
        """
        try:
            response = self.client.chat.completions.create(
                model=self.azure_config.deployment_name,
                messages=messages,
                temperature=temperature or self.agent_config.temperature,
                max_tokens=max_tokens or self.agent_config.max_tokens,
                stream=stream
            )
            
            if stream:
                return {"stream": response}
            
            # Extract response content
            result = {
                "id": response.id,
                "model": response.model,
                "requested_model": model or self.azure_config.model,
                "deployment_name": self.azure_config.deployment_name,
                "created": response.created,
                "content": response.choices[0].message.content,
                "role": response.choices[0].message.role,
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                } if response.usage else {}
            }
            
            logger.info(f"Generated completion with {result['usage']['total_tokens']} tokens")
            return result
            
        except Exception as e:
            logger.error(f"Error generating chat completion: {str(e)}")
            raise
    
    def get_system_message(self) -> Dict[str, str]:
        """Get the system message for the agent.
        
        Returns:
            System message dictionary
        """
        return {
            "role": "system",
            "content": self.agent_config.system_prompt
        }
