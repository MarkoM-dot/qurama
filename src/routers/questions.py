from fastapi import HTTPException, APIRouter, Depends
from src import managers
from src.models import Question, QuestionCreate
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session

router = APIRouter()


@router.get("/", response_model=list[Question])
async def get_questions(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_session)
):
    questions = managers.get_questions(db, skip=skip, limit=limit)
    return questions


@router.get("/{question_id}", response_model=Question)
async def get_question(question_id: int, db: AsyncSession = Depends(get_session)):
    db_question = managers.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    return db_question


@router.post("/", response_model=Question, status_code=201)
async def post_question(
    question: QuestionCreate, db: AsyncSession = Depends(get_session)
):
    return managers.create_question(db=db, question=question)


@router.delete("/{question_id}")
async def delete_question(question_id: int, db: AsyncSession = Depends(get_session)):
    db_question = managers.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    managers.delete_question(db, question_id=db_question.id)
    return {"message": "Successfully deleted question."}


# @router.put("/questions/{question_id}")
# async def update_question(question_id: int, response_model=schemas.Question, status_code=200)
#    return {"status": "Successfully updated question."}
