#!/usr/bin/env python3
"""Auth module"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Hash a password using bcrypt

    Args:
        password (str): The password to hash

    Returns:
        str: The hashed password
    """
    return bcrypt.hashpw(password.encode('utf-8'),
                         bcrypt.gensalt()).decode('utf-8')


def _generate_uuid() -> str:
    """Generate a new UUID

    Returns:
        str: A new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to manage authentication"""

    def __init__(self):
        """Initialize Auth instance with DB"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user

        Args:
            email (str): The user's email address
            password (str): The user's password

        Returns:
            User: The newly created user

        Raises:
            ValueError: If the user already exists
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials

        Args:
            email (str): The user's email address
            password (str): The user's password

        Returns:
            bool: True if credentials are valid, False otherwise
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(
                password.encode('utf-8'),
                user.hashed_password.encode('utf-8')
            ):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a session ID for a user

        Args:
            email (str): The user's email address

        Returns:
            Union[str, None]: The session ID or None if user not found
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get a user from a session ID

        Args:
            session_id (str): The session ID

        Returns:
            Union[User, None]: The user or None if not found
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session

        Args:
            user_id (int): The user's ID

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generate a password reset token

        Args:
            email (str): The user's email address

        Returns:
            str: The reset token

        Raises:
            ValueError: If user is not found
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, email: str, reset_token:
                        str, password: str) -> None:
        """Update user's password using reset token

        Args:
            email (str): The user's email address
            reset_token (str): The reset token
            password (str): The new password

        Returns:
            None

        Raises:
            ValueError: If reset token is invalid or email does not match
        """
        try:
            user = self._db.find_user_by(email=email, reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None
            )
        except NoResultFound:
            raise ValueError
