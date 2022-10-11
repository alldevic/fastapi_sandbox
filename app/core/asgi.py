"""
core
"""

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from users import current_active_user, users_routes
from users.models import User
from utils.debug_middleware import toolbar
from utils.rapidoc import get_rapidoc_html

from .db import get_async_session
from .models import Song, SongCreate

app = FastAPI(debug=True, docs_url=None, redoc_url=None)

app.add_middleware(**toolbar)

app.mount("/static", StaticFiles(directory="static"), name="static")

for route in users_routes:
    app.include_router(**route)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    RapiDoc documentation
    """
    return get_rapidoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - RapiDoc",
        rapidoc_js_url="/static/js/rapidoc-min.js",
        add_debug_support=True
    )

@app.get("/ping", tags=["test"])
async def pong():
    """
    Hello world
    """
    return {"ping": "pong!"}


@app.get("/songs", response_model=list[Song], tags=['songs'])
async def get_songs(session: AsyncSession = Depends(get_async_session)):
    """
    Get all songs from db
    """
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    await session.close()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


@app.post("/songs", tags=['songs'])
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Add new song to db
    """
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    await session.close()
    return song


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    """
    Auth route sample
    """
    return {"message": f"Hello {user.email}!"}
