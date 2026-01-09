"""
价格相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field, field_serializer
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
    id: int = Field(..., serialization_alias="id", description="价格ID")
    product_id: int = Field(..., serialization_alias="productId", description="商品ID")
    level_id: int = Field(..., serialization_alias="levelId", description="会员等级ID")
    sale_price: Decimal = Field(..., serialization_alias="salePrice", description="销售价格")
    created_at: datetime = Field(..., serialization_alias="createdAt", description="创建时间")

    @field_serializer('id', 'product_id', 'level_id')
    def serialize_ids(self, value: int) -> str:
        """将ID序列化为字符串"""
        return str(value)

    class Config:
        from_attributes = True
        populate_by_name = True


class ProductPriceListResponse(BaseModel):
    """商品价格列表响应 Schema"""
    product_id: int = Field(..., serialization_alias="productId", description="商品ID")
    product_name: str = Field(..., serialization_alias="productName", description="商品名称")
    prices: List["PriceItemResponse"] = Field(default_factory=list, serialization_alias="prices", description="价格列表")

    @field_serializer('product_id')
    def serialize_product_id(self, value: int) -> str:
        """将商品ID序列化为字符串"""
        return str(value)


class PriceItemResponse(BaseModel):
    """价格项响应 Schema"""
    id: int = Field(..., serialization_alias="id", description="价格ID")
    level_id: int = Field(..., serialization_alias="levelId", description="会员等级ID")
    level_name: Optional[str] = Field(None, serialization_alias="levelName", description="会员等级名称")
    sale_price: Decimal = Field(..., serialization_alias="salePrice", description="销售价格")
    updated_at: datetime = Field(..., serialization_alias="updatedAt", description="更新时间")

    @field_serializer('id', 'level_id')
    def serialize_ids(self, value: int) -> str:
        """将ID序列化为字符串"""
        return str(value)

    class Config:
        from_attributes = True
        populate_by_name = True


class BatchPriceResponse(BaseModel):
    """批量价格创建响应 Schema"""
    product_id: int = Field(..., serialization_alias="productId", description="商品ID")
    created_count: int = Field(..., serialization_alias="createdCount", description="创建数量")
    updated_count: int = Field(..., serialization_alias="updatedCount", description="更新数量")

    @field_serializer('product_id')
    def serialize_product_id(self, value: int) -> str:
        """将商品ID序列化为字符串"""
        return str(value)

    class Config:
        populate_by_name = True
