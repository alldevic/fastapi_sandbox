"""
User db models and api schemas
"""

import uuid

from fastapi_users import schemas
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB


class User(SQLModelBaseUserDB, table=True):
    """
    Database User model
    """

class UserRead(schemas.BaseUser[uuid.UUID]):
    """
    Schema for reading user
    """

class UserCreate(schemas.BaseUserCreate):
    """
    Schema for creating user (wout id)
    """


class UserUpdate(schemas.BaseUserUpdate):
    """
    Schema for update user info
    """
