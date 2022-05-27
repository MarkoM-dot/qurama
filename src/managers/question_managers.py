from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src import schemas
from src.config import get_session
from src.models import Answer, Question


class QuestionManager(BaseModel):
    @classmethod
    async def get_question(
        cls, question_id: int, db: AsyncSession = Depends(get_session)
    ) -> Question:
        query: Question = await db.execute(
            select(Question)
            .where(Question.id == question_id)
            .options(selectinload(Question.answers))
        )
        return query.scalar()

    @classmethod
    async def get_questions(
        cls, offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
    ) -> list[Question]:
        query: Question = await db.execute(
            select(Question).offset(offset).limit(limit).options(selectinload(Question.answers))
        )
        return query.scalars().all()

    @classmethod
    async def create_question(
        cls, question: schemas.QuestionCreate, db: AsyncSession = Depends(get_session)
    ) -> Question:
        new_question: Question = Question(inquiry=question.inquiry, publish=question.publish)
        db.add(new_question)
        await db.commit()
        await db.refresh(new_question)

        for answer in question.answers:
            new_answer: Answer = Answer(
                retort=answer.retort,
                is_correct=answer.is_correct,
                question_id=new_question.id,
            )
            db.add(new_answer)
            await db.commit()
            await db.refresh(new_answer)

        query: Question = await db.execute(
            select(Question)
            .where(Question.id == new_question.id)
            .options(selectinload(Question.answers))
        )
        return query.scalar()

    @classmethod
    async def delete_question(
        cls, question: Question, db: AsyncSession = Depends(get_session)
    ) -> None:
        await db.delete(question)
        await db.commit()
