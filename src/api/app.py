"""Flask application for the conversational agent API."""

import logging
import os
import uuid
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from typing import Dict, Any
from werkzeug.utils import secure_filename

from src.config import get_settings
from src.agent import ConversationManager

logger = logging.getLogger(__name__)

# In-memory storage for demo (replace with database in production)
users_db = {}
documents_db = {}
training_data_db = {}


def create_app(config_path: str = "config.yaml") -> Flask:
    """Create and configure Flask application.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__, 
                template_folder='../../templates',
                static_folder='../../static')
    
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
    
    # Ensure upload directory exists
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    # Serve UI
    @app.route("/")
    def index():
        """Serve the main UI."""
        return render_template("index.html")
    
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
    
    # Authentication Endpoints
    @app.route("/auth/register", methods=["POST"])
    def register():
        """Register a new user."""
        try:
            data = request.get_json()
            
            if not data or "email" not in data or "password" not in data:
                return jsonify({"error": "Email and password required"}), 400
            
            email = data["email"]
            
            # Check if user already exists
            if email in users_db:
                return jsonify({"error": "User already exists"}), 400
            
            # Create user (in production, hash the password!)
            user_id = str(uuid.uuid4())
            users_db[email] = {
                "id": user_id,
                "email": email,
                "name": data.get("name", email.split("@")[0]),
                "password": data["password"]  # In production, hash this!
            }
            
            # Generate token (in production, use JWT!)
            token = str(uuid.uuid4())
            
            return jsonify({
                "message": "User registered successfully",
                "token": token,
                "user": {
                    "id": user_id,
                    "email": email,
                    "name": users_db[email]["name"]
                }
            }), 201
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/auth/login", methods=["POST"])
    def login():
        """Login a user."""
        try:
            data = request.get_json()
            
            if not data or "email" not in data or "password" not in data:
                return jsonify({"error": "Email and password required"}), 400
            
            email = data["email"]
            password = data["password"]
            
            # Check credentials
            if email not in users_db or users_db[email]["password"] != password:
                return jsonify({"error": "Invalid credentials"}), 401
            
            # Generate token (in production, use JWT!)
            token = str(uuid.uuid4())
            
            user = users_db[email]
            return jsonify({
                "message": "Login successful",
                "token": token,
                "user": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"]
                }
            })
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    # Training Endpoints
    @app.route("/training/url", methods=["POST"])
    def train_from_url():
        """Learn from a URL."""
        try:
            data = request.get_json()
            
            if not data or "url" not in data:
                return jsonify({"error": "URL required"}), 400
            
            url = data["url"]
            
            # Store URL for training (in production, fetch and process content)
            training_id = str(uuid.uuid4())
            training_data_db[training_id] = {
                "id": training_id,
                "type": "url",
                "source": url,
                "status": "processed"
            }
            
            logger.info(f"Added URL for training: {url}")
            
            return jsonify({
                "message": f"Successfully learned from URL: {url}",
                "training_id": training_id
            })
            
        except Exception as e:
            logger.error(f"URL training error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/training/documents", methods=["POST"])
    def upload_documents():
        """Upload and process documents for training."""
        try:
            if 'documents' not in request.files:
                return jsonify({"error": "No documents provided"}), 400
            
            files = request.files.getlist('documents')
            uploaded = []
            
            for file in files:
                if file.filename == '':
                    continue
                
                # Save file
                filename = secure_filename(file.filename)
                file_id = str(uuid.uuid4())
                filepath = upload_dir / f"{file_id}_{filename}"
                file.save(filepath)
                
                # Store document info
                documents_db[file_id] = {
                    "id": file_id,
                    "name": filename,
                    "path": str(filepath),
                    "size": os.path.getsize(filepath)
                }
                
                uploaded.append({
                    "id": file_id,
                    "name": filename
                })
                
                logger.info(f"Document uploaded: {filename}")
            
            return jsonify({
                "message": f"Successfully uploaded {len(uploaded)} document(s)",
                "documents": uploaded
            })
            
        except Exception as e:
            logger.error(f"Document upload error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/training/documents", methods=["GET"])
    def get_documents():
        """Get list of uploaded documents."""
        try:
            docs = [
                {"id": doc_id, "name": doc["name"], "size": doc["size"]}
                for doc_id, doc in documents_db.items()
            ]
            return jsonify({"documents": docs})
        except Exception as e:
            logger.error(f"Get documents error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/training/documents/<document_id>", methods=["DELETE"])
    def delete_document(document_id: str):
        """Delete a document."""
        try:
            if document_id not in documents_db:
                return jsonify({"error": "Document not found"}), 404
            
            # Delete file
            doc = documents_db[document_id]
            if os.path.exists(doc["path"]):
                os.remove(doc["path"])
            
            # Remove from database
            del documents_db[document_id]
            
            logger.info(f"Document deleted: {doc['name']}")
            
            return jsonify({"message": "Document deleted successfully"})
            
        except Exception as e:
            logger.error(f"Delete document error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
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
