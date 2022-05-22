from asyncio import get_event_loop
from functools import lru_cache
from typing import AsyncGenerator
import logging

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import TestSettings
from src.database import Base
from src.main import app


logger = logging.getLogger(__name__)

@lru_cache
def get_test_settings():
    settings = TestSettings()
    logger.info(f"Loading settings for: {settings.env_name}")

    return settings


# @pytest.mark.skip("later bring in in-mem db")
# @pytest.fixture
# def get_app():
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
