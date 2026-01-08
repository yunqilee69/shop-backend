"""
客户管理 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.response import Response, success_response, PageResponse
from app.core.snowflake import generate_snowflake_id
from app.core.exceptions import NotFoundException, BadRequestException
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerDelete,
    CustomerById,
    CustomerResponse,
    CustomerListResponse,
)
from app.models.customer import Customer
from app.models.customer_level import CustomerLevel
from app.api.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/customers", tags=["客户管理"])


@router.post("/create", summary="创建客户")
async def create_customer(
    customer_create: CustomerCreate,
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[CustomerListResponse]:
    """
    创建新的客户（所有用户可用）

    - **level_id**: 会员等级ID（必填）
    - **name**: 客户名称（必填，1-50字符）
    - **phone**: 联系电话（必填，1-30字符）
    - **contact_person**: 联系人（选填，1-50字符）
    - **address**: 地址（必填）
    """
    # 验证会员等级是否存在
    level = db.query(CustomerLevel).filter(CustomerLevel.id == customer_create.level_id).first()
    if not level:
        raise NotFoundException("会员等级不存在")

    # 创建新客户
    new_customer = Customer(
        id=generate_snowflake_id(),
        level_id=customer_create.level_id,
        name=customer_create.name,
        phone=customer_create.phone,
        contact_person=customer_create.contact_person,
        address=customer_create.address,
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    # 转换为响应格式
    customer_response = CustomerListResponse(
        id=new_customer.id,
        level_id=new_customer.level_id,
        level_name=level.level_name,
        name=new_customer.name,
        phone=new_customer.phone,
        contact_person=new_customer.contact_person,
        address=new_customer.address,
        created_at=new_customer.created_at,
    )

    return success_response(data=customer_response, msg="客户创建成功")


@router.get("/list", summary="查询客户列表")
async def get_customers(
    page_index: int = Query(1, ge=1, alias="pageIndex", description="页码"),
    page_size: int = Query(20, ge=1, le=100, alias="pageSize", description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词（客户名称或手机号）"),
    level_id: Optional[int] = Query(None, alias="levelId", description="会员等级ID筛选"),
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[PageResponse[CustomerListResponse]]:
    """
    查询客户列表（所有用户可用）

    支持分页、搜索和筛选
    """
    # 构建查询
    query = db.query(Customer).join(CustomerLevel)

    # 搜索条件
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Customer.name.like(search_pattern)) | (Customer.phone.like(search_pattern))
        )

    # 等级筛选
    if level_id:
        query = query.filter(Customer.level_id == level_id)

    # 计算总数
    total = query.count()

    # 分页
    offset = (page_index - 1) * page_size
    customers = query.order_by(Customer.created_at.desc()).offset(offset).limit(page_size).all()

    # 构建响应数据
    items = []
    for customer in customers:
        customer_data = CustomerListResponse(
            id=customer.id,
            level_id=customer.level_id,
            level_name=customer.level.level_name if customer.level else None,
            name=customer.name,
            phone=customer.phone,
            contact_person=customer.contact_person,
            address=customer.address,
            created_at=customer.created_at,
        )
        items.append(customer_data)

    page_response = PageResponse[CustomerListResponse](
        total=total,
        items=items,
    )

    return success_response(data=page_response)


@router.post("/detail", summary="查询客户详情")
async def get_customer(
    customer_query: CustomerById,
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[CustomerListResponse]:
    """
    查询单个客户详情（所有用户可用）
    """
    customer = db.query(Customer).filter(Customer.id == customer_query.id).first()
    if not customer:
        raise NotFoundException("客户不存在")

    customer_response = CustomerListResponse(
        id=customer.id,
        level_id=customer.level_id,
        level_name=customer.level.level_name if customer.level else None,
        name=customer.name,
        phone=customer.phone,
        contact_person=customer.contact_person,
        address=customer.address,
        created_at=customer.created_at,
    )

    return success_response(data=customer_response)


@router.post("/update", summary="更新客户信息")
async def update_customer(
    customer_update: CustomerUpdate,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response[CustomerListResponse]:
    """
    修改客户信息（仅管理员可用）

    所有字段都是选填的，只更新提供的字段
    """
    customer = db.query(Customer).filter(Customer.id == customer_update.id).first()
    if not customer:
        raise NotFoundException("客户不存在")

    # 验证会员等级是否存在（如果提供了 level_id）
    if customer_update.level_id:
        level = db.query(CustomerLevel).filter(
            CustomerLevel.id == customer_update.level_id
        ).first()
        if not level:
            raise NotFoundException("会员等级不存在")

    # 更新字段
    update_data = customer_update.model_dump(exclude_unset=True, exclude={"id"})
    for field, value in update_data.items():
        setattr(customer, field, value)

    db.commit()
    db.refresh(customer)

    customer_response = CustomerListResponse(
        id=customer.id,
        level_id=customer.level_id,
        level_name=customer.level.level_name if customer.level else None,
        name=customer.name,
        phone=customer.phone,
        contact_person=customer.contact_person,
        address=customer.address,
        created_at=customer.created_at,
    )

    return success_response(data=customer_response, msg="客户信息更新成功")


@router.post("/delete", summary="删除客户")
async def delete_customer(
    customer_delete: CustomerDelete,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response:
    """
    删除客户（仅管理员可用）
    """
    customer = db.query(Customer).filter(Customer.id == customer_delete.id).first()
    if not customer:
        raise NotFoundException("客户不存在")

    db.delete(customer)
    db.commit()

    return success_response(data={"message": "客户删除成功"})
