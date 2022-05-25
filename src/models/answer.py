from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    retort = Column(String)
    is_correct = Column(Boolean, default=False)

    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"Answer no.{self.id}: {self.retort}"

    def __str__(self):
        return f"{self.id}: {self.retort}"
