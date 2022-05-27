from pydantic import BaseModel, validator

from .answer import AnswerCreate, AnswerRead


class QuestionBase(BaseModel):
    inquiry: str
    publish: bool


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
        orm_mode = True


class QuestionDelete(BaseModel):
    pass


class QuestionRead(QuestionBase):
    id: int
    answers: list[AnswerRead]

    class Config:
        orm_mode = True
