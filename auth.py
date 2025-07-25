from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from passlib.hash import bcrypt
from app.models import User
from app.database import get_session

router = APIRouter()

@router.post("/signup")
def signup(username: str, email: str, password: str, session: Session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.email == email)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(username=username, email=email, hashed_password=bcrypt.hash(password))
    session.add(user)
    session.commit()
    return {"message": "User created", "user_id": user.id}

@router.post("/login")
def login(email: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}
