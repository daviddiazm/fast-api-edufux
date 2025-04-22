from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from database import engine

Base = declarative_base()

class Questions(Base):
    __tablename__ = "questions"
    id = (Column(Integer, primary_key=True, index=True))
    question_text = (Column(String, index=True))
    form_id = (Column(Integer, ForeignKey("forms.id")))
    
    form = relationship("Forms", back_populates="questions")
    choices = relationship("Choices", back_populates="question")

class Choices(Base):
    __tablename__ = "choices"
    id = (Column(Integer, primary_key=True, index=True))
    choice_text = (Column(String, index=True))
    is_correct = (Column(Boolean, default=False))
    question_id = (Column(Integer, ForeignKey("questions.id")))
    
    question = relationship("Questions", back_populates="choices")


class Forms(Base):
    __tablename__ = "forms"
    id = (Column(Integer, primary_key=True, index=True))
    name_form = (Column(String, index=True))
    description_form = (Column(String))
    
    questions = relationship("Questions", back_populates="form")
