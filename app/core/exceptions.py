"""
自定义异常类
"""
from typing import Any, Optional
from app.core.response import ResponseCode


class AppException(Exception):
    """应用基础异常类"""

    def __init__(
        self,
        msg: str,
        code: ResponseCode = ResponseCode.BAD_REQUEST,
        data: Any = None
    ):
        """
        初始化异常

        Args:
            msg: 错误消息
            code: 错误码
            data: 附加数据
        """
        self.msg = msg
        self.code = code
        self.data = data
        super().__init__(msg)


class BadRequestException(AppException):
    """错误请求异常 (400)"""

    def __init__(self, msg: str, data: Any = None):
        super().__init__(msg, ResponseCode.BAD_REQUEST, data)


class UnauthorizedException(AppException):
    """未授权异常 (401)"""

    def __init__(self, msg: str = "未认证或Token失效", data: Any = None):
        super().__init__(msg, ResponseCode.UNAUTHORIZED, data)


class ForbiddenException(AppException):
    """权限不足异常 (403)"""

    def __init__(self, msg: str = "权限不足", data: Any = None):
        super().__init__(msg, ResponseCode.FORBIDDEN, data)


class NotFoundException(AppException):
    """资源不存在异常 (404)"""

    def __init__(self, msg: str = "资源不存在", data: Any = None):
        super().__init__(msg, ResponseCode.NOT_FOUND, data)


class ConflictException(AppException):
    """资源冲突异常 (409)"""

    def __init__(self, msg: str, data: Any = None):
        super().__init__(msg, ResponseCode.CONFLICT, data)


class InternalErrorException(AppException):
    """服务器内部错误异常 (500)"""

    def __init__(self, msg: str = "服务器内部错误", data: Any = None):
        super().__init__(msg, ResponseCode.INTERNAL_ERROR, data)
