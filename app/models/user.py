from sqlalchemy import Column, String, Boolean
from app.models.base import BaseEntity


class User(BaseEntity):
    """用户模型"""

    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True, nullable=False, comment="登录账号")
    name = Column(String(50), nullable=False, comment="用户名称")
    password = Column(String(200), nullable=False, comment="密码(加密)")
    admin_flag = Column(Boolean, default=False, nullable=False, comment="是否为管理员")
    phone = Column(String(20), nullable=True, comment="手机号")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', name='{self.name}')>"

