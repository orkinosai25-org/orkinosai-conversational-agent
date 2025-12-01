"""Flask application for the conversational agent API."""

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any

from src.config import get_settings
from src.agent import ConversationManager

logger = logging.getLogger(__name__)


def create_app(config_path: str = "config.yaml") -> Flask:
    """Create and configure Flask application.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load settings
    settings = get_settings(config_path)
    
    # Configure CORS
    CORS(app, origins=settings.server.cors_origins)
    
    # Initialize conversation manager
    conversation_manager = ConversationManager(settings)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.logging.level),
        format=settings.logging.format
    )
    
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "agent": settings.agent.name,
            "version": settings.agent.version
        })
    
    @app.route("/chat", methods=["POST"])
    def chat():
        """Chat endpoint for conversational interaction.
        
        Request body:
            {
                "conversation_id": "optional-conversation-id",
                "message": "user message",
                "temperature": 0.7,  // optional
                "max_tokens": 1000   // optional
            }
        
        Returns:
            Response with assistant's message
        """
        try:
            data = request.get_json()
            
            if not data or "message" not in data:
                return jsonify({"error": "Missing 'message' in request body"}), 400
            
            conversation_id = data.get("conversation_id")
            user_message = data["message"]
            temperature = data.get("temperature")
            max_tokens = data.get("max_tokens")
            
            # Generate response
            response = conversation_manager.chat(
                conversation_id=conversation_id or "default",
                user_message=user_message,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return jsonify(response)
            
        except Exception as e:
            logger.error(f"Error in chat endpoint: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/conversations/<conversation_id>", methods=["GET"])
    def get_conversation(conversation_id: str):
        """Get conversation details.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Conversation details
        """
        conversation = conversation_manager.get_conversation(conversation_id)
        
        if conversation is None:
            return jsonify({"error": "Conversation not found"}), 404
        
        return jsonify({
            "conversation_id": conversation.conversation_id,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "message_count": len(conversation.messages)
        })
    
    @app.route("/conversations/<conversation_id>", methods=["DELETE"])
    def delete_conversation(conversation_id: str):
        """Delete a conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Success message
        """
        success = conversation_manager.delete_conversation(conversation_id)
        
        if not success:
            return jsonify({"error": "Conversation not found"}), 404
        
        return jsonify({"message": f"Conversation {conversation_id} deleted"})
    
    @app.route("/conversations/<conversation_id>/clear", methods=["POST"])
    def clear_conversation(conversation_id: str):
        """Clear conversation history.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Success message
        """
        success = conversation_manager.clear_conversation(conversation_id)
        
        if not success:
            return jsonify({"error": "Conversation not found"}), 404
        
        return jsonify({"message": f"Conversation {conversation_id} cleared"})
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({"error": "Internal server error"}), 500
    
    return app
