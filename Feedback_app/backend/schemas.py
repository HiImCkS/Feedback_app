from pydantic import BaseModel, EmailStr
from typing import List, Optional, Union

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Login(BaseModel):
    email: EmailStr
    password: str

class QuestionCreate(BaseModel):
    question_text: str
    question_type: str
    options: Optional[str] = ""

class FormCreate(BaseModel):
    title: str
    questions: List[QuestionCreate]

class Answer(BaseModel):
    question_id: int
    answer: str

class ResponseCreate(BaseModel):
    answers: List[Answer]
