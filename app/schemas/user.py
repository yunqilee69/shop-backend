"""
用户相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field
from typing import Optional


class UserCreate(BaseModel):
    """用户创建 Schema"""
    username: str = Field(..., min_length=3, max_length=50, description="登录用户名")
    name: str = Field(..., min_length=1, max_length=50, description="真实姓名")
    password: str = Field(..., min_length=6, max_length=255, description="密码")
    admin_flag: bool = Field(default=False, description="是否管理员")
    phone: Optional[str] = Field(None, max_length=30, description="联系电话")

    class Config:
        populate_by_name = True


class UserLogin(BaseModel):
    """用户登录 Schema"""
    username: str = Field(..., description="登录用户名")
    password: str = Field(..., description="密码")

    class Config:
        populate_by_name = True


class ChangePassword(BaseModel):
    """修改密码 Schema"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=6, max_length=255, description="新密码")

    class Config:
        populate_by_name = True


class UserResponse(BaseModel):
    """用户响应 Schema"""
    id: int = Field(..., alias="id", description="用户ID")
    username: str = Field(..., alias="username", description="登录用户名")
    name: str = Field(..., alias="name", description="真实姓名")
    admin_flag: bool = Field(..., alias="adminFlag", description="是否管理员")
    phone: Optional[str] = Field(None, alias="phone", description="联系电话")

    class Config:
        from_attributes = True
        populate_by_name = True


class TokenResponse(BaseModel):
    """Token 响应 Schema"""
    access_token: str = Field(..., alias="accessToken", description="访问令牌")
    token_type: str = Field(default="bearer", alias="tokenType", description="令牌类型")
    user: UserResponse = Field(..., alias="user", description="用户信息")

    class Config:
        populate_by_name = True
