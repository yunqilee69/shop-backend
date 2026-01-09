"""
会员等级管理 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import Response, success_response, PageResponse
from app.core.snowflake import generate_snowflake_id
from app.core.exceptions import ConflictException, NotFoundException, BadRequestException
from app.schemas.customer_level import (
    CustomerLevelCreate,
    CustomerLevelUpdate,
    CustomerLevelDelete,
    CustomerLevelById,
    CustomerLevelResponse,
)
from app.models.customer_level import CustomerLevel
from app.models.customer import Customer
from app.models.product_level_price import ProductLevelPrice
from app.api.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/customer-levels", tags=["会员等级管理"])


@router.post("/create", summary="创建会员等级")
async def create_customer_level(
    level_create: CustomerLevelCreate,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response[CustomerLevelResponse]:
    """
    创建新的会员等级（仅管理员可用）

    - **level_name**: 等级名称（必填，1-30字符，唯一）
    """
    # 检查等级名称是否已存在
    existing_level = db.query(CustomerLevel).filter(
        CustomerLevel.level_name == level_create.level_name
    ).first()
    if existing_level:
        raise ConflictException("等级名称已存在")

    # 创建新等级
    new_level = CustomerLevel(
        id=generate_snowflake_id(),
        level_name=level_create.level_name,
    )
    db.add(new_level)
    db.commit()
    db.refresh(new_level)

    # 转换为响应格式
    level_response = CustomerLevelResponse.model_validate(new_level)

    return success_response(data=level_response, msg="等级创建成功")


@router.get("/list", summary="查询等级列表")
async def get_customer_levels(
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    """
    查询所有会员等级列表（所有用户可用）
    """
    levels = db.query(CustomerLevel).all()

    # 转换为响应格式
    level_list = [CustomerLevelResponse.model_validate(level) for level in levels]

    page_response = PageResponse[CustomerLevelResponse](
        items=level_list
    )
    return success_response(data=page_response)


@router.post("/detail", summary="查询等级详情")
async def get_customer_level(
    level_query: CustomerLevelById,
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[CustomerLevelResponse]:
    """
    查询单个会员等级详情（所有用户可用）
    """
    level = db.query(CustomerLevel).filter(CustomerLevel.id == level_query.id).first()
    if not level:
        raise NotFoundException("等级不存在")

    # 转换为响应格式
    level_response = CustomerLevelResponse.model_validate(level)

    return success_response(data=level_response)


@router.post("/update", summary="更新会员等级")
async def update_customer_level(
    level_update: CustomerLevelUpdate,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response[CustomerLevelResponse]:
    """
    修改会员等级名称（仅管理员可用）

    - **id**: 等级ID（必填）
    - **level_name**: 新等级名称（必填，1-30字符）
    """
    level = db.query(CustomerLevel).filter(CustomerLevel.id == level_update.id).first()
    if not level:
        raise NotFoundException("等级不存在")

    # 检查新名称是否与其他等级重复
    existing_level = db.query(CustomerLevel).filter(
        CustomerLevel.level_name == level_update.level_name,
        CustomerLevel.id != level_update.id
    ).first()
    if existing_level:
        raise ConflictException("等级名称已存在")

    # 更新等级
    level.level_name = level_update.level_name
    db.commit()
    db.refresh(level)

    # 转换为响应格式
    level_response = CustomerLevelResponse.model_validate(level)

    return success_response(data=level_response, msg="等级更新成功")


@router.post("/delete", summary="删除会员等级")
async def delete_customer_level(
    level_delete: CustomerLevelDelete,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response:
    """
    删除会员等级（仅管理员可用）

    如果等级下有关联的客户或价格，不能删除

    - **id**: 等级ID（必填）
    """
    level = db.query(CustomerLevel).filter(CustomerLevel.id == level_delete.id).first()
    if not level:
        raise NotFoundException("等级不存在")

    # 检查是否有关联的客户
    customer_count = db.query(Customer).filter(Customer.level_id == level_delete.id).count()
    if customer_count > 0:
        raise BadRequestException("该等级下有客户，无法删除")

    # 检查是否有关联的价格
    price_count = db.query(ProductLevelPrice).filter(ProductLevelPrice.level_id == level_delete.id).count()
    if price_count > 0:
        raise BadRequestException("该等级下有价格设置，无法删除")

    # 删除等级
    db.delete(level)
    db.commit()

    return success_response(data={"message": "等级删除成功"})
