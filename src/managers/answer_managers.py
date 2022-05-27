from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.config import get_session
from src.models import Answer


class AnswerManager(BaseModel):
    @classmethod
    async def get_answer(cls, answer_id: int, db: AsyncSession = Depends(get_session)) -> Answer:
        query: Answer = await db.get(Answer, answer_id)
        return query

    @classmethod
    async def get_answers(
        cls, offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
    ) -> list[Answer]:
        query: Answer = await db.execute(select(Answer).offset(offset).limit(limit))
        return query.scalars().all()
