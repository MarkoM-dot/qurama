from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Answer, Question, QuestionCreate


async def get_question(db: AsyncSession, question_id: int):
    q = await db.execute(select(Question).where(Question.id == question_id))
    return q


async def get_questions(db: AsyncSession, skip: int = 0, limit: int = 100):
    q = await db.execute(select(Question).offset(skip).limit(limit))
    return q


async def create_question(db: AsyncSession, question: QuestionCreate):
    question_data = question.dict()
    answers_data = question_data.pop("answers")
    db_question = Question(**question_data)
    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)

    question_id = db_question.id
    for answer in answers_data:
        answer["question_id"] = question_id
        db_answer = Answer(**answer)
        db.add(db_answer)
        await db.commit()
        await db.refresh(db_answer)
    print(db_question)
    return db_question


async def delete_question(db: AsyncSession, question_id: int):
    await db.execute(select(Question).where(Question.id == question_id).delete())
    await db.commit()
