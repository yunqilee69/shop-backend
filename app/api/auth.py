"""
认证相关 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.snowflake import generate_snowflake_id
from app.core.response import Response, success_response
from app.schemas.user import UserCreate, UserLogin, ChangePassword, UserResponse, TokenResponse
from app.models.user import User
from app.api.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", summary="用户注册")
async def register(
    user_create: UserCreate,
    db: Session = Depends(get_db),
) -> Response[UserResponse]:
    """
    用户注册（仅管理员可用）

    - **username**: 登录用户名（必填，3-50字符，唯一）
    - **name**: 真实姓名（必填，1-50字符）
    - **password**: 密码（必填，6-255字符）
    - **admin_flag**: 是否管理员（默认 false）
    - **phone**: 联系电话（选填）
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_create.username).first()
    if existing_user:
        return Response(code=400, msg="用户名已存在", data=None)

    # 创建新用户
    new_user = User(
        id=generate_snowflake_id(),
        username=user_create.username,
        name=user_create.name,
        password=get_password_hash(user_create.password),
        admin_flag=user_create.admin_flag,
        phone=user_create.phone,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 返回用户信息
    user_response = UserResponse(
        id=new_user.id,
        username=new_user.username,
        name=new_user.name,
        admin_flag=new_user.admin_flag,
        phone=new_user.phone,
    )

    return success_response(data=user_response, msg="用户创建成功")


@router.post("/login", summary="用户登录")
async def login(
    user_login: UserLogin,
    db: Session = Depends(get_db),
) -> Response[TokenResponse]:
    """
    用户登录

    - **username**: 登录用户名
    - **password**: 密码

    返回 JWT Token 和用户信息
    """
    # 查询用户
    user = db.query(User).filter(User.username == user_login.username).first()
    if not user:
        return Response(code=401, msg="用户名或密码错误", data=None)

    # 验证密码
    if not verify_password(user_login.password, user.password):
        return Response(code=401, msg="用户名或密码错误", data=None)

    # 生成 Token
    access_token = create_access_token(data={"sub": str(user.id)})

    # 构建响应
    user_response = UserResponse(
        id=user.id,
        username=user.username,
        name=user.name,
        admin_flag=user.admin_flag,
        phone=user.phone,
    )

    token_response = TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response,
    )

    return success_response(data=token_response)


@router.post("/change-password", summary="修改密码")
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    """
    修改当前用户密码

    - **old_password**: 旧密码
    - **new_password**: 新密码（至少6字符）
    """
    # 验证旧密码
    if not verify_password(password_data.old_password, current_user.password):
        return Response(code=401, msg="旧密码错误", data=None)

    # 更新密码
    current_user.password = get_password_hash(password_data.new_password)
    db.commit()

    return success_response(data={"message": "密码修改成功"})
