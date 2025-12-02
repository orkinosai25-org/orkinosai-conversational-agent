"""Main entry point for the conversational agent API server."""

import os
import logging
from pathlib import Path

from src.api import create_app
from src.config import get_settings


def main():
    """Start the conversational agent API server."""
    # Ensure logs directory exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Load settings (auto-detects appsettings.json or config.yaml)
    config_path = os.getenv("CONFIG_PATH")
    settings = get_settings(config_path)
    
    # Configure logging to file
    log_file = Path(settings.logging.file)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter(settings.logging.format))
    
    logger = logging.getLogger()
    logger.addHandler(file_handler)
    
    # Create and run app
    app = create_app(config_path)
    
    print(f"Starting {settings.agent.name} v{settings.agent.version}")
    print(f"Server running on http://{settings.server.host}:{settings.server.port}")
    print(f"Logs: {log_file}")
    
    app.run(
        host=settings.server.host,
        port=settings.server.port,
        debug=settings.server.debug
    )


if __name__ == "__main__":
    main()
