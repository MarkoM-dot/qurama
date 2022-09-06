import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import __app_name__, __version__
from src.config import database, get_settings, init_db
from src.routers import answers, questions, tools

app = FastAPI(title=__app_name__, debug=get_settings().debug, version=__version__)

logger = logging.getLogger(__name__)

origins = ["https://localhost:3000", "http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
