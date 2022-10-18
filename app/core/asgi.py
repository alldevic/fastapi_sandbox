"""
core
"""

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_amis_admin.admin.settings import Settings as AmisSettings
from fastapi_amis_admin.admin.site import AdminSite
from openapi import CustomOpenapi
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from users import current_active_user, users_routes
from users.models import User
from utils.debug_middleware import toolbar

from .admin import SongsAdmin
from .db import get_async_session
from .models import Song, SongCreate
from .settings import Settings

app = FastAPI(debug=True, docs_url=None, redoc_url=None)

if app.debug:
    app.add_middleware(**toolbar)

app.mount("/static", StaticFiles(directory="static"), name="static")

for route in users_routes:
    app.include_router(**route)

site = AdminSite(
    settings=AmisSettings(
        database_url_async=Settings().ASYNC_DATABASE_URI,
        debug=app.debug,
    ),
)
site.register_admin(SongsAdmin)
site.mount_app(app)

CustomOpenapi(app).register()


@app.get("/ping", tags=["test"])
async def pong():
    """
    Hello world
    """
    return {"ping": "pong!"}


@app.get("/songs", response_model=list[Song], tags=["songs"])
async def get_songs(session: AsyncSession = Depends(get_async_session)):
    """
    Get all songs from db
    """
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    await session.close()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


@app.post("/songs", tags=["songs"])
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
