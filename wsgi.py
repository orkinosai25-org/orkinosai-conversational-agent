"""WSGI entry point for Azure App Service.

This module exposes the Flask application as ``app`` so that Gunicorn (and
Azure App Service's Oryx build system) can discover and serve it.

Startup command (set in Azure Portal or workflow):
    gunicorn --bind=0.0.0.0 --timeout 600 wsgi:app
"""

from src.api import create_app

app = create_app()
