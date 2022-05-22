from functools import lru_cache

from pydantic import BaseSettings


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
def get_settings():
    settings = DevSettings()
    print(f"Loading settings for: {settings.env_name}")

    return settings
