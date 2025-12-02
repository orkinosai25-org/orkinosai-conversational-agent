"""Settings and configuration management."""

import os
import json
import yaml
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


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
    def _create_default_appsettings(cls, config_path: str = "appsettings.json") -> None:
        """Create default appsettings.json if it doesn't exist."""
        config_file = Path(config_path)
        
        if not config_file.exists():
            default_settings = {
                "azure": {
                    "openai": {
                        "endpoint": "https://your-resource-name.openai.azure.com/",
                        "api_key": "your-api-key-here",
                        "api_version": "2024-08-01-preview",
                        "deployment_name": "your-deployment-name",
                        "model": "gpt-4"
                    },
                    "search": {
                        "endpoint": "https://your-search-service.search.windows.net",
                        "api_key": "your-search-api-key",
                        "index_name": "your-index-name"
                    },
                    "cognitive_services": {
                        "endpoint": "https://your-cognitive-service.cognitiveservices.azure.com/",
                        "api_key": "your-cognitive-services-key"
                    }
                },
                "agent": {
                    "name": "Orkinosai Conversational Agent",
                    "version": "1.0.0",
                    "max_history": 10,
                    "temperature": 0.7,
                    "max_tokens": 1000,
                    "system_prompt": "You are a helpful AI assistant."
                },
                "server": {
                    "host": "0.0.0.0",
                    "port": 5000,
                    "debug": False,
                    "cors_origins": ["*"]
                },
                "logging": {
                    "level": "INFO",
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    "file": "logs/agent.log"
                }
            }
            
            with open(config_file, "w") as f:
                json.dump(default_settings, f, indent=2)
            
            logger.info(f"Created default configuration file: {config_path}")

    @classmethod
    def from_json(cls, config_path: str = "appsettings.json") -> "Settings":
        """Load settings from JSON file with environment variable override."""
        config_file = Path(config_path)
        
        # Create default appsettings.json if it doesn't exist
        if not config_file.exists():
            cls._create_default_appsettings(config_path)
        
        with open(config_file, "r") as f:
            config_data = json.load(f)
        
        # Override with environment variables if present
        config_data = cls._apply_env_overrides(config_data)
        
        return cls(**config_data)

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
    def _apply_env_overrides(config_data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply environment variable overrides to configuration."""
        # Azure OpenAI overrides
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if endpoint:
            config_data.setdefault("azure", {}).setdefault("openai", {})["endpoint"] = endpoint
        
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        if api_key:
            config_data.setdefault("azure", {}).setdefault("openai", {})["api_key"] = api_key
        
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        if deployment_name:
            config_data.setdefault("azure", {}).setdefault("openai", {})["deployment_name"] = deployment_name
        
        api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        if api_version:
            config_data.setdefault("azure", {}).setdefault("openai", {})["api_version"] = api_version
        
        # Azure Search overrides
        search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
        if search_endpoint:
            config_data.setdefault("azure", {}).setdefault("search", {})["endpoint"] = search_endpoint
        
        search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
        if search_api_key:
            config_data.setdefault("azure", {}).setdefault("search", {})["api_key"] = search_api_key
        
        search_index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
        if search_index_name:
            config_data.setdefault("azure", {}).setdefault("search", {})["index_name"] = search_index_name
        
        return config_data
    
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


import threading

_settings_lock = threading.Lock()


def get_settings(config_path: Optional[str] = None) -> Settings:
    """Get or create settings instance (thread-safe).
    
    Args:
        config_path: Optional path to config file. If not provided:
                    - Creates appsettings.json with defaults if it doesn't exist
                    - Prefers appsettings.json
                    - Falls back to config.yaml if appsettings.json doesn't exist
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        with _settings_lock:
            # Double-check locking pattern
            if _settings is None:
                if config_path:
                    # Use specified config file
                    if config_path.endswith('.json'):
                        _settings = Settings.from_json(config_path)
                    else:
                        _settings = Settings.from_yaml(config_path)
                else:
                    # Ensure appsettings.json exists with defaults
                    Settings._create_default_appsettings("appsettings.json")
                    
                    # Prefer appsettings.json, fall back to config.yaml if JSON doesn't exist
                    # (This handles edge case where creation failed)
                    if Path("appsettings.json").exists():
                        _settings = Settings.from_json("appsettings.json")
                    elif Path("config.yaml").exists():
                        _settings = Settings.from_yaml("config.yaml")
                    else:
                        # Should not reach here since _create_default_appsettings creates the file
                        raise FileNotFoundError("No configuration file found and failed to create default appsettings.json")
    return _settings
