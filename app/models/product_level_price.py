from sqlalchemy import Column, BigInteger, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import BaseEntity


class ProductLevelPrice(BaseEntity):
    """商品等级价格模型"""

    __tablename__ = "product_level_prices"

    product_id = Column(BigInteger, ForeignKey("products.id"), nullable=False, comment="商品ID")
    level_id = Column(BigInteger, ForeignKey("customer_levels.id"), nullable=False, comment="会员等级ID")
    sale_price = Column(Numeric(12, 2), nullable=False, comment="销售价格")

    # 唯一约束：同一商品同一等级只能有一个价格
    __table_args__ = (
        UniqueConstraint('product_id', 'level_id', name='unique_product_level'),
    )

    # 关联关系
    product = relationship("Product", backref="prices")
    level = relationship("CustomerLevel", backref="product_prices")

    def __repr__(self):
        return f"<ProductLevelPrice(id={self.id}, product_id={self.product_id}, level_id={self.level_id}, sale_price={self.sale_price})>"
