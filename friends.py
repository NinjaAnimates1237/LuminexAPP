from fastapi import APIRouter, Form
from sqlalchemy.orm import Session
from database import SessionLocal
from models import FriendRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send_friend_request")
async def send_friend_request(from_user_id: int = Form(...), to_user_id: int = Form(...), db: Session = next(get_db())):
    request = FriendRequest(from_user_id=from_user_id, to_user_id=to_user_id)
    db.add(request)
    db.commit()
    return {"status": "Request sent"}

@router.post("/accept_friend_request")
async def accept_friend_request(request_id: int = Form(...), db: Session = next(get_db())):
    request = db.query(FriendRequest).get(request_id)
    request.accepted = True
    db.commit()
    return {"status": "Request accepted"}
