from fastapi import FastAPI

from src.config import get_settings
from .routers import questions, tools
from .database import create_db_and_tables

app = FastAPI(debug=get_settings().debug)

app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(tools.router, prefix="/tools", tags=["Tools"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
