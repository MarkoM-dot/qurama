from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from src.config import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    inquiry = Column(String, index=True)
    publish = Column(Boolean, default=False, index=True)

    answers = relationship("Answer", back_populates="question", cascade="all, delete")

    def __repr__(self):
        return f"Question: {self.inquiry}"

    def __str__(self):
        return f"{self.id}: {self.inquiry}"
