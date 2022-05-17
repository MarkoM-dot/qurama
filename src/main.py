from fastapi import FastAPI
from sqlmodel.main import SQLModel
from .database import engine
from .routers import questions, tools

SQLModel.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(tools.router, prefix="/tools", tags=["Tools"])
