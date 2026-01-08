"""
会员等级相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CustomerLevelCreate(BaseModel):
    """会员等级创建 Schema"""
    level_name: str = Field(..., min_length=1, max_length=30, description="等级名称")

    class Config:
        populate_by_name = True


class CustomerLevelUpdate(BaseModel):
    """会员等级更新 Schema"""
    id: int = Field(..., description="等级ID")
    level_name: str = Field(..., min_length=1, max_length=30, description="等级名称")

    class Config:
        populate_by_name = True


class CustomerLevelDelete(BaseModel):
    """会员等级删除 Schema"""
    id: int = Field(..., description="等级ID")

    class Config:
        populate_by_name = True


class CustomerLevelById(BaseModel):
    """根据ID查询会员等级 Schema"""
    id: int = Field(..., description="等级ID")

    class Config:
        populate_by_name = True


class CustomerLevelResponse(BaseModel):
    """会员等级响应 Schema"""
    id: int = Field(..., alias="id", description="等级ID")
    level_name: str = Field(..., alias="levelName", description="等级名称")
    created_at: datetime = Field(..., alias="createdAt", description="创建时间")

    class Config:
        from_attributes = True
        populate_by_name = True
