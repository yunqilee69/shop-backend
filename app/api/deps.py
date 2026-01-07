from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.service.user_service import UserService
from app.schemas.user import UserResponse

security = HTTPBearer()


# ============ Service 依赖注入工厂 ============

def get_service(service_class):
    """
    通用 Service 依赖注入

    使用示例:
        user_service: UserService = Depends(lambda db: get_service(db, UserService))
        或者直接用下面的预定义依赖
    """
    def _get_service(db: Session = Depends(get_db)):
        return service_class(db)
    return _get_service


# ============ 预定义的 Service 依赖 ============
# 这样在 API 中可以直接使用，不需要每次都写 Depends(get_service(...))

get_user_service = get_service(UserService)
# 后续添加其他 Service:
# get_product_service = get_service(ProductService)
# get_order_service = get_service(OrderService)


# ============ 认证相关依赖 ============

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """
    获取当前登录用户
    """
    token = credentials.credentials
    try:
        return user_service.get_current_user(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """
    获取当前激活用户
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return current_user

