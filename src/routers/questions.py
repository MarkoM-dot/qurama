from fastapi import HTTPException, APIRouter, Depends
from src import managers, schemas
from sqlalchemy.orm import Session
from src.database import get_db

router = APIRouter()


@router.get("/", response_model=list[schemas.Question])
async def get_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = managers.get_questions(db, skip=skip, limit=limit)
    return questions


@router.get("/{question_id}", response_model=schemas.Question)
async def get_question(question_id: int, db: Session = Depends(get_db)):
    db_question = managers.get_question(db, question_id=question_id)
    if db_question is None:
        raise HTTPException(
            status_code=404,
            detail=f"Question {question_id} does not exist.",
        )
    return db_question


@router.post("/", response_model=schemas.Question, status_code=201)
async def post_question(
    question: schemas.QuestionCreate, db: Session = Depends(get_db)
):
    return managers.create_question(db=db, question=question)


@router.delete("/{question_id}", response_model=schemas.QuestionDelete)
async def delete_question(question_id: int, db: Session = Depends(get_db)):
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
