from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_session
from src.managers import AnswerManager
from src.models import Answer
from src.schemas import AnswerRead

router = APIRouter()


@router.get("/", response_model=list[AnswerRead])
async def get_answers(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
) -> list[Answer]:
    """Return a list of answers given an offset and limit."""
    answers: list[Answer] = await AnswerManager.get_answers(offset, limit, db)
    return answers


@router.get("/{answer_id}", response_model=AnswerRead)
async def get_answer(answer_id: int, db: AsyncSession = Depends(get_session)) -> Answer:
    """Return a single answer given an id."""
    answer: Answer = await AnswerManager.get_answer(answer_id, db)
    if answer is None:
        raise HTTPException(status_code=404, detail=f"Answer {answer_id} does not exist.")
    return answer
