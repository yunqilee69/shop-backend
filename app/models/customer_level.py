from sqlalchemy import Column, String
from app.models.base import BaseEntity


class CustomerLevel(BaseEntity):
    """会员等级模型"""

    __tablename__ = "customer_levels"

    level_name = Column(String(30), unique=True, nullable=False, comment="等级名称")

    def __repr__(self):
        return f"<CustomerLevel(id={self.id}, level_name='{self.level_name}')>"
