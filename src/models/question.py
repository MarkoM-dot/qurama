from sqlmodel import SQLModel, Field, Relationship
from pydantic import validator
from typing import Optional
from .answer import Answer, AnswerRead, AnswerCreate



class QuestionBase(SQLModel):

    inquiry: str = Field(index=True)
    publish: bool = Field(default=False)

    def __repr__(self):
        return f"Question: {self.inquiry}"


class Question(QuestionBase, table=True):

    id: Optional[int] = Field(primary_key=True)
    answers: list[Answer] = Relationship(back_populates="question")


class QuestionRead(QuestionBase):
    id: int

class QuestionWithAnswers(QuestionRead):
    answers: list[AnswerRead]


class QuestionCreate(QuestionBase):

    answers: list[AnswerCreate]

    @validator("answers", check_fields=False)
    def check_for_four_answers(cls, v):
        assert len(v) == 4, "Please provide 4 answers."
        return v

    @validator("answers", check_fields=False)
    def check_one_correct_answer(cls, v):
        correct_count = 0
        for answer in v:
            if answer.is_correct:
                correct_count += 1
        assert correct_count == 1, "Please select exactly one correct answer."
        return v

    class Config:
        schema_extra = {
            "inquiry": "Amarelle, May Duke, and Morello are all types of which fruit?",
            "publish": True,
            "answers": [
                {"retort": "strawberry", "is_correct": False},
                {"retort": "cherry", "is_correct": True},
                {"retort": "tomato", "is_correct": False},
                {"retort": "pear", "is_correct": False},
            ],
        }
