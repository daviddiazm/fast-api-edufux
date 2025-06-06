from fastapi import FastAPI, Body, Depends
# from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from typing import List, Annotated
from database import get_db, engine
from models import Base, Questions, Choices, Forms
import models

app = FastAPI()

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

class FromsBase(BaseModel):
    name_form: str
    description_form: str
    questions: List[QuestionBase]


@app.get("/check_connection")
def check_connection(db: Session = Depends(get_db)):
    with db:
        result = db.execute(text("SELECT 1")).scalar()
        return {"connection": "successful" if result == 1 else "failed"}


@app.get("/", tags=["home"])
def home():
    return "hola mundo"

# questions

@app.get("/questions", tags=["questions"])
def get_questions(db: Session = Depends(get_db)):
    return db.query(Questions).options(joinedload(Questions.choices)).all()

@app.get("/choices", tags=["questions"])
def get_choices(db: Session = Depends(get_db)):
    db_choices = db.query(Choices).all()
    return db_choices

@app.post("/questions", tags=["questions"])
async def post_question(question: QuestionBase, db: Session = Depends(get_db)):
    db_question = Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)
    db.commit()

@app.get("/forms", tags=["questions"])
def get_fomrs(db: Session = Depends(get_db)):
    return db.query(Forms).options(
        joinedload(Forms.questions).options(
            joinedload(Questions.choices))
        ).all()

@app.post("/forms", tags=["questions"])
async def post_from(form: FromsBase, db: Session = Depends(get_db)):
    db_form = Forms(name_form = form.name_form, description_form = form.description_form )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    for question in form.questions:
        db_question = Questions(
            question_text=question.question_text,
            form_id=db_form.id
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        for choice in question.choices:
            db_choice = Choices(
                choice_text=choice.choice_text,
                is_correct=choice.is_correct,
                question_id=db_question.id
            )
            db.add(db_choice)
    db.commit()