from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = next(get_db())):
    hashed = pwd_context.hash(password)
    user = User(username=username, email=email, hashed_password=hashed)
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=303)

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = next(get_db())):
    user = db.query(User).filter(User.username == username).first()
    if user and pwd_context.verify(password, user.hashed_password):
        # TODO: set session / cookie
        return RedirectResponse("/profile", status_code=303)
    return RedirectResponse("/login", status_code=303)
