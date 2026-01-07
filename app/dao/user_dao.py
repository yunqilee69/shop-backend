from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional

from app.models.user import User
from app.schemas.user import UserCreate


class UserDAO:
    """用户数据访问对象"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """根据用户名或邮箱获取用户"""
        return (
            self.db.query(User)
            .filter(or_(User.username == identifier, User.email == identifier))
            .first()
        )

    def create(self, user_create: UserCreate) -> User:
        """创建新用户"""
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password = pwd_context.hash(user_create.password)

        db_user = User(
            username=user_create.username,
            email=user_create.email,
            full_name=user_create.full_name,
            phone=user_create.phone,
            hashed_password=hashed_password,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user: User) -> User:
        """更新用户"""
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """删除用户"""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """获取用户列表"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """验证用户凭据"""
        from passlib.context import CryptContext

        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        user = self.get_by_username_or_email(username)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user
