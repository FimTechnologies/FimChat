from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.models import User
from app.repositories.user import UserRepository
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def register_user(self, username: str, password: str) -> User:
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            raise ValueError("Username already registered")

        password_hash = self.get_password_hash(password)
        return self.user_repository.create(username, password_hash)

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_by_username(username)
        if not user or not self.verify_password(password, user.password_hash):
            raise ValueError("Incorrect username or password")

        payload = {
            "sub": user.username,
            "exp": datetime.utcnow() + timedelta(hours=6)
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username
        }
