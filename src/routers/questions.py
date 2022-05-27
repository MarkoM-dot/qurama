from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import get_session
from src.managers import QuestionManager
from src.models import Question
from src.schemas import QuestionCreate, QuestionRead

router = APIRouter()


@router.get("/", response_model=list[QuestionRead])
async def get_questions(
    offset: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
) -> list[Question]:
    """Return all questions from DB."""
    questions: list[Question] = await QuestionManager.get_questions(offset, limit, db)
    return questions


@router.get("/{question_id}", response_model=QuestionRead)
async def get_question(question_id: int, db: AsyncSession = Depends(get_session)) -> Question:
    """Return a particular question from DB given an id."""
    question: Question = await QuestionManager.get_question(question_id, db)
    if question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    return question


@router.post("/", response_model=QuestionRead, status_code=201)
async def post_question(
    question: QuestionCreate, db: AsyncSession = Depends(get_session)
) -> Question:
    """Create a question in DB and return said question."""
    created_question: Question = await QuestionManager.create_question(db=db, question=question)
    return created_question


@router.delete("/{question_id}")
async def delete_question(
    question_id: int, db: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    """Delete a particular question given an id."""
    question = await QuestionManager.get_question(question_id, db)
    if question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    await QuestionManager.delete_question(question, db)
    return {"message": f"Successfully deleted Question {question_id}."}


# @router.put("/questions/{question_id}")
# async def update_question(question_id: int, response_model=schemas.Question, status_code=200)
#    return {"status": "Successfully updated question."}
