"""Application configuration"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Orkinosai CMS"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    # Default to SQLite for development. Override with PostgreSQL for production.
    DATABASE_URL: str = "sqlite:///./orkinosai.db"
    
    # Security
    # WARNING: Change SECRET_KEY in production! Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Azure Configuration (Placeholder)
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    AZURE_STORAGE_CONTAINER_NAME: str = "orkinosai-documents"
    AZURE_AI_ENDPOINT: Optional[str] = None
    AZURE_AI_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
