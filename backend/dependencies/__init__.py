"""
FastAPI Dependencies

This package contains reusable dependencies for FastAPI endpoints.
"""

from dependencies.auth import get_current_user

__all__ = ["get_current_user"]
