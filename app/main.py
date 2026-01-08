from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.config import get_settings
from app.core.response import Response
from app.core.exceptions import AppException
from app.core.handlers import (
    app_exception_handler,
    integrity_error_handler,
    general_exception_handler,
)
from app.api import auth, customer_levels, customers, products, prices

settings = get_settings()

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="超市后端管理系统API",
    debug=settings.DEBUG,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理器
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 注册路由
app.include_router(auth.router, prefix="/api/v1", tags=["认证"])
app.include_router(customer_levels.router, prefix="/api/v1", tags=["会员等级管理"])
app.include_router(customers.router, prefix="/api/v1", tags=["客户管理"])
app.include_router(products.router, prefix="/api/v1", tags=["商品管理"])
app.include_router(prices.router, prefix="/api/v1", tags=["价格管理"])


@app.get("/")
async def root():
    """
    根路径
    """
    return {
        "message": "欢迎使用超市后端管理系统",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy"}
