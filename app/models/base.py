from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime
from app.core.database import Base


class BaseEntity(Base):
    """基础实体类，包含通用字段"""
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True, comment="主键ID (Snowflake ID)")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
