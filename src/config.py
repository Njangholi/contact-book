"""
Application configuration module.

This module defines base paths and database configuration.
The database URL is resolved from environment variables when available,
with a safe fallback to a local SQLite database for development
and testing purposes.
"""

import os

# Absolute path to the directory containing this file.
# Used as a stable reference point for resolving relative paths.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database connection URL.
# Priority:
# 1. Use DATABASE_URL from environment variables (production / CI).
# 2. Fallback to a local SQLite database for development and testing.
DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'database/contacts.db')}"
)
