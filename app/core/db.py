"""
Database provider
"""

from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession

from .settings import Settings

settings = Settings()
engine = AsyncEngine(create_engine(settings.ASYNC_DATABASE_URI, echo=True, future=True))
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session
    """
    async with async_session_maker() as session:
        yield session
