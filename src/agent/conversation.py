"""Conversation management for the agent."""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import uuid

from src.config import Settings
from .azure_client import AzureAIClient
from .mock_client import MockAIClient
from .routing import (
    DEFAULT_FALLBACK_MODEL,
    DEFAULT_PRIMARY_MODEL,
    DEFAULT_ROUTING_MODE,
    MessageRouter,
)

logger = logging.getLogger(__name__)


class Conversation:
    """Represents a single conversation session."""
    
    def __init__(self, conversation_id: Optional[str] = None, system_prompt: Optional[str] = None):
        """Initialize a conversation.
        
        Args:
            conversation_id: Unique identifier for the conversation
            system_prompt: Optional system prompt override
        """
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.messages: List[Dict[str, str]] = []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.selected_model = DEFAULT_PRIMARY_MODEL
        self.fallback_model = DEFAULT_FALLBACK_MODEL
        self.routing_mode = DEFAULT_ROUTING_MODE
        
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
        """
        self.messages.append({"role": role, "content": content})
        self.updated_at = datetime.utcnow()
        logger.debug(f"Added {role} message to conversation {self.conversation_id}")
    
    def get_messages(self, max_history: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation messages.
        
        Args:
            max_history: Maximum number of messages to return (excluding system message)
            
        Returns:
            List of message dictionaries
        """
        if max_history is None:
            return self.messages.copy()
        
        # Separate system messages from conversation messages
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        other_messages = [msg for msg in self.messages if msg["role"] != "system"]
        
        # Return system messages + last N messages
        return system_messages + other_messages[-max_history:]
    
    def clear(self) -> None:
        """Clear conversation history (keeping system message if present)."""
        system_messages = [msg for msg in self.messages if msg["role"] == "system"]
        self.messages = system_messages
        self.updated_at = datetime.utcnow()
        logger.info(f"Cleared conversation {self.conversation_id}")


class ConversationManager:
    """Manages conversations and interactions with Azure AI."""
    
    def __init__(self, settings: Settings):
        """Initialize conversation manager.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        
        # Try to initialize Azure client, fall back to mock if credentials missing
        try:
            if (settings.azure.openai.api_key and 
                settings.azure.openai.api_key != "${AZURE_OPENAI_API_KEY}" and
                settings.azure.openai.endpoint and 
                settings.azure.openai.endpoint != "${AZURE_OPENAI_ENDPOINT}"):
                self.azure_client = AzureAIClient(settings)
                logger.info("Using Azure OpenAI client")
            else:
                self.azure_client = MockAIClient(settings)
                logger.info("Using Mock AI client (demo mode)")
        except Exception as e:
            logger.warning(f"Failed to initialize Azure client, using mock: {str(e)}")
            self.azure_client = MockAIClient(settings)
        
        self.conversations: Dict[str, Conversation] = {}
        self.router = MessageRouter()
        logger.info("Initialized conversation manager")
    
    def create_conversation(self, conversation_id: Optional[str] = None) -> Conversation:
        """Create a new conversation.
        
        Args:
            conversation_id: Optional conversation ID
            
        Returns:
            New conversation instance
        """
        system_message = self.azure_client.get_system_message()
        conversation = Conversation(
            conversation_id=conversation_id,
            system_prompt=system_message["content"]
        )
        self.conversations[conversation.conversation_id] = conversation
        logger.info(f"Created conversation {conversation.conversation_id}")
        return conversation
    
    def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """Get an existing conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Conversation instance or None if not found
        """
        return self.conversations.get(conversation_id)
    
    def chat(
        self,
        conversation_id: str,
        user_message: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        preferred_model: Optional[str] = None,
        fallback_model: Optional[str] = None,
        routing_mode: Optional[str] = None,
    ) -> Dict:
        """Send a message and get a response.
        
        Args:
            conversation_id: Conversation identifier
            user_message: User's message
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            Response dictionary with assistant's reply
        """
        # Get or create conversation
        conversation = self.get_conversation(conversation_id)
        if conversation is None:
            conversation = self.create_conversation(conversation_id)

        routing = self.router.route(
            user_message,
            preferred_model=preferred_model or conversation.selected_model,
            fallback_model=fallback_model or conversation.fallback_model,
            routing_mode=routing_mode or conversation.routing_mode,
        )
        conversation.selected_model = routing.assigned_model
        conversation.fallback_model = routing.fallback_model
        conversation.routing_mode = routing.mode

        normalized_message = routing.classification.normalized_message

        # Add user message
        conversation.add_message("user", normalized_message)
        
        # Get messages with history limit
        messages = conversation.get_messages(max_history=self.settings.agent.max_history)
        
        # Generate response
        try:
            selected_model = routing.assigned_model

            try:
                response = self.azure_client.chat_completion(
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    model=selected_model,
                )
            except Exception as primary_error:
                if routing.fallback_model == selected_model:
                    raise

                logger.warning(
                    "Primary model '%s' failed for conversation %s, retrying with fallback '%s'",
                    selected_model,
                    conversation_id,
                    routing.fallback_model,
                    exc_info=primary_error,
                )

                selected_model = routing.fallback_model

                try:
                    response = self.azure_client.chat_completion(
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        model=selected_model,
                    )
                except Exception as fallback_error:
                    logger.error(
                        "Fallback model '%s' also failed for conversation %s",
                        selected_model,
                        conversation_id,
                        exc_info=fallback_error,
                    )
                    raise fallback_error from primary_error
            
            # Add assistant response to conversation
            conversation.add_message("assistant", response["content"])
            usage = response.get("usage", {})
            total_tokens = int(usage.get("total_tokens", 0) or 0)
            estimated_cost = self.router.estimate_cost(selected_model, total_tokens)
             
            return {
                "conversation_id": conversation_id,
                "user_message": normalized_message,
                "assistant_message": response["content"],
                "usage": usage,
                "timestamp": conversation.updated_at.isoformat(),
                "classification": routing.classification.to_dict(),
                "routing": {
                    **routing.to_dict(),
                    "assigned_model": selected_model,
                    "requested_model": response.get("requested_model"),
                    "deployment_name": response.get("deployment_name"),
                },
                "estimated_cost_usd": estimated_cost,
            }
            
        except Exception as e:
            logger.error(f"Error in chat for conversation {conversation_id}: {str(e)}")
            raise
    
    def clear_conversation(self, conversation_id: str) -> bool:
        """Clear a conversation's history.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            True if conversation was cleared, False if not found
        """
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.clear()
            return True
        return False
    
    def delete_conversation(self, conversation_id: str) -> bool:
        """Delete a conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            True if conversation was deleted, False if not found
        """
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            logger.info(f"Deleted conversation {conversation_id}")
            return True
        return False
