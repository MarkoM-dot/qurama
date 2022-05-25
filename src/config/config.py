import logging
from functools import lru_cache

from pydantic import BaseSettings

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    env_name: str = "local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./db.db"
    debug: bool = True
    echo: bool = True


class DevSettings(Settings):
    class Config:
        env_file = ".env"


class TestSettings(Settings):
    class Config:
        env_file = ".env.test"


@lru_cache
def get_settings() -> DevSettings:
    settings = DevSettings()
    logger.info(f"Loading settings for: {settings.env_name}")

    return settings
