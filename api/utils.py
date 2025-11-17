"""Utility functions for the API app."""

import os


def validate_environment():
    """
    Validate that all required environment variables are set.

    Returns:
        tuple: (is_valid, missing_vars)
    """
    required_vars = {
        "SECRET_KEY": "Django secret key for cryptographic signing",
    }

    optional_vars = {
        "OPENAI_API_KEY": "OpenAI API key for AI task suggestions",
        "DATABASE_URL": "Database connection URL",
    }

    missing = []
    warnings = []

    for var, description in required_vars.items():
        if (
            not os.getenv(var)
            or os.getenv(var) == "fallback-secret-key-change-in-production"
        ):
            missing.append(f"{var}: {description}")

    for var, description in optional_vars.items():
        if not os.getenv(var):
            warnings.append(f"{var}: {description}")

    return len(missing) == 0, missing, warnings
