"""
统一响应格式
"""
from typing import Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from enum import Enum


class ResponseCode(int, Enum):
    """响应状态码枚举"""
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_ERROR = 500


T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """
    统一响应格式

    Attributes:
        code: 状态码
        msg: 消息描述
        data: 实际数据
    """
    code: ResponseCode = Field(default=ResponseCode.SUCCESS, description="状态码")
    msg: str = Field(default="success", description="消息描述")
    data: Optional[T] = Field(default=None, description="实际数据")

    class Config:
        """Pydantic 配置"""
        json_encoders = {
            # 可以在这里添加自定义的 JSON 编码器
        }


class PageResponse(BaseModel, Generic[T]):
    """
    分页响应格式

    Attributes:
        total: 总记录数
        list: 数据列表
    """
    total: int = Field(default=0, description="总记录数")
    items: list[T] = Field(default_factory=list, description="数据列表", validation_alias="list", serialization_alias="list")


def success_response(data: Any = None, msg: str = "success", code: ResponseCode = ResponseCode.SUCCESS) -> Response:
    """
    创建成功响应

    Args:
        data: 实际数据
        msg: 消息描述
        code: 状态码

    Returns:
        Response 对象
    """
    return Response(code=code, msg=msg, data=data)


def error_response(msg: str, code: ResponseCode = ResponseCode.BAD_REQUEST, data: Any = None) -> Response:
    """
    创建错误响应

    Args:
        msg: 错误消息
        code: 错误码
        data: 附加数据

    Returns:
        Response 对象
    """
    return Response(code=code, msg=msg, data=data)
