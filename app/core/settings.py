"""
Settings repository
"""

import os
from typing import Any, Dict, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """
    Settings repository
    """
    DATABASE_USER: str = os.environ.get("POSTGRES_SU")
    DATABASE_PASSWORD: str = os.environ.get("POSTGRES_SU_PASS")
    DATABASE_HOST: str = os.environ.get("POSTGRES_HOST")
    DATABASE_PORT: Union[int, str] = 5432
    DATABASE_NAME: str = os.environ.get("POSTGRES_DB")
    ASYNC_DATABASE_URI: Optional[
        Any
    ] = f"postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?ssl=disable"

    @classmethod
    @validator("ASYNC_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, value: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Build connection string from args
        """
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            host=values.get("DATABASE_HOST"),
            port=values.get("DATABASE_PORT"),
            path=f"/{values.get('DATABASE_NAME') or ''}",
        )

    class Config:
        """
        BaseSettings config
        """
        case_sensitive = True
