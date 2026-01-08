from sqlalchemy import Column, String, Numeric, Integer, Text
from app.models.base import BaseEntity


class Product(BaseEntity):
    """商品模型"""

    __tablename__ = "products"

    name = Column(String(100), nullable=False, comment="商品全称")
    short_name = Column(String(50), nullable=False, comment="商品简称")
    spec = Column(String(50), nullable=True, comment="规格型号")
    barcode = Column(String(64), unique=True, nullable=True, comment="条形码")
    image_url = Column(String(512), nullable=True, comment="商品图片URL")
    purchase_price = Column(Numeric(12, 2), nullable=False, comment="进价")
    stock_qty = Column(Integer, default=0, nullable=False, comment="库存数量")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', barcode='{self.barcode}')>"
