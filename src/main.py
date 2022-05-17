from fastapi import FastAPI
from .database import engine
from . import models
from .routers import questions, tools

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(tools.router, prefix="/tools", tags=["Tools"])
