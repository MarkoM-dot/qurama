from functools import lru_cache

import pytest
from pydantic import BaseSettings
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool


class TestSettings(BaseSettings):
    env_name: str = "testing"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./test.db"
    debug: bool = True
    echo: bool = True

    class Config:
        env_file = ".env.test"


@lru_cache
def get_test_settings():
    settings = TestSettings()
    print(f"Loading settings for: {settings.env_name}")

    return settings


@pytest.fixture(name="Session")
def session_fixture():
    engine = create_engine(
        get_test_settings().db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
