from typing import AsyncGenerator
from asyncio import get_event_loop
from functools import lru_cache
from httpx import AsyncClient

from src.main import app
import pytest
from pydantic import BaseSettings
from src.database import Base
from sqlalchemy.ext.asyncio import create_async_engine


class TestSettings(BaseSettings):
    env_name: str = "testing"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite://"
    debug: bool = True
    echo: bool = True

    class Config:
        env_file = ".env.test"


@lru_cache
def get_test_settings():
    settings = TestSettings()
    print(f"Loading settings for: {settings.env_name}")

    return settings



#@pytest.mark.skip("later bring in in-mem db")
#@pytest.fixture
#def get_app():
#    engine = create_async_engine(
#    get_test_settings().db_url,
#    future=True,
#    echo=get_test_settings().echo
#    )
#
#    Base.metadata.create_all(engine)
#
#    return app

@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client

#@pytest.fixture(scope="module")
#def event_loop():
#    loop = get_event_loop()
#
#    yield loop
#    loop.close()
