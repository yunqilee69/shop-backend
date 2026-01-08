from sqlalchemy import Column, String, Text, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseEntity


class Customer(BaseEntity):
    """客户模型"""

    __tablename__ = "customers"

    level_id = Column(BigInteger, ForeignKey("customer_levels.id"), nullable=False, comment="会员等级ID")
    name = Column(String(50), nullable=False, comment="客户名称")
    phone = Column(String(30), nullable=False, comment="联系电话")
    contact_person = Column(String(50), nullable=True, comment="联系人")
    address = Column(Text, nullable=False, comment="地址")

    # 关联关系
    level = relationship("CustomerLevel", backref="customers")

    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.name}', phone='{self.phone}')>"
