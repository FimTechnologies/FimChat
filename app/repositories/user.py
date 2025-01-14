from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        return self.db.execute(stmt).scalar()

    def create(self, username: str, password_hash: str) -> User:
        new_user = User(username=username, password_hash=password_hash)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user
