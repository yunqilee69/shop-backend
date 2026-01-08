"""
全局异常处理器
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from pydantic import ValidationError
from app.core.exceptions import AppException
from app.core.response import Response, ResponseCode
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


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


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    处理 FastAPI HTTPException

    Args:
        request: 请求对象
        exc: 异常对象

    Returns:
        JSONResponse
    """
    logger.warning(f"HTTPException: {exc.status_code} - {exc.detail}", exc_info=False)

    return JSONResponse(
        status_code=exc.status_code,
        content=Response(
            code=exc.status_code,
            msg=exc.detail,
            data=None
        ).model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    处理请求参数验证错误

    Args:
        request: 请求对象
        exc: 异常对象

    Returns:
        JSONResponse
    """
    logger.warning(f"ValidationError: {exc.errors()}", exc_info=False)

    # 格式化错误信息
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append(f"{field}: {error['msg']}")

    error_msg = "参数验证失败: " + "; ".join(errors)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=Response(
            code=ResponseCode.BAD_REQUEST,
            msg=error_msg,
            data=exc.errors() if settings.DEBUG else None
        ).model_dump()
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
    error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    if "UniqueViolation" in error_msg or "duplicate key" in error_msg:
        msg = "数据重复，请检查唯一性约束"
    elif "ForeignKeyViolation" in error_msg:
        msg = "关联数据不存在"
    elif "NOT NULL" in error_msg:
        msg = "必填字段不能为空"
    else:
        msg = "数据完整性错误"

    # 开发模式下返回详细错误信息
    if settings.DEBUG:
        msg = f"{msg} ({error_msg})"

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=Response(code=ResponseCode.CONFLICT, msg=msg, data=None).model_dump()
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    处理其他数据库错误

    Args:
        request: 请求对象
        exc: 异常对象

    Returns:
        JSONResponse
    """
    logger.error(f"SQLAlchemyError: {str(exc)}", exc_info=True)

    msg = "数据库操作失败"
    if settings.DEBUG:
        msg = f"{msg}: {str(exc)}"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Response(code=ResponseCode.INTERNAL_ERROR, msg=msg, data=None).model_dump()
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
    logger.error(f"Unhandled Exception: {type(exc).__name__} - {str(exc)}", exc_info=True)

    # 生产环境下隐藏详细错误信息
    msg = "服务器内部错误" if not settings.DEBUG else f"{type(exc).__name__}: {str(exc)}"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Response(
            code=ResponseCode.INTERNAL_ERROR,
            msg=msg,
            data={"traceback": str(exc)} if settings.DEBUG else None
        ).model_dump()
    )
