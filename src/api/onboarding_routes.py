"""
Onboarding API Routes

RESTful API endpoints for managing user onboarding flows.
These endpoints integrate with the CMS onboarding service to provide:
- Flow initialization
- Step progression
- Progress tracking
- Content delivery

Usage in Flask app:
    from src.api.onboarding_routes import onboarding_bp
    app.register_blueprint(onboarding_bp)
"""

from flask import Blueprint, request, jsonify
from typing import Optional, Dict, Any
import logging

from src.cms.onboarding import (
    OnboardingService,
    OnboardingState
)

logger = logging.getLogger(__name__)

# Create blueprint for onboarding routes
onboarding_bp = Blueprint('onboarding', __name__, url_prefix='/api/onboarding')

# Initialize onboarding service (singleton pattern)
_onboarding_service: Optional[OnboardingService] = None


def get_onboarding_service() -> OnboardingService:
    """
    Get the onboarding service instance (lazy initialization).
    
    Returns:
        OnboardingService singleton instance
    """
    global _onboarding_service
    if _onboarding_service is None:
        _onboarding_service = OnboardingService()
    return _onboarding_service


# Flow Management Endpoints

@onboarding_bp.route('/flows', methods=['GET'])
def list_flows():
    """
    List all available onboarding flows.
    
    Returns:
        JSON array of onboarding flows
        
    Example response:
        {
            "success": true,
            "flows": [
                {
                    "id": "user_onboarding",
                    "name": "user_onboarding",
                    "title": "User Onboarding",
                    "description": "Standard onboarding flow for new users",
                    "steps": [...],
                    "is_active": true
                }
            ]
        }
    """
    try:
        service = get_onboarding_service()
        flows = service.list_flows()
        
        return jsonify({
            'success': True,
            'flows': [flow.model_dump() for flow in flows]
        }), 200
    except Exception as e:
        logger.error(f"Error listing flows: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@onboarding_bp.route('/flows/<flow_id>', methods=['GET'])
def get_flow(flow_id: str):
    """
    Get details of a specific onboarding flow.
    
    Args:
        flow_id: Flow identifier
        
    Returns:
        JSON object with flow details
        
    Example response:
        {
            "success": true,
            "flow": {
                "id": "user_onboarding",
                "name": "user_onboarding",
                "title": "User Onboarding",
                "steps": [...]
            }
        }
    """
    try:
        service = get_onboarding_service()
        flow = service.get_flow(flow_id)
        
        if not flow:
            return jsonify({
                'success': False,
                'error': f'Flow not found: {flow_id}'
            }), 404
        
        return jsonify({
            'success': True,
            'flow': flow.model_dump()
        }), 200
    except Exception as e:
        logger.error(f"Error getting flow {flow_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# User Progress Endpoints

@onboarding_bp.route('/start', methods=['POST'])
def start_onboarding():
    """
    Start onboarding for a user.
    
    Request body:
        {
            "user_id": "user-123",
            "flow_type": "user_onboarding",  // optional, defaults to "user_onboarding"
            "metadata": {                     // optional
                "source": "website",
                "referrer": "google"
            }
        }
        
    Returns:
        JSON object with progress details
        
    Example response:
        {
            "success": true,
            "progress": {
                "id": "progress-123",
                "user_id": "user-123",
                "flow_id": "user_onboarding",
                "state": "in_progress",
                "current_step_index": 0,
                "started_at": "2025-12-11T18:30:00Z"
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: user_id'
            }), 400
        
        service = get_onboarding_service()
        progress = service.start_onboarding(
            user_id=data['user_id'],
            flow_type=data.get('flow_type', 'user_onboarding'),
            metadata=data.get('metadata')
        )
        
        return jsonify({
            'success': True,
            'progress': progress.model_dump()
        }), 201
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Error starting onboarding: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@onboarding_bp.route('/progress/<progress_id>', methods=['GET'])
def get_progress(progress_id: str):
    """
    Get onboarding progress by ID.
    
    Args:
        progress_id: Progress record identifier
        
    Returns:
        JSON object with progress details
        
    Example response:
        {
            "success": true,
            "progress": {
                "id": "progress-123",
                "user_id": "user-123",
                "flow_id": "user_onboarding",
                "state": "in_progress",
                "current_step_index": 2,
                "completed_steps": ["step1", "step2"],
                "completion_percentage": 33.3
            }
        }
    """
    try:
        service = get_onboarding_service()
        progress = service.get_progress(progress_id)
        
        if not progress:
            return jsonify({
                'success': False,
                'error': f'Progress not found: {progress_id}'
            }), 404
        
        # Get flow to calculate completion percentage
        flow = service.get_flow(progress.flow_id)
        total_steps = len(flow.steps) if flow else 0
        
        progress_data = progress.model_dump()
        progress_data['completion_percentage'] = progress.get_progress_percentage(total_steps)
        
        return jsonify({
            'success': True,
            'progress': progress_data
        }), 200
    except Exception as e:
        logger.error(f"Error getting progress {progress_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@onboarding_bp.route('/progress/user/<user_id>', methods=['GET'])
def get_user_progress(user_id: str):
    """
    Get all onboarding progress records for a user.
    
    Args:
        user_id: User identifier
        
    Query parameters:
        flow_type: Optional flow type filter
        
    Returns:
        JSON array of progress records
        
    Example response:
        {
            "success": true,
            "progress_records": [
                {
                    "id": "progress-123",
                    "user_id": "user-123",
                    "flow_id": "user_onboarding",
                    "state": "completed"
                }
            ]
        }
    """
    try:
        flow_type = request.args.get('flow_type')
        
        service = get_onboarding_service()
        progress_records = service.get_user_progress(user_id, flow_type)
        
        return jsonify({
            'success': True,
            'progress_records': [p.model_dump() for p in progress_records]
        }), 200
    except Exception as e:
        logger.error(f"Error getting user progress for {user_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Step Navigation Endpoints

@onboarding_bp.route('/progress/<progress_id>/current-step', methods=['GET'])
def get_current_step(progress_id: str):
    """
    Get the current step for a user's onboarding progress.
    
    Args:
        progress_id: Progress record identifier
        
    Query parameters:
        user_name: Optional user name for content personalization
        user_role: Optional user role for content personalization
        
    Returns:
        JSON object with current step details and CMS content
        
    Example response:
        {
            "success": true,
            "step": {
                "id": "user_onboarding_welcome",
                "step_type": "welcome",
                "order": 0,
                "title": "Welcome to Orkinosai, John! 🚀",
                "description": "Let's get you set up in just a few minutes.",
                "content": {
                    "hero_text": "Welcome to the future of conversational AI",
                    "features": [...]
                },
                "is_required": true,
                "cta_text": "Get Started"
            }
        }
    """
    try:
        # Build user context from query parameters
        user_context = {}
        if request.args.get('user_name'):
            user_context['name'] = request.args.get('user_name')
        if request.args.get('user_role'):
            user_context['role'] = request.args.get('user_role')
        
        service = get_onboarding_service()
        step = service.get_current_step(progress_id, user_context)
        
        if not step:
            return jsonify({
                'success': False,
                'error': 'Current step not found or progress completed'
            }), 404
        
        return jsonify({
            'success': True,
            'step': step.model_dump()
        }), 200
    except Exception as e:
        logger.error(f"Error getting current step for {progress_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@onboarding_bp.route('/progress/<progress_id>/complete-step', methods=['POST'])
def complete_step(progress_id: str):
    """
    Mark a step as completed and advance to the next step.
    
    Args:
        progress_id: Progress record identifier
        
    Request body:
        {
            "step_id": "user_onboarding_profile",
            "step_data": {                        // optional
                "name": "John Doe",
                "role": "Developer",
                "company": "Acme Inc."
            }
        }
        
    Returns:
        JSON object indicating success
        
    Example response:
        {
            "success": true,
            "message": "Step completed successfully",
            "next_step": {
                "id": "user_onboarding_organization",
                "title": "Create Workspace",
                ...
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'step_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: step_id'
            }), 400
        
        service = get_onboarding_service()
        success = service.complete_step(
            progress_id=progress_id,
            step_id=data['step_id'],
            step_data=data.get('step_data')
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to complete step'
            }), 400
        
        # Get the next step (if any)
        next_step = service.get_current_step(progress_id)
        
        response_data = {
            'success': True,
            'message': 'Step completed successfully'
        }
        
        if next_step:
            response_data['next_step'] = next_step.model_dump()
        else:
            response_data['message'] = 'Onboarding completed!'
        
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f"Error completing step for {progress_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@onboarding_bp.route('/progress/<progress_id>/skip-step', methods=['POST'])
def skip_step(progress_id: str):
    """
    Skip an optional step and move to the next step.
    
    Args:
        progress_id: Progress record identifier
        
    Request body:
        {
            "step_id": "user_onboarding_theme"
        }
        
    Returns:
        JSON object indicating success
        
    Example response:
        {
            "success": true,
            "message": "Step skipped successfully",
            "next_step": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'step_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: step_id'
            }), 400
        
        service = get_onboarding_service()
        success = service.skip_step(
            progress_id=progress_id,
            step_id=data['step_id']
        )
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'Failed to skip step (may be required)'
            }), 400
        
        # Get the next step (if any)
        next_step = service.get_current_step(progress_id)
        
        response_data = {
            'success': True,
            'message': 'Step skipped successfully'
        }
        
        if next_step:
            response_data['next_step'] = next_step.model_dump()
        else:
            response_data['message'] = 'Onboarding completed!'
        
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f"Error skipping step for {progress_id}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
