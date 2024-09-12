#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class for database operations"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Create and return a new session"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database

        Args:
            email (str): The user's email address
            hashed_password (str): The user's hashed password

        Returns:
            User: The newly created user
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            User: The user found

        Raises:
            NoResultFound: If no user is found
            InvalidRequestError: If invalid arguments are provided
        """
        session = self._session
        if not kwargs:
            raise InvalidRequestError("No arguments provided")
        valid_attrs = [
            'id',
            'email',
            'hashed_password',
            'session_id',
            'reset_token',
        ]
        for key in kwargs.keys():
            if key not in valid_attrs:
                raise InvalidRequestError(f"Invalid attribute: {key}")
        user = session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes

        Args:
            user_id (int): The user's ID
            **kwargs: Arbitrary keyword arguments of attributes to update

        Raises:
            ValueError: If an attribute does not exist
        """
        session = self._session
        user = self.find_user_by(id=user_id)
        valid_attrs = [
            'email',
            'hashed_password',
            'session_id',
            'reset_token',
        ]
        for key, value in kwargs.items():
            if key not in valid_attrs:
                raise ValueError(f"Attribute {key} does not exist")
            setattr(user, key, value)
        session.commit()
