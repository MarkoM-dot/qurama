import logging
from functools import lru_cache
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Base, TestSettings, get_session
from src.main import app

logger = logging.getLogger(__name__)


@lru_cache
def get_test_settings() -> TestSettings:
    """Return cached settings."""
    settings = TestSettings()
    logger.info(f"Loading settings for: {settings.env_name}")

    return settings


engine = create_async_engine(get_test_settings().db_url, future=True, echo=get_test_settings().echo)


async def override_get_session() -> AsyncGenerator:
    """Create models in test DB and generate an async session."""
    async with engine.begin() as conn:
        logger.info("Revving the engine...")
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as err:
            logger.exception(err)


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
async def client() -> AsyncGenerator:
    """Generate an async client for async http requests."""
    async with AsyncClient(app=app, base_url="http://testserver") as async_client:
        yield async_client
