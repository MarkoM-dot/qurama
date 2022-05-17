from .database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    publish = Column(Boolean, default=False)
    answers = relationship(
        "Answer", backref="question", cascade="all,delete, delete-orphan"
    )

    def __repr__(self):
        return f"Question no.{self.id}: {self.text}"


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    is_correct = Column(Boolean, default=False)
    question_id = Column(Integer, ForeignKey("questions.id"))

    def __repr__(self):
        return f"Answer no.{self.id}: {self.text}"
