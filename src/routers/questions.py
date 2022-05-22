from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_session
from src.managers import QuestionManager
from src.schemas import QuestionCreate, QuestionRead

router = APIRouter()


@router.get("/")
async def get_questions(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
):
    questions = await QuestionManager.get_questions(db, offset, limit)
    return questions


@router.get("/{question_id}")
async def get_question(question_id: int, db: AsyncSession = Depends(get_session)):
    question = await QuestionManager.get_question(db, question_id=question_id)
    if question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    return question


@router.post("/", status_code=201)
async def post_question(
    question: QuestionCreate, db: AsyncSession = Depends(get_session)
):
    question = await QuestionManager.create_question(db=db, question=question)
    return question


@router.delete("/{question_id}")
async def delete_question(question_id: int, db: AsyncSession = Depends(get_session)):
    question = await QuestionManager.get_question(db, question_id=question_id)
    if question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    await db.delete(question)
    await db.commit()
    return {"message": f"Successfully deleted Question {question_id}."}


# @router.put("/questions/{question_id}")
# async def update_question(question_id: int, response_model=schemas.Question, status_code=200)
#    return {"status": "Successfully updated question."}
