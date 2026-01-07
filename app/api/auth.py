from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.service.user_service import UserService
from app.api.deps import get_user_service, get_current_active_user

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    """
    用户注册

    - **username**: 用户名(3-50字符)
    - **email**: 邮箱地址
    - **password**: 密码(至少6字符)
    - **full_name**: 全名(可选)
    - **phone**: 电话号码(可选)
    """
    try:
        return user_service.register(user_create)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(
    user_login: UserLogin,
    user_service: UserService = Depends(get_user_service),
):
    """
    用户登录

    - **username**: 用户名
    - **password**: 密码

    返回JWT访问令牌
    """
    try:
        return user_service.login(user_login)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserResponse = Depends(get_current_active_user),
):
    """
    获取当前登录用户信息

    需要在请求头中携带: Authorization: Bearer <token>
    """
    return current_user
