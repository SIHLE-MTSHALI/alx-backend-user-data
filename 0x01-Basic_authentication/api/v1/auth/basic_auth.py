#!/usr/bin/env python3
"""Basic authentication module for the API.
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class to manage API authentication."""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract the Base64 part of the Authorization header."""
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Decode the Base64 authorization header."""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extract user credentials from the decoded authorization header."""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(':', 1)
        return credentials[0], credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Get User instance based on email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve the User instance for a request."""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        if b64_auth_token is None:
            return None

        decoded_auth_token = self.decode_base64_authorization_header(
            b64_auth_token)
        if decoded_auth_token is None:
            return None

        email, password = self.extract_user_credentials(decoded_auth_token)
        if email is None or password is None:
            return None

        return self.user_object_from_credentials(email, password)
