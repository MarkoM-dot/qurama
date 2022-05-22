from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING: 
    from .question import Question, QuestionRead


class AnswerBase(SQLModel):
    retort: str = Field(index=True)
    is_correct: bool


class AnswerKey(AnswerBase):

    question_id: int = Field(foreign_key="question.id")

class Answer(AnswerKey, table=True):

    id: Optional[int] = Field(primary_key=True)

    question: "Question" = Relationship(back_populates="answers")

    def __repr__(self):
        return f"Answer no.{self.id}: {self.retort}"

class AnswerRead(AnswerKey):
    id: int

class AnswerWithQuestion(AnswerRead):
    question: "QuestionRead"

class AnswerCreate(AnswerBase):
    pass
