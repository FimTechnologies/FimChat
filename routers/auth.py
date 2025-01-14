from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import User
from app.schemas import UserRead, UserLogin, UserCreate

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, db: Session = Depends(get_db)):

    stmt = select(User).where(User.username == user_data.username)
    existing_user = db.execute(stmt).scalar()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(
        username=user_data.username,
        password_hash = get_password_hash(user_data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):

    stmt = select(User).where(User.username == user_data.username)
    user = db.execute(stmt).scalar()

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    payload = {
        "sub": user.username,
        "exp": datetime.now() + timedelta(hours=6)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }