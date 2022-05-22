from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import databases
from sqlmodel import SQLModel
from src.config import get_settings
import logging


logger = logging.getLogger(__name__)
database = databases.Database(get_settings().db_url)

engine = create_async_engine(
    get_settings().db_url, future=True, echo=get_settings().echo
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as err:
            logger.exception(err)
