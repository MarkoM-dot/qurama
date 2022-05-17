from pydantic import BaseModel, Field


class AnswerBase(BaseModel):
    text: str = Field(min_length=1, max_length=255)
    is_correct: bool = False


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int

    class Config:
        orm_mode = True
