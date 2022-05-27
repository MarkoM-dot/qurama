import logging

from fastapi import FastAPI

from src.config import get_settings

from .config import database, init_db
from .routers import answers, questions, tools

app = FastAPI(title="QURAMA REST API", debug=get_settings().debug)

logger = logging.getLogger(__name__)


@app.on_event("startup")
async def startup() -> None:
    """Initialize DB and connect to it with an async driver."""
    logger.info("Initializing database...")
    await init_db()
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Disconnect when shutting down."""
    logger.info("Shutting down...")
    await database.disconnect()


app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(answers.router, prefix="/answers", tags=["Answers"])
app.include_router(tools.router, prefix="/tools", tags=["Tools"])
