"""Tests for configuration management."""

import os
import pytest
from pathlib import Path

from src.config import Settings


def test_settings_env_substitution():
    """Test environment variable substitution in settings."""
    # Set test environment variables
    os.environ["TEST_ENDPOINT"] = "https://test.openai.azure.com/"
    os.environ["TEST_API_KEY"] = "test-key"
    os.environ["TEST_DEPLOYMENT"] = "test-deployment"
    
    # Test data with environment variable references
    test_data = {
        "azure": {
            "openai": {
                "endpoint": "${TEST_ENDPOINT}",
                "api_key": "${TEST_API_KEY}",
                "deployment_name": "${TEST_DEPLOYMENT}"
            }
        }
    }
    
    # Substitute environment variables
    result = Settings._substitute_env_vars(test_data)
    
    assert result["azure"]["openai"]["endpoint"] == "https://test.openai.azure.com/"
    assert result["azure"]["openai"]["api_key"] == "test-key"
    assert result["azure"]["openai"]["deployment_name"] == "test-deployment"


def test_settings_nested_substitution():
    """Test nested environment variable substitution."""
    os.environ["NESTED_VAR"] = "nested-value"
    
    test_data = {
        "level1": {
            "level2": {
                "level3": "${NESTED_VAR}"
            }
        },
        "list": ["${NESTED_VAR}", "static-value"]
    }
    
    result = Settings._substitute_env_vars(test_data)
    
    assert result["level1"]["level2"]["level3"] == "nested-value"
    assert result["list"][0] == "nested-value"
    assert result["list"][1] == "static-value"


def test_settings_missing_env_var():
    """Test handling of missing environment variables."""
    test_data = {
        "value": "${NONEXISTENT_VAR}"
    }
    
    result = Settings._substitute_env_vars(test_data)
    
    # Should return the original string if env var doesn't exist
    assert result["value"] == "${NONEXISTENT_VAR}"
