"""In-memory database for user storage (for development/testing)

WARNING: This is a simple in-memory database for development and testing only.
For production, replace with a proper database (PostgreSQL, MongoDB, etc.)
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime
from ..models.user import UserInDB

logger = logging.getLogger(__name__)


class UserDatabase:
    """In-memory user database"""
    
    def __init__(self):
        """Initialize empty user database"""
        self._users: Dict[str, UserInDB] = {}  # user_id -> UserInDB
        self._users_by_email: Dict[str, str] = {}  # email -> user_id
    
    def create_user(self, user: UserInDB) -> bool:
        """
        Create a new user in database
        
        Args:
            user: UserInDB object with all fields including password_hash
            
        Returns:
            True if user was created, False if user already exists
        """
        if user.email in self._users_by_email:
            logger.warning(f"User with email {user.email} already exists")
            return False
        
        self._users[user.id] = user
        self._users_by_email[user.email] = user.id
        logger.info(f"User {user.email} created successfully with ID {user.id}")
        return True
    
    def get_user_by_id(self, user_id: str) -> Optional[UserInDB]:
        """
        Get user by ID
        
        Args:
            user_id: User unique identifier
            
        Returns:
            UserInDB object if found, None otherwise
        """
        return self._users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """
        Get user by email
        
        Args:
            email: User email address
            
        Returns:
            UserInDB object if found, None otherwise
        """
        user_id = self._users_by_email.get(email)
        if user_id:
            return self._users.get(user_id)
        return None
    
    def update_user(self, user_id: str, updates: Dict) -> bool:
        """
        Update user information
        
        Args:
            user_id: User unique identifier
            updates: Dictionary of fields to update
            
        Returns:
            True if user was updated, False if user not found
        """
        user = self._users.get(user_id)
        if not user:
            logger.warning(f"User {user_id} not found for update")
            return False
        
        # Update fields
        for key, value in updates.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        logger.info(f"User {user_id} updated successfully")
        return True
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete user from database
        
        Args:
            user_id: User unique identifier
            
        Returns:
            True if user was deleted, False if user not found
        """
        user = self._users.get(user_id)
        if not user:
            logger.warning(f"User {user_id} not found for deletion")
            return False
        
        del self._users_by_email[user.email]
        del self._users[user_id]
        logger.info(f"User {user_id} deleted successfully")
        return True
    
    def list_users(self) -> List[UserInDB]:
        """
        List all users
        
        Returns:
            List of all UserInDB objects
        """
        return list(self._users.values())
    
    def user_exists(self, email: str) -> bool:
        """
        Check if user exists by email
        
        Args:
            email: User email address
            
        Returns:
            True if user exists, False otherwise
        """
        return email in self._users_by_email
    
    def clear(self):
        """Clear all users from database (for testing)"""
        self._users.clear()
        self._users_by_email.clear()
        logger.info("User database cleared")


# Singleton instance
_user_db_instance: Optional[UserDatabase] = None


def get_user_database() -> UserDatabase:
    """
    Get singleton user database instance
    
    Returns:
        UserDatabase instance
    """
    global _user_db_instance
    if _user_db_instance is None:
        _user_db_instance = UserDatabase()
    return _user_db_instance
