from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config import get_session
from src.managers import AnswerManager
from src.models import Answer
from src.schemas import AnswerRead

router = APIRouter()


@router.get("/")
async def get_answers(offset: int, limit: int, db: AsyncSession = Depends(get_session)) -> list[Answer]:
    answers: list[Answer] = await AnswerManager.get_answers(offset, limit, db)
    return answers


@router.get("/{answer_id}")
async def get_answer(answer_id: int, db: AsyncSession = Depends(get_session)) -> Answer:
    answer: Answer = await AnswerManager.get_answer(answer_id, db)
    if answer is None:
        raise HTTPException(status_code=404, detail=f"Answer no.{answer_id} not found.")
    return answer
