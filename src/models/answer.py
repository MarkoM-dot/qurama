from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .question import Question


class AnswerBase(SQLModel):
    text: str
    is_correct: bool


class Answer(AnswerBase, table=True):

    id: Optional[int] = Field(primary_key=True, index=True)

    question_id: int = Field(foreign_key="question.id")
    question: Optional["Question"] = Relationship(back_populates="answers")

    def __repr__(self):
        return f"Answer no.{self.id}: {self.text}"


class AnswerCreate(AnswerBase):
    pass
