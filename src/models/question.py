from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.config import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    inquiry = Column(String)
    publish = Column(Boolean, default=False)

    answers = relationship("Answer", back_populates="question", cascade="all, delete")

    def __repr__(self):
        return f"Question: {self.inquiry}"
