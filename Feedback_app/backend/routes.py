from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import database, models, schemas, auth
import json

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    payload = auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    return user

@router.post("/register", response_model=schemas.Token)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    new_user = models.User(email=user.email, hashed_password=auth.hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"access_token": auth.create_token({"sub": user.email})}

@router.post("/token", response_model=schemas.Token)
def login(login: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == login.email).first()
    if not user or not auth.verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": auth.create_token({"sub": user.email})}

@router.post("/forms")
def create_form(form: schemas.FormCreate, db_user=Depends(get_db_user), db: Session = Depends(database.get_db)):
    f = models.Form(title=form.title, owner_id=db_user.id)
    db.add(f)
    db.commit()
    for q in form.questions:
        db.add(models.Question(form_id=f.id, question_text=q.question_text, question_type=q.question_type, options=q.options))
    db.commit()
    return {"message": "Form created", "form_id": f.id}

@router.get("/forms/{form_id}")
def get_form(form_id: int, db: Session = Depends(database.get_db)):
    form = db.query(models.Form).filter(models.Form.id == form_id).first()
    questions = db.query(models.Question).filter(models.Question.form_id == form_id).all()
    return {
        "form_id": form.id,
        "title": form.title,
        "questions": [
            {
                "id": q.id,
                "text": q.question_text,
                "type": q.question_type,
                "options": q.options.split(",") if q.options else []
            } for q in questions
        ]
    }

@router.post("/forms/{form_id}/submit")
def submit_response(form_id: int, response: schemas.ResponseCreate, db: Session = Depends(database.get_db)):
    db.add(models.Response(form_id=form_id, answers_json=json.dumps([a.dict() for a in response.answers])))
    db.commit()
    return {"message": "Response submitted"}

@router.get("/forms/{form_id}/responses")
def view_responses(form_id: int, db_user=Depends(get_db_user), db: Session = Depends(database.get_db)):
    form = db.query(models.Form).filter(models.Form.id == form_id, models.Form.owner_id == db_user.id).first()
    if not form:
        raise HTTPException(status_code=403, detail="Unauthorized")
    responses = db.query(models.Response).filter(models.Response.form_id == form_id).all()
    return [json.loads(r.answers_json) for r in responses]
