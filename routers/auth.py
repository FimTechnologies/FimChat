from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import UserRead, UserLogin, UserCreate
from app.repositories.user import UserRepository
from app.services.user import UserService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    user_repository = UserRepository(db)
    return UserService(user_repository)

@router.post("/register", response_model=UserRead)
def register(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        new_user = user_service.register_user(user_data.username, user_data.password)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user_data: UserLogin, user_service: UserService = Depends(get_user_service)):
    try:
        token_data = user_service.authenticate_user(user_data.username, user_data.password)
        return token_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
