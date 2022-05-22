from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import get_session
from src.models import Answer
from src.schemas import AnswerRead

router = APIRouter()


@router.get("/", response_model=list[AnswerRead])
async def get_answers(db: AsyncSession = Depends(get_session)):
    query = await db.execute(select(Answer))
    return query.all()


@router.get("/{answer_id}", response_model=AnswerRead)
async def get_answer(answer_id: int, db: AsyncSession = Depends(get_session)):
    query = await db.get(Answer, answer_id)
    if query is None:
        raise HTTPException(status_code=404, detail=f"Answer no.{answer_id} not found.")
    return query
