from pydantic import BaseModel


class AnswerBase(BaseModel):
    retort: str
    is_correct: bool = False


class AnswerCreate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True
