from fastapi import FastAPI
from .routers import questions, tools
from .database import create_db_and_tables

app = FastAPI(debug=True)

app.include_router(questions.router, prefix="/questions", tags=["Questions"])
app.include_router(tools.router, prefix="/tools", tags=["Tools"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
