from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)

class Form(Base):
    __tablename__ = "forms"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey("forms.id"))
    question_text = Column(String)
    question_type = Column(String)  # 'text' or 'mcq'
    options = Column(Text)  # comma-separated for MCQ

class Response(Base):
    __tablename__ = "responses"
    id = Column(Integer, primary_key=True)
    form_id = Column(Integer, ForeignKey("forms.id"))
    answers_json = Column(Text)  # JSON string of answers
