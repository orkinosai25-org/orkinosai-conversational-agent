"""Authentication service for user management"""

import bcrypt
import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict
from ..models.user import UserCreate, UserLogin, User, UserInDB

logger = logging.getLogger(__name__)


class AuthService:
    """Service for user authentication and token management"""
    
    def __init__(self, jwt_secret: str = "dev-secret-key-change-in-production", jwt_algorithm: str = "HS256"):
        """
        Initialize authentication service
        
        Args:
            jwt_secret: Secret key for JWT token signing (should be from environment in production)
            jwt_algorithm: JWT signing algorithm
        """
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self.token_expiry_hours = 24
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Plain text password
            password_hash: Bcrypt password hash
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    def create_token(self, user: User) -> str:
        """
        Create JWT token for user
        
        Args:
            user: User object
            
        Returns:
            JWT token string
        """
        payload = {
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "organization_id": user.organization_id,
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours),
            "iat": datetime.utcnow()
        }
        
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
    
    def extract_user_from_token(self, token: str) -> Optional[User]:
        """
        Extract user information from JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            User object if token is valid, None otherwise
        """
        payload = self.verify_token(token)
        if not payload:
            return None
        
        user = User(
            id=payload.get("user_id"),
            email=payload.get("email"),
            name=payload.get("name"),
            organization_id=payload.get("organization_id")
        )
        return user
