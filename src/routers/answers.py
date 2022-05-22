from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.managers import AnswerManager
from src.config import get_session
from src.models import Answer
from src.schemas import AnswerRead

router = APIRouter()


@router.get("/")
async def get_answers(db: AsyncSession = Depends(get_session)):
    query = await db.execute(select(Answer))
    return query.all()


@router.get("/{answer_id}")
async def get_answer(answer_id: int, db: AsyncSession = Depends(get_session)):
    answer = await AnswerManager.get_answer(answer_id, db)
    if answer is None:
        raise HTTPException(status_code=404, detail=f"Answer no.{answer_id} not found.")
    return answer
