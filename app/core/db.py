"""
Database provider
"""

from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession

from .settings import Settings

settings = Settings()

engine = AsyncEngine(create_engine(settings.ASYNC_DATABASE_URI, echo=True, future=True))

async def init_db():
    """
    Init databse
    """
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """
    Get active session
    """
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session