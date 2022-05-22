from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pydantic import BaseModel

from src import schemas
from src.models import Answer, Question

class QuestionManager(BaseModel):

    @classmethod
    async def get_question(cls, db: AsyncSession, question_id: int) -> list[Question]:
        query = await db.execute(
            select(Question)
            .where(Question.id == question_id)
            .options(selectinload(Question.answers))
        )
        return query.scalar()


    @classmethod
    async def get_questions(cls, db: AsyncSession, offset: int = 0, limit: int = 100):
        query = await db.execute(
            select(Question)
            .offset(offset)
            .limit(limit)
            .options(selectinload(Question.answers))
        )
        return query.scalars().all()


    @classmethod
    async def create_question(cls, db: AsyncSession, question: schemas.QuestionCreate):
        new_question = Question(inquiry=question.inquiry, publish=question.publish)
        db.add(new_question)
        await db.commit()
        await db.refresh(new_question)

        for answer in question.answers:
            new_answer = Answer(
                retort=answer.retort,
                is_correct=answer.is_correct,
                question_id=new_question.id,
            )
            db.add(new_answer)
            await db.commit()
            await db.refresh(new_answer)

        query = await db.execute(
            select(Question)
            .where(Question.id == new_question.id)
            .options(selectinload(Question.answers))
        )
        return query.scalar()
