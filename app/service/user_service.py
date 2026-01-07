from sqlalchemy.orm import Session
from typing import Optional
from datetime import timedelta, datetime

from app.dao.user_dao import UserDAO
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.config import get_settings
from jose import JWTError, jwt

settings = get_settings()


class UserService:
    """用户业务逻辑服务"""

    def __init__(self, db: Session):
        self.db = db
        self.user_dao = UserDAO(db)

    def register(self, user_create: UserCreate) -> UserResponse:
        """
        用户注册
        """
        # 检查用户名是否已存在
        existing_user = self.user_dao.get_by_username(user_create.username)
        if existing_user:
            raise ValueError("用户名已存在")

        # 检查邮箱是否已存在
        existing_email = self.user_dao.get_by_email(user_create.email)
        if existing_email:
            raise ValueError("邮箱已被注册")

        # 创建用户
        user = self.user_dao.create(user_create)
        return UserResponse.model_validate(user)

    def login(self, user_login: UserLogin) -> Token:
        """
        用户登录
        """
        # 验证用户凭据
        user = self.user_dao.authenticate(user_login.username, user_login.password)
        if not user:
            raise ValueError("用户名或密码错误")

        if not user.is_active:
            raise ValueError("用户账号已被禁用")

        # 生成JWT token
        access_token = self._create_access_token(data={"sub": user.username})

        return Token(access_token=access_token)

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        """
        获取用户信息
        """
        user = self.user_dao.get_by_id(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)

    def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        """
        根据用户名获取用户
        """
        user = self.user_dao.get_by_username(username)
        if not user:
            return None
        return UserResponse.model_validate(user)

    def get_current_user(self, token: str) -> UserResponse:
        """
        根据token获取当前用户
        """
        credentials_exception = ValueError("无法验证凭证")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = self.user_dao.get_by_username(username)
        if user is None:
            raise credentials_exception

        return UserResponse.model_validate(user)

    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        创建访问令牌
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
