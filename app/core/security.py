"""
安全相关功能：密码加密、JWT Token 生成和验证
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException

settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码和哈希密码是否匹配

    Args:
        plain_password: 明文密码
        hashed_password: 哈希密码

    Returns:
        bool: 是否匹配
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )


def get_password_hash(password: str) -> str:
    """
    将明文密码加密为哈希密码

    Args:
        password: 明文密码

    Returns:
        str: 哈希密码
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建 JWT Token

    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量

    Returns:
        str: JWT Token
    """
    to_encode = data.copy()

    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # 生成 Token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    解析 JWT Token

    Args:
        token: JWT Token

    Returns:
        dict: 解码后的数据

    Raises:
        UnauthorizedException: Token 无效或过期
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise UnauthorizedException("Token无效或已过期")


def get_user_id_from_token(token: str) -> int:
    """
    从 Token 中获取用户 ID

    Args:
        token: JWT Token

    Returns:
        int: 用户 ID
    """
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise UnauthorizedException("Token中缺少用户信息")
    return int(user_id)
