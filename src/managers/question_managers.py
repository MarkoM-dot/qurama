from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Answer, Question, QuestionCreate


async def get_question(db: AsyncSession, question_id: int):
    q = await db.get(Question, question_id)
    return q


async def get_questions(db: AsyncSession, offset: int = 0, limit: int = 100):
    query = await db.execute(select(Question).offset(offset).limit(limit))
    return query.scalars().all()


async def create_question(db: AsyncSession, question: QuestionCreate):
    db_question = question.dict()
    db_answers = db_question.pop("answers")
    db_question = Question(**db_question)

    db.add(db_question)
    await db.commit()
    await db.refresh(db_question)

    for answer in db_answers:
        answer["question_id"] = db_question.id
        db_answer = Answer(**answer)

        db.add(db_answer)
        await db.commit()
        await db.refresh(db_answer)
    print("db question: ", db_question)

    return db_question

