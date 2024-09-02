#!/usr/bin/env python3
"""Authentication module for the API.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class to manage API authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required for the given path."""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        path = path.rstrip('/')

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path.rstrip('/'):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get the Authorization header from the request."""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Get the current user from the request."""
        return None
