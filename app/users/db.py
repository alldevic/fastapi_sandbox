"""
User context database provider
"""

from core.db import get_async_session
from fastapi import Depends
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync
from sqlmodel.ext.asyncio.session import AsyncSession

from .models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Get user database representation
    """
    yield SQLModelUserDatabaseAsync(session, User)
