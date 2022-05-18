from sqlmodel import SQLModel, Field
from pydantic import validator
from .answer import Answer, AnswerCreate


class QuestionBase(SQLModel):
    text: str = Field(min_length=1)
    publish: bool = False


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


class QuestionDelete(SQLModel):
    pass


class Question(QuestionBase):
    id: int
    answers: list[Answer]

    class Config:
        orm_mode = True
