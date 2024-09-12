#!/usr/bin/env python3
"""User model module"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    """User class for SQLAlchemy mapping to 'users' table

    Attributes:
        id (int): The user's ID
        email (str): The user's email address
        hashed_password (str): The hashed password
        session_id (str): The session ID
        reset_token (str): The reset token
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
