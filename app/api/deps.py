"""
API 依赖注入
"""
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import TypeVar, Type

from app.core.database import get_db
from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.models.user import User

security = HTTPBearer()

T = TypeVar("T")


# ============ Service 依赖注入工厂 ============

def get_service(service_class: Type[T]):
    """
    通用 Service 依赖注入工厂

    Args:
        service_class: Service 类

    Returns:
        Service 实例

    使用示例:
        user_service: UserService = Depends(get_service(UserService))
    """
    def _get_service(db: Session = Depends(get_db)) -> T:
        return service_class(db)
    return _get_service


# ============ 认证相关依赖 ============

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    获取当前登录用户

    Args:
        credentials: HTTP Bearer Token
        db: 数据库会话

    Returns:
        User: 当前用户对象

    Raises:
        UnauthorizedException: Token 无效或用户不存在
    """
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException("Token中缺少用户信息")
    except Exception as e:
        raise UnauthorizedException("Token无效或已过期")

    # 查询用户
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise UnauthorizedException("用户不存在")

    return user


async def get_current_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前管理员用户

    Args:
        current_user: 当前登录用户

    Returns:
        User: 管理员用户对象

    Raises:
        ForbiddenException: 用户不是管理员
    """
    if not current_user.admin_flag:
        raise ForbiddenException("需要管理员权限")
    return current_user

