from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from database import engine

Base = declarative_base()

class Questions(Base):
    __tablename__ = "questions"
    id = (Column(Integer, primary_key=True, index=True))
    question_text = (Column(String, index=True))
    
    choices = relationship("Choices", back_populates="question")

class Choices(Base):
    __tablename__ = "choices"
    id = (Column(Integer, primary_key=True, index=True))
    choice_text = (Column(String, index=True))
    is_correct = (Column(Boolean, default=False))
    question_id = (Column(Integer, ForeignKey("questions.id")))
    
    question = relationship("Questions", back_populates="choices")