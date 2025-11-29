"""Settings and configuration management."""

import os
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AzureOpenAIConfig(BaseModel):
    """Azure OpenAI Service configuration."""
    endpoint: str = Field(..., description="Azure OpenAI endpoint URL")
    api_key: str = Field(..., description="Azure OpenAI API key")
    api_version: str = Field(default="2024-08-01-preview", description="API version")
    deployment_name: str = Field(..., description="Deployment name")
    model: str = Field(default="gpt-4", description="Model name")


class AzureSearchConfig(BaseModel):
    """Azure AI Search configuration."""
    endpoint: Optional[str] = None
    api_key: Optional[str] = None
    index_name: Optional[str] = None


class AzureCognitiveServicesConfig(BaseModel):
    """Azure Cognitive Services configuration."""
    endpoint: Optional[str] = None
    api_key: Optional[str] = None


class AzureConfig(BaseModel):
    """Azure services configuration."""
    openai: AzureOpenAIConfig
    search: Optional[AzureSearchConfig] = None
    cognitive_services: Optional[AzureCognitiveServicesConfig] = None


class AgentConfig(BaseModel):
    """Conversational agent configuration."""
    name: str = Field(default="Orkinosai Conversational Agent")
    version: str = Field(default="1.0.0")
    max_history: int = Field(default=10, description="Maximum conversation history")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, gt=0)
    system_prompt: str = Field(default="You are a helpful AI assistant.")


class ServerConfig(BaseModel):
    """API server configuration."""
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=5000, gt=0, lt=65536)
    debug: bool = Field(default=False)
    cors_origins: List[str] = Field(default=["*"])


class LoggingConfig(BaseModel):
    """Logging configuration."""
    level: str = Field(default="INFO")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file: str = Field(default="logs/agent.log")


class Settings(BaseModel):
    """Application settings."""
    azure: AzureConfig
    agent: AgentConfig = Field(default_factory=AgentConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    @classmethod
    def from_yaml(cls, config_path: str = "config.yaml") -> "Settings":
        """Load settings from YAML file with environment variable substitution."""
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, "r") as f:
            config_data = yaml.safe_load(f)
        
        # Substitute environment variables
        config_data = cls._substitute_env_vars(config_data)
        
        return cls(**config_data)
    
    @staticmethod
    def _substitute_env_vars(data: Any) -> Any:
        """Recursively substitute environment variables in configuration."""
        if isinstance(data, dict):
            return {key: Settings._substitute_env_vars(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [Settings._substitute_env_vars(item) for item in data]
        elif isinstance(data, str) and data.startswith("${") and data.endswith("}"):
            env_var = data[2:-1]
            return os.getenv(env_var, data)
        return data


# Global settings instance
_settings: Optional[Settings] = None


def get_settings(config_path: str = "config.yaml") -> Settings:
    """Get or create settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings.from_yaml(config_path)
    return _settings
