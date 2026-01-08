"""
全局异常处理器
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.exceptions import AppException
from app.core.response import Response
import logging

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    处理应用自定义异常

    Args:
        request: 请求对象
        exc: 异常对象

    Returns:
        JSONResponse
    """
    logger.error(f"AppException: {exc.msg}", exc_info=True)
    return JSONResponse(
        status_code=exc.code,
        content=Response(code=exc.code, msg=exc.msg, data=exc.data).model_dump()
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """
    处理数据库完整性错误

    Args:
        request: 请求对象
        exc: 异常对象

    Returns:
        JSONResponse
    """
    logger.error(f"IntegrityError: {str(exc)}", exc_info=True)

    # 解析错误消息
    error_msg = str(exc.orig)
    if "UniqueViolation" in error_msg or "duplicate key" in error_msg:
        msg = "数据重复，请检查唯一性约束"
    elif "ForeignKeyViolation" in error_msg:
        msg = "关联数据不存在"
    else:
        msg = "数据完整性错误"

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=Response(code=409, msg=msg, data=None).model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    处理所有未捕获的异常

    Args:
        request: 请求对象
        exc: 异常对象

    Returns:
        JSONResponse
    """
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Response(code=500, msg="服务器内部错误", data=None).model_dump()
    )
