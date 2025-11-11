"""
AI Bible API Package

This package provides programmatic access to the Confluence Chronicles Story Bible
repository through GitHub's API.

Main components:
- GitHubService: Low-level GitHub API wrapper
- AIBibleAPI: High-level story bible operations
- Flask server: REST API for remote access

Quick start:
    from api import create_ai_api

    api = create_ai_api()
    lexicon = api.get_master_lexicon()
    novellas = api.list_novellas()
"""

from .github_service import GitHubService, GitHubAPIError, create_service
from .ai_bible_api import AIBibleAPI, create_ai_api

__version__ = "1.0.0"
__all__ = [
    "GitHubService",
    "GitHubAPIError",
    "AIBibleAPI",
    "create_service",
    "create_ai_api"
]
