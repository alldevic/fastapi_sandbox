"""
core
"""

from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from utils.debug_middleware import toolbar
from utils.swaggerui import swagger_ui_params

from .db import get_session
from .models import Song, SongCreate

app = FastAPI(debug=True, swagger_ui_parameters=swagger_ui_params)
app.add_middleware(**toolbar)


@app.get("/ping")
async def pong():
    """
    Hello world
    """
    return {"ping": "pong!"}


@app.get("/songs", response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    """
    Get all songs from db
    """
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


@app.post("/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    """
    Add new song to db
    """
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song
