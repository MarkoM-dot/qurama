from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .answer import Answer, AnswerCreate
from pydantic import validator


class QuestionBase(SQLModel):

    text: str
    publish: bool = Field(default=False)

    def __repr__(self):
        return f"Question: {self.text}"


class Question(QuestionBase, table=True):

    id: Optional[int] = Field(primary_key=True, index=True)
    answers: list[Answer] = Relationship(back_populates="question")


class QuestionCreate(QuestionBase):
    
    answers: list[AnswerCreate]
    
    @validator("answers")
    def check_for_four_answers(cls, v):
        assert len(v) == 4, "Please provide 4 answers."
        return v

    @validator("answers")
    def check_one_correct_answer(cls, v):
        correct_count = 0
        for answer in v:
            if answer.is_correct:
                correct_count += 1
        assert correct_count == 1, "Please select exactly one correct answer."
        return v
