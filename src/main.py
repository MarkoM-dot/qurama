from fastapi import FastAPI

from src.config import get_settings
from .routers import questions, tools
from .database import database, init_db

app = FastAPI(title="QURAMA REST API", debug=get_settings().debug)


@app.on_event("startup")
async def startup():
    await init_db()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(tools.router, prefix="/tools", tags=["Tools"])
