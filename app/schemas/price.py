"""
价格相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class PriceCreate(BaseModel):
    """价格创建 Schema"""
    product_id: int = Field(..., description="商品ID")
    level_id: int = Field(..., description="会员等级ID")
    sale_price: Decimal = Field(..., gt=0, description="销售价格")

    class Config:
        populate_by_name = True


class PriceItem(BaseModel):
    """价格项"""
    level_id: int = Field(..., description="会员等级ID")
    sale_price: Decimal = Field(..., gt=0, description="销售价格")

    class Config:
        populate_by_name = True


class BatchPriceCreate(BaseModel):
    """批量价格创建 Schema"""
    product_id: int = Field(..., description="商品ID")
    prices: List[PriceItem] = Field(..., description="价格列表")

    class Config:
        populate_by_name = True


class PriceDelete(BaseModel):
    """价格删除 Schema"""
    id: int = Field(..., description="价格ID")

    class Config:
        populate_by_name = True


class PriceByProduct(BaseModel):
    """根据商品ID查询价格 Schema"""
    product_id: int = Field(..., description="商品ID")

    class Config:
        populate_by_name = True


class PriceResponse(BaseModel):
    """价格响应 Schema"""
    id: int = Field(..., alias="id", description="价格ID")
    product_id: int = Field(..., alias="productId", description="商品ID")
    level_id: int = Field(..., alias="levelId", description="会员等级ID")
    sale_price: Decimal = Field(..., alias="salePrice", description="销售价格")
    created_at: datetime = Field(..., alias="createdAt", description="创建时间")

    class Config:
        from_attributes = True
        populate_by_name = True


class ProductPriceListResponse(BaseModel):
    """商品价格列表响应 Schema"""
    product_id: int = Field(..., alias="productId", description="商品ID")
    product_name: str = Field(..., alias="productName", description="商品名称")
    prices: List["PriceItemResponse"] = Field(default_factory=list, alias="prices", description="价格列表")


class PriceItemResponse(BaseModel):
    """价格项响应 Schema"""
    id: int = Field(..., alias="id", description="价格ID")
    level_id: int = Field(..., alias="levelId", description="会员等级ID")
    level_name: Optional[str] = Field(None, alias="levelName", description="会员等级名称")
    sale_price: Decimal = Field(..., alias="salePrice", description="销售价格")
    updated_at: datetime = Field(..., alias="updatedAt", description="更新时间")

    class Config:
        from_attributes = True
        populate_by_name = True


class BatchPriceResponse(BaseModel):
    """批量价格创建响应 Schema"""
    product_id: int = Field(..., alias="productId", description="商品ID")
    created_count: int = Field(..., alias="createdCount", description="创建数量")
    updated_count: int = Field(..., alias="updatedCount", description="更新数量")

    class Config:
        populate_by_name = True
