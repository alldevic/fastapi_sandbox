"""
Database, request and responses models
"""
from typing import Optional

from sqlmodel import Field, SQLModel


class SongBase(SQLModel):
    """
    Base Song model
    """
    name: str
    artist: str
    year: Optional[int] = None


class Song(SongBase, table=True):
    """
    Database Song model
    """
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    """
    New instance Song model
    """
