from fastapi import HTTPException, APIRouter, Depends
from src.models import Answer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.database import get_session


router = APIRouter()


@router.get("/", response_model=list[Answer])
async def get_answers(db: AsyncSession = Depends(get_session)):
    query = await db.execute(select(Answer))
    return query.scalars().all()


@router.get("/{answer_id}", response_model=Answer)
async def get_answer(answer_id: int, db: AsyncSession = Depends(get_session)):
    query = await db.get(Answer, answer_id)
    if query is None:
        raise HTTPException(status_code=404, detail=f"Answer no.{answer_id} not found.")
    return query
