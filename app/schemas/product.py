"""
商品相关的 Pydantic Schema
"""
from pydantic import BaseModel, Field, field_serializer
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ProductCreate(BaseModel):
    """商品创建 Schema"""
    name: str = Field(..., min_length=1, max_length=100, description="商品全称")
    short_name: str = Field(..., min_length=1, max_length=50, description="商品简称")
    spec: Optional[str] = Field(None, max_length=50, description="规格型号")
    barcode: Optional[str] = Field(None, max_length=64, description="条形码")
    image_url: Optional[str] = Field(None, max_length=512, description="商品图片URL")
    purchase_price: Decimal = Field(..., gt=0, description="进价")
    stock_qty: int = Field(default=0, ge=0, description="库存数量")

    class Config:
        populate_by_name = True


class ProductUpdate(BaseModel):
    """商品更新 Schema"""
    id: int = Field(..., description="商品ID")
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="商品全称")
    short_name: Optional[str] = Field(None, min_length=1, max_length=50, description="商品简称")
    spec: Optional[str] = Field(None, max_length=50, description="规格型号")
    barcode: Optional[str] = Field(None, max_length=64, description="条形码")
    image_url: Optional[str] = Field(None, max_length=512, description="商品图片URL")
    purchase_price: Optional[Decimal] = Field(None, gt=0, description="进价")
    stock_qty: Optional[int] = Field(None, ge=0, description="库存数量")

    class Config:
        populate_by_name = True


class ProductDelete(BaseModel):
    """商品删除 Schema"""
    id: int = Field(..., description="商品ID")

    class Config:
        populate_by_name = True


class ProductById(BaseModel):
    """根据ID查询商品 Schema"""
    id: int = Field(..., description="商品ID")

    class Config:
        populate_by_name = True


class ProductResponse(BaseModel):
    """商品响应 Schema"""
    id: int = Field(..., serialization_alias="id", description="商品ID")
    name: str = Field(..., serialization_alias="name", description="商品全称")
    short_name: str = Field(..., serialization_alias="shortName", description="商品简称")
    spec: Optional[str] = Field(None, serialization_alias="spec", description="规格型号")
    barcode: Optional[str] = Field(None, serialization_alias="barcode", description="条形码")
    image_url: Optional[str] = Field(None, serialization_alias="imageUrl", description="商品图片URL")
    purchase_price: Decimal = Field(..., serialization_alias="purchasePrice", description="进价")
    stock_qty: int = Field(..., serialization_alias="stockQty", description="库存数量")
    created_at: datetime = Field(..., serialization_alias="createdAt", description="创建时间")

    @field_serializer('id')
    def serialize_id(self, value: int) -> str:
        """将ID序列化为字符串"""
        return str(value)

    class Config:
        from_attributes = True
        populate_by_name = True


class ProductDetailResponse(BaseModel):
    """商品详情响应 Schema（带价格列表）"""
    id: int = Field(..., serialization_alias="id", description="商品ID")
    name: str = Field(..., serialization_alias="name", description="商品全称")
    short_name: str = Field(..., serialization_alias="shortName", description="商品简称")
    spec: Optional[str] = Field(None, serialization_alias="spec", description="规格型号")
    barcode: Optional[str] = Field(None, serialization_alias="barcode", description="条形码")
    image_url: Optional[str] = Field(None, serialization_alias="imageUrl", description="商品图片URL")
    purchase_price: Decimal = Field(..., serialization_alias="purchasePrice", description="进价")
    stock_qty: int = Field(..., serialization_alias="stockQty", description="库存数量")
    created_at: datetime = Field(..., serialization_alias="createdAt", description="创建时间")
    prices: list["ProductPriceInDetail"] = Field(default_factory=list, serialization_alias="prices", description="价格列表")

    @field_serializer('id')
    def serialize_id(self, value: int) -> str:
        """将ID序列化为字符串"""
        return str(value)

    class Config:
        from_attributes = True
        populate_by_name = True


class ProductPriceInDetail(BaseModel):
    """商品详情中的价格信息"""
    level_id: int = Field(..., serialization_alias="levelId", description="会员等级ID")
    level_name: Optional[str] = Field(None, serialization_alias="levelName", description="会员等级名称")
    sale_price: Decimal = Field(..., serialization_alias="salePrice", description="销售价格")

    @field_serializer('level_id')
    def serialize_level_id(self, value: int) -> str:
        """将等级ID序列化为字符串"""
        return str(value)

    class Config:
        from_attributes = True
        populate_by_name = True


class StockUpdate(BaseModel):
    """库存更新 Schema"""
    id: int = Field(..., description="商品ID")
    delta: int = Field(..., description="库存变化量（正数增加，负数减少）")
    reason: Optional[str] = Field(None, description="变更原因")

    class Config:
        populate_by_name = True
