from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """用户创建Schema"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")


class UserLogin(BaseModel):
    """用户登录Schema"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class UserResponse(BaseModel):
    """用户响应Schema"""
    id: int
    username: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Token响应Schema"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token数据Schema"""
    username: str | None = None

