from sqlalchemy.orm import Session
from src.models import Answer, Question, QuestionCreate


def get_question(db: Session, question_id: int):
    return db.query(Question).filter(Question.id == question_id).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Question).offset(skip).limit(limit).all()


def create_question(db: Session, question: QuestionCreate):
    question_data = question.dict()
    answers_data = question_data.pop("answers")
    db_question = Question(**question_data)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    question_id = db_question.id
    for answer in answers_data:
        answer["question_id"] = question_id
        db_answer = Answer(**answer)
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)
    print(db_question)
    return db_question


def delete_question(db: Session, question_id: int):
    db.query(Question).filter(Question.id == question_id).delete()
    db.commit()
