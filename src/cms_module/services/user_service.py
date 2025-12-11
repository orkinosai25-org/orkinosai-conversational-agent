"""User service for user management operations"""

import logging
import uuid
from datetime import datetime
from typing import Optional
from ..models.user import UserCreate, UserLogin, User, UserResponse, UserInDB
from ..db.user_db import get_user_database
from .auth_service import AuthService

logger = logging.getLogger(__name__)


class UserService:
    """Service for user management operations"""
    
    def __init__(self, auth_service: Optional[AuthService] = None):
        """
        Initialize user service
        
        Args:
            auth_service: AuthService instance (creates new one if not provided)
        """
        self.auth_service = auth_service or AuthService()
        self.user_db = get_user_database()
    
    def register_user(self, user_data: UserCreate) -> UserResponse:
        """
        Register a new user
        
        Args:
            user_data: UserCreate model with registration data
            
        Returns:
            UserResponse with success status, message, user data, and token
        """
        try:
            # Check if user already exists
            if self.user_db.user_exists(user_data.email):
                return UserResponse(
                    success=False,
                    message="User with this email already exists",
                    user=None,
                    token=None
                )
            
            # Hash password
            password_hash = self.auth_service.hash_password(user_data.password)
            
            # Create user ID
            user_id = f"user_{uuid.uuid4().hex[:12]}"
            
            # Create organization if provided
            organization_id = None
            if user_data.organization_name:
                organization_id = f"org_{uuid.uuid4().hex[:12]}"
            
            # Create user in database
            now = datetime.utcnow()
            user_in_db = UserInDB(
                id=user_id,
                email=user_data.email,
                name=user_data.name,
                phone=user_data.phone,
                organization_id=organization_id,
                organization_name=user_data.organization_name,
                password_hash=password_hash,
                is_active=True,
                is_verified=False,
                created_at=now,
                updated_at=now,
                onboarding_completed=False
            )
            
            success = self.user_db.create_user(user_in_db)
            if not success:
                return UserResponse(
                    success=False,
                    message="Failed to create user",
                    user=None,
                    token=None
                )
            
            # Create user response (without password hash)
            user = User(
                id=user_in_db.id,
                email=user_in_db.email,
                name=user_in_db.name,
                phone=user_in_db.phone,
                organization_id=user_in_db.organization_id,
                organization_name=user_in_db.organization_name,
                is_active=user_in_db.is_active,
                is_verified=user_in_db.is_verified,
                created_at=user_in_db.created_at,
                updated_at=user_in_db.updated_at,
                onboarding_completed=user_in_db.onboarding_completed
            )
            
            # Generate token
            token = self.auth_service.create_token(user)
            
            logger.info(f"User {user.email} registered successfully")
            
            return UserResponse(
                success=True,
                message="User registered successfully",
                user=user,
                token=token
            )
            
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return UserResponse(
                success=False,
                message=f"Error registering user: {str(e)}",
                user=None,
                token=None
            )
    
    def login_user(self, login_data: UserLogin) -> UserResponse:
        """
        Login user
        
        Args:
            login_data: UserLogin model with email and password
            
        Returns:
            UserResponse with success status, message, user data, and token
        """
        try:
            # Get user from database
            user_in_db = self.user_db.get_user_by_email(login_data.email)
            if not user_in_db:
                return UserResponse(
                    success=False,
                    message="Invalid email or password",
                    user=None,
                    token=None
                )
            
            # Verify password
            if not self.auth_service.verify_password(login_data.password, user_in_db.password_hash):
                return UserResponse(
                    success=False,
                    message="Invalid email or password",
                    user=None,
                    token=None
                )
            
            # Check if user is active
            if not user_in_db.is_active:
                return UserResponse(
                    success=False,
                    message="User account is inactive",
                    user=None,
                    token=None
                )
            
            # Update last login
            self.user_db.update_user(user_in_db.id, {"last_login": datetime.utcnow()})
            
            # Create user response (without password hash)
            user = User(
                id=user_in_db.id,
                email=user_in_db.email,
                name=user_in_db.name,
                phone=user_in_db.phone,
                organization_id=user_in_db.organization_id,
                organization_name=user_in_db.organization_name,
                is_active=user_in_db.is_active,
                is_verified=user_in_db.is_verified,
                created_at=user_in_db.created_at,
                updated_at=user_in_db.updated_at,
                last_login=datetime.utcnow(),
                onboarding_completed=user_in_db.onboarding_completed
            )
            
            # Generate token
            token = self.auth_service.create_token(user)
            
            logger.info(f"User {user.email} logged in successfully")
            
            return UserResponse(
                success=True,
                message="Login successful",
                user=user,
                token=token
            )
            
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            return UserResponse(
                success=False,
                message=f"Error logging in: {str(e)}",
                user=None,
                token=None
            )
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User unique identifier
            
        Returns:
            User object if found, None otherwise
        """
        user_in_db = self.user_db.get_user_by_id(user_id)
        if not user_in_db:
            return None
        
        return User(
            id=user_in_db.id,
            email=user_in_db.email,
            name=user_in_db.name,
            phone=user_in_db.phone,
            organization_id=user_in_db.organization_id,
            organization_name=user_in_db.organization_name,
            is_active=user_in_db.is_active,
            is_verified=user_in_db.is_verified,
            created_at=user_in_db.created_at,
            updated_at=user_in_db.updated_at,
            last_login=user_in_db.last_login,
            onboarding_completed=user_in_db.onboarding_completed
        )
    
    def verify_token(self, token: str) -> Optional[User]:
        """
        Verify JWT token and return user
        
        Args:
            token: JWT token string
            
        Returns:
            User object if token is valid, None otherwise
        """
        return self.auth_service.extract_user_from_token(token)
