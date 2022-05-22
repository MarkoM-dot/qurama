from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import get_session
from src.models import Answer

class AnswerManager(BaseModel):
    
    @classmethod
    async def get_answer(cls, answer_id: int, db: AsyncSession = Depends(get_session)):
        query = await db.get(Answer, answer_id)
        return query
