"""Flask application for the conversational agent API.

SECURITY NOTICE: This implementation includes demo authentication and storage
features for development and testing purposes only. DO NOT use in production
without implementing proper security measures:

1. Replace plain-text password storage with bcrypt hashing
2. Replace UUID tokens with JWT tokens with expiration
3. Replace in-memory storage with a proper database
4. Add rate limiting for API endpoints
5. Implement HTTPS/TLS in production
6. Add CSRF protection
7. Implement proper session management
8. Add input validation and sanitization
9. Use environment-specific configuration
10. Add security headers (HSTS, CSP, etc.)

See requirements.txt for security-related packages to add for production.
"""

import logging
import os
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from werkzeug.utils import secure_filename

from src.config import get_settings
from src.agent import ConversationManager
from src.cms_module import UserService, UserCreate, UserLogin
from src.cms_module.services import OnboardingService
from src.cms_module.models.onboarding import OnboardingStepData

logger = logging.getLogger(__name__)

# SECURITY WARNING: In-memory storage for DEMO ONLY
# TODO: Replace with proper database (PostgreSQL, MongoDB, etc.) for production
# TODO: Implement thread-safety for concurrent access
# TODO: Add data persistence across server restarts
users_db = {}
documents_db = {}
training_data_db = {}
seats_db = {}


def create_app(config_path: Optional[str] = None) -> Flask:
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
    
    # Initialize user service for authentication
    user_service = UserService()
    
    # Initialize onboarding service
    onboarding_service = OnboardingService()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, settings.logging.level),
        format=settings.logging.format
    )
    
    # Ensure upload directory exists
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)

    def _normalize_site_domain(value: str) -> str:
        """Normalize user-provided site/domain value."""
        parsed = urlparse(value if "://" in value else f"https://{value}")
        return (parsed.netloc or parsed.path).lower().strip("/")

    def _build_seat(seat_id: str, site_domain: str, bot_name: str, greeting: str) -> Dict[str, Any]:
        """Build a standard seat response payload."""
        return {
            "id": seat_id,
            "site_domain": site_domain,
            "bot_name": bot_name,
            "greeting": greeting,
            "trained_sources": {
                "urls": [],
                "documents": []
            },
            "created_at": datetime.utcnow().isoformat()
        }
    
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

    @app.route("/seats", methods=["POST"])
    def create_seat():
        """Create a chatbot seat for a specific website."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Request body is required"}), 400

            site_value = data.get("site_domain") or data.get("site_url")
            if not site_value or not str(site_value).strip():
                return jsonify({"error": "site_domain (or site_url) is required"}), 400

            site_domain = _normalize_site_domain(str(site_value))
            if not site_domain:
                return jsonify({"error": "Invalid site_domain"}), 400

            seat_id = str(uuid.uuid4())
            seat = _build_seat(
                seat_id=seat_id,
                site_domain=site_domain,
                bot_name=data.get("bot_name", "Website Assistant"),
                greeting=data.get("greeting", "Hi! How can I help you today?")
            )
            seats_db[seat_id] = seat

            return jsonify({
                "message": "Chatbot Seat created successfully",
                "seat": seat
            }), 201
        except Exception as e:
            logger.error(f"Error creating seat: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500

    @app.route("/seats", methods=["GET"])
    def list_seats():
        """List chatbot seats."""
        return jsonify({"seats": list(seats_db.values())})

    @app.route("/seats/<seat_id>", methods=["GET"])
    def get_seat(seat_id: str):
        """Get a chatbot seat."""
        seat = seats_db.get(seat_id)
        if not seat:
            return jsonify({"error": "Seat not found"}), 404
        return jsonify({"seat": seat})
    
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
        """Register a new user with proper password hashing and JWT tokens."""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "Request body is required"}), 400
            
            # Validate required fields
            required_fields = ["email", "password", "name"]
            missing_fields = [f for f in required_fields if f not in data]
            if missing_fields:
                return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
            
            # Create UserCreate model (this will validate the data)
            try:
                user_create = UserCreate(
                    email=data["email"],
                    password=data["password"],
                    name=data["name"],
                    phone=data.get("phone"),
                    organization_name=data.get("organization_name")
                )
            except Exception as validation_error:
                return jsonify({"error": str(validation_error)}), 400
            
            # Register user using the CMS user service
            response = user_service.register_user(user_create)
            
            if not response.success:
                return jsonify({"error": response.message}), 400
            
            return jsonify({
                "message": response.message,
                "token": response.token,
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "name": response.user.name,
                    "phone": response.user.phone,
                    "organization_id": response.user.organization_id,
                    "organization_name": response.user.organization_name,
                    "is_verified": response.user.is_verified,
                    "onboarding_completed": response.user.onboarding_completed
                }
            }), 201
            
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.route("/auth/login", methods=["POST"])
    def login():
        """Login a user with proper password verification and JWT tokens."""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "Request body is required"}), 400
            
            # Validate required fields
            if "email" not in data or "password" not in data:
                return jsonify({"error": "Email and password required"}), 400
            
            # Create UserLogin model
            try:
                user_login = UserLogin(
                    email=data["email"],
                    password=data["password"]
                )
            except Exception as validation_error:
                return jsonify({"error": str(validation_error)}), 400
            
            # Login user using the CMS user service
            response = user_service.login_user(user_login)
            
            if not response.success:
                return jsonify({"error": response.message}), 401
            
            return jsonify({
                "message": response.message,
                "token": response.token,
                "user": {
                    "id": response.user.id,
                    "email": response.user.email,
                    "name": response.user.name,
                    "phone": response.user.phone,
                    "organization_id": response.user.organization_id,
                    "organization_name": response.user.organization_name,
                    "is_verified": response.user.is_verified,
                    "onboarding_completed": response.user.onboarding_completed,
                    "last_login": response.user.last_login.isoformat() if response.user.last_login else None
                }
            })
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    # Onboarding Endpoints
    @app.route("/onboarding/start", methods=["POST"])
    def start_onboarding():
        """Start onboarding for a user"""
        try:
            data = request.get_json()
            
            if not data or "user_id" not in data:
                return jsonify({"error": "user_id required"}), 400
            
            user_id = data["user_id"]
            response = onboarding_service.start_onboarding(user_id)
            
            if not response.success:
                return jsonify({"error": response.message}), 400
            
            return jsonify({
                "message": response.message,
                "progress": {
                    "user_id": response.progress.user_id,
                    "current_step": response.progress.current_step.value,
                    "completed_steps": [s.value for s in response.progress.completed_steps],
                    "status": response.progress.status.value,
                    "started_at": response.progress.started_at.isoformat() if response.progress.started_at else None
                }
            })
            
        except Exception as e:
            logger.error(f"Error starting onboarding: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.route("/onboarding/progress/<user_id>", methods=["GET"])
    def get_onboarding_progress(user_id: str):
        """Get onboarding progress for a user"""
        try:
            progress = onboarding_service.get_onboarding_progress(user_id)
            
            if not progress:
                return jsonify({"error": "Onboarding not started"}), 404
            
            return jsonify({
                "user_id": progress.user_id,
                "current_step": progress.current_step.value,
                "completed_steps": [s.value for s in progress.completed_steps],
                "status": progress.status.value,
                "started_at": progress.started_at.isoformat() if progress.started_at else None,
                "completed_at": progress.completed_at.isoformat() if progress.completed_at else None,
                "data": progress.data
            })
            
        except Exception as e:
            logger.error(f"Error getting onboarding progress: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.route("/onboarding/step/complete", methods=["POST"])
    def complete_onboarding_step():
        """Complete an onboarding step"""
        try:
            data = request.get_json()
            
            if not data or "user_id" not in data or "step" not in data:
                return jsonify({"error": "user_id and step required"}), 400
            
            user_id = data["user_id"]
            step_data = OnboardingStepData(
                step=data["step"],
                data=data.get("data", {})
            )
            
            response = onboarding_service.complete_step(user_id, step_data)
            
            if not response.success:
                return jsonify({"error": response.message}), 400
            
            return jsonify({
                "message": response.message,
                "progress": {
                    "user_id": response.progress.user_id,
                    "current_step": response.progress.current_step.value,
                    "completed_steps": [s.value for s in response.progress.completed_steps],
                    "status": response.progress.status.value
                }
            })
            
        except Exception as e:
            logger.error(f"Error completing step: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.route("/onboarding/skip", methods=["POST"])
    def skip_onboarding():
        """Skip onboarding for a user"""
        try:
            data = request.get_json()
            
            if not data or "user_id" not in data:
                return jsonify({"error": "user_id required"}), 400
            
            user_id = data["user_id"]
            response = onboarding_service.skip_onboarding(user_id)
            
            if not response.success:
                return jsonify({"error": response.message}), 400
            
            return jsonify({
                "message": response.message,
                "progress": {
                    "user_id": response.progress.user_id,
                    "status": response.progress.status.value
                }
            })
            
        except Exception as e:
            logger.error(f"Error skipping onboarding: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.route("/profile/<user_id>", methods=["GET"])
    def get_user_profile(user_id: str):
        """Get user profile"""
        try:
            profile = onboarding_service.get_profile(user_id)
            
            if not profile:
                return jsonify({"error": "Profile not found"}), 404
            
            return jsonify({
                "user_id": profile.user_id,
                "job_title": profile.job_title,
                "department": profile.department,
                "bio": profile.bio,
                "avatar_url": profile.avatar_url,
                "preferences": {
                    "theme": profile.preferences.theme,
                    "language": profile.preferences.language,
                    "notifications_enabled": profile.preferences.notifications_enabled,
                    "email_notifications": profile.preferences.email_notifications,
                    "chat_history_enabled": profile.preferences.chat_history_enabled,
                    "timezone": profile.preferences.timezone
                },
                "updated_at": profile.updated_at.isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error getting profile: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    @app.route("/profile/<user_id>", methods=["PUT"])
    def update_user_profile(user_id: str):
        """Update user profile"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({"error": "Request body required"}), 400
            
            response = onboarding_service.update_profile(user_id, data)
            
            if not response.success:
                return jsonify({"error": response.message}), 400
            
            return jsonify({
                "message": response.message,
                "profile": {
                    "user_id": response.profile.user_id,
                    "job_title": response.profile.job_title,
                    "department": response.profile.department,
                    "bio": response.profile.bio,
                    "preferences": {
                        "theme": response.profile.preferences.theme,
                        "language": response.profile.preferences.language
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    
    # Training Endpoints
    @app.route("/training/url", methods=["POST"])
    def train_from_url():
        """Learn from a URL."""
        try:
            data = request.get_json()
            
            if not data or "url" not in data:
                return jsonify({"error": "URL required"}), 400
            
            url = data["url"]
            seat_id = data.get("seat_id")

            if seat_id and seat_id not in seats_db:
                return jsonify({"error": "Seat not found"}), 404
            
            # Store URL for training (in production, fetch and process content)
            training_id = str(uuid.uuid4())
            training_data_db[training_id] = {
                "id": training_id,
                "type": "url",
                "source": url,
                "seat_id": seat_id,
                "status": "processed"
            }

            if seat_id:
                seats_db[seat_id]["trained_sources"]["urls"].append({
                    "training_id": training_id,
                    "source": url
                })
            
            logger.info(f"Added URL for training: {url}")
            
            return jsonify({
                "message": f"Successfully learned from URL: {url}",
                "training_id": training_id,
                "seat_id": seat_id
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
            seat_id = request.form.get('seat_id')
            if seat_id and seat_id not in seats_db:
                return jsonify({"error": "Seat not found"}), 404
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
                    "size": os.path.getsize(filepath),
                    "seat_id": seat_id
                }
                
                uploaded.append({
                    "id": file_id,
                    "name": filename
                })

                if seat_id:
                    seats_db[seat_id]["trained_sources"]["documents"].append({
                        "document_id": file_id,
                        "name": filename
                    })
                
                logger.info(f"Document uploaded: {filename}")
            
            return jsonify({
                "message": f"Successfully uploaded {len(uploaded)} document(s)",
                "documents": uploaded,
                "seat_id": seat_id
            })
            
        except Exception as e:
            logger.error(f"Document upload error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @app.route("/training/documents", methods=["GET"])
    def get_documents():
        """Get list of uploaded documents."""
        try:
            seat_id = request.args.get("seat_id")
            if seat_id and seat_id not in seats_db:
                return jsonify({"error": "Seat not found"}), 404

            docs = [
                {"id": doc_id, "name": doc["name"], "size": doc["size"]}
                for doc_id, doc in documents_db.items()
                if not seat_id or doc.get("seat_id") == seat_id
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
            seat_id = doc.get("seat_id")
            if seat_id and seat_id in seats_db:
                seats_db[seat_id]["trained_sources"]["documents"] = [
                    seat_doc
                    for seat_doc in seats_db[seat_id]["trained_sources"]["documents"]
                    if seat_doc["document_id"] != document_id
                ]
            del documents_db[document_id]
            
            logger.info(f"Document deleted: {doc['name']}")
            
            return jsonify({"message": "Document deleted successfully"})
            
        except Exception as e:
            logger.error(f"Delete document error: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    # Register CMS Blueprint
    # NOTE: CMS routes disabled - CMS is now implemented as a Blazor application in src/cms/
    # from src.api.cms_routes import cms_bp
    # app.register_blueprint(cms_bp)
    
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
