from sqlmodel import SQLModel, Field


class Question(SQLModel, table=True):

    id: int = Field(primary_key=True, index=True)
    text: str
    publish: bool = Field(default=False)

    def __repr__(self):
        return f"Question no.{self.id}: {self.text}"


class Answer(SQLModel, table=True):

    id: int = Field(primary_key=True, index=True)
    text: str 
    is_correct: bool = Field(default=False)
    question_id: int = Field(foreign_key="question.id")

    def __repr__(self):
        return f"Answer no.{self.id}: {self.text}"
