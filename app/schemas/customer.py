"""
客户相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CustomerCreate(BaseModel):
    """客户创建 Schema"""
    level_id: int = Field(..., description="会员等级ID")
    name: str = Field(..., min_length=1, max_length=50, description="客户名称")
    phone: str = Field(..., min_length=1, max_length=30, description="联系电话")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    address: str = Field(..., min_length=1, description="地址")

    class Config:
        populate_by_name = True


class CustomerUpdate(BaseModel):
    """客户更新 Schema"""
    id: int = Field(..., description="客户ID")
    level_id: Optional[int] = Field(None, description="会员等级ID")
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="客户名称")
    phone: Optional[str] = Field(None, min_length=1, max_length=30, description="联系电话")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    address: Optional[str] = Field(None, min_length=1, description="地址")

    class Config:
        populate_by_name = True


class CustomerDelete(BaseModel):
    """客户删除 Schema"""
    id: int = Field(..., description="客户ID")

    class Config:
        populate_by_name = True


class CustomerById(BaseModel):
    """根据ID查询客户 Schema"""
    id: int = Field(..., description="客户ID")

    class Config:
        populate_by_name = True


class CustomerResponse(BaseModel):
    """客户响应 Schema"""
    id: int = Field(..., alias="id", description="客户ID")
    level_id: int = Field(..., alias="levelId", description="会员等级ID")
    level_name: Optional[str] = Field(None, alias="levelName", description="会员等级名称")
    name: str = Field(..., alias="name", description="客户名称")
    phone: str = Field(..., alias="phone", description="联系电话")
    contact_person: Optional[str] = Field(None, alias="contactPerson", description="联系人")
    address: str = Field(..., alias="address", description="地址")
    created_at: datetime = Field(..., alias="createdAt", description="创建时间")

    class Config:
        from_attributes = True
        populate_by_name = True


class CustomerListResponse(BaseModel):
    """客户列表响应 Schema（带等级名称）"""
    id: int = Field(..., alias="id", description="客户ID")
    level_id: int = Field(..., alias="levelId", description="会员等级ID")
    level_name: Optional[str] = Field(None, alias="levelName", description="会员等级名称")
    name: str = Field(..., alias="name", description="客户名称")
    phone: str = Field(..., alias="phone", description="联系电话")
    contact_person: Optional[str] = Field(None, alias="contactPerson", description="联系人")
    address: str = Field(..., alias="address", description="地址")
    created_at: datetime = Field(..., alias="createdAt", description="创建时间")

    class Config:
        from_attributes = True
        populate_by_name = True
