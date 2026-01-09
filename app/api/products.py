"""
商品管理 API
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.response import Response, success_response, PageResponse
from app.core.snowflake import generate_snowflake_id
from app.core.exceptions import ConflictException, NotFoundException, BadRequestException
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    ProductById,
    ProductResponse,
    ProductDetailResponse,
    StockUpdate,
    ProductPriceInDetail,
)
from app.models.product import Product
from app.models.product_level_price import ProductLevelPrice
from app.models.customer_level import CustomerLevel
from app.api.deps import get_current_user, get_current_admin
from decimal import Decimal

router = APIRouter(prefix="/products", tags=["商品管理"])


@router.post("/create", summary="创建商品")
async def create_product(
    product_create: ProductCreate,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response[ProductResponse]:
    """
    创建新的商品（仅管理员可用）

    - **name**: 商品全称（必填，1-100字符）
    - **short_name**: 商品简称（必填，1-50字符）
    - **spec**: 规格型号（选填，1-50字符）
    - **barcode**: 条形码（选填，1-64字符，唯一）
    - **image_url**: 商品图片URL（选填，1-512字符）
    - **purchase_price**: 进价（必填，必须大于0）
    - **stock_qty**: 库存数量（选填，默认0）
    """
    # 检查条形码是否已存在
    if product_create.barcode:
        existing_product = db.query(Product).filter(
            Product.barcode == product_create.barcode
        ).first()
        if existing_product:
            raise ConflictException("条形码已存在")

    # 创建新商品
    new_product = Product(
        id=generate_snowflake_id(),
        name=product_create.name,
        short_name=product_create.short_name,
        spec=product_create.spec,
        barcode=product_create.barcode,
        image_url=product_create.image_url,
        purchase_price=product_create.purchase_price,
        stock_qty=product_create.stock_qty,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # 转换为响应格式
    product_response = ProductResponse.model_validate(new_product)

    return success_response(data=product_response, msg="商品创建成功")


@router.get("/page", summary="分页查询商品列表")
async def get_products_page(
    page_index: int = Query(1, ge=1, alias="pageIndex", description="页码"),
    page_size: int = Query(20, ge=1, le=100, alias="pageSize", description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词（商品名称、简称或条形码）"),
    in_stock: Optional[bool] = Query(None, alias="inStock", description="是否有库存"),
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[PageResponse[ProductResponse]]:
    """
    分页查询商品列表（所有用户可用）

    支持分页、搜索和筛选
    """
    # 构建查询
    query = db.query(Product)

    # 搜索条件
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Product.name.like(search_pattern))
            | (Product.short_name.like(search_pattern))
            | (Product.barcode.like(search_pattern))
        )

    # 库存筛选
    if in_stock is not None:
        if in_stock:
            query = query.filter(Product.stock_qty > 0)
        else:
            query = query.filter(Product.stock_qty == 0)

    # 计算总数
    total = query.count()

    # 分页
    offset = (page_index - 1) * page_size
    products = query.order_by(Product.created_at.desc()).offset(offset).limit(page_size).all()

    # 转换为响应格式
    items = [ProductResponse.model_validate(product) for product in products]

    page_response = PageResponse[ProductResponse](
        total=total,
        items=items
    )

    return success_response(data=page_response)


@router.post("/detail", summary="查询商品详情")
async def get_product(
    product_query: ProductById,
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[ProductDetailResponse]:
    """
    查询单个商品详情（所有用户可用）

    返回商品基本信息和所有等级的价格列表
    """
    product = db.query(Product).filter(Product.id == product_query.id).first()
    if not product:
        raise NotFoundException("商品不存在")

    # 查询所有等级的价格
    prices = db.query(ProductLevelPrice).filter(
        ProductLevelPrice.product_id == product_query.id
    ).all()

    # 构建价格列表
    price_items = []
    for price in prices:
        price_item = ProductPriceInDetail(
            level_id=price.level_id,
            level_name=price.level.level_name if price.level else None,
            sale_price=price.sale_price,
        )
        price_items.append(price_item)

    # 构建响应
    product_detail = ProductDetailResponse(
        id=product.id,
        name=product.name,
        short_name=product.short_name,
        spec=product.spec,
        barcode=product.barcode,
        image_url=product.image_url,
        purchase_price=product.purchase_price,
        stock_qty=product.stock_qty,
        created_at=product.created_at,
        prices=price_items,
    )

    return success_response(data=product_detail)


@router.post("/update", summary="更新商品信息")
async def update_product(
    product_update: ProductUpdate,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response[ProductResponse]:
    """
    修改商品信息（仅管理员可用）

    所有字段都是选填的，只更新提供的字段
    """
    product = db.query(Product).filter(Product.id == product_update.id).first()
    if not product:
        raise NotFoundException("商品不存在")

    # 检查条形码是否与其他商品重复
    if product_update.barcode:
        existing_product = db.query(Product).filter(
            Product.barcode == product_update.barcode,
            Product.id != product_update.id
        ).first()
        if existing_product:
            raise ConflictException("条形码已存在")

    # 更新字段
    update_data = product_update.model_dump(exclude_unset=True, exclude={"id"})
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    # 转换为响应格式
    product_response = ProductResponse.model_validate(product)

    return success_response(data=product_response, msg="商品信息更新成功")


@router.post("/delete", summary="删除商品")
async def delete_product(
    product_delete: ProductDelete,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response:
    """
    删除商品（仅管理员可用）

    如果商品下有关联的价格，需要先删除价格才能删除商品
    """
    product = db.query(Product).filter(Product.id == product_delete.id).first()
    if not product:
        raise NotFoundException("商品不存在")

    # 检查是否有关联的价格
    price_count = db.query(ProductLevelPrice).filter(
        ProductLevelPrice.product_id == product_delete.id
    ).count()
    if price_count > 0:
        raise BadRequestException("该商品有价格设置，请先删除价格")

    db.delete(product)
    db.commit()

    return success_response(data={"message": "商品删除成功"})


@router.post("/stock", summary="更新库存")
async def update_stock(
    stock_update: StockUpdate,
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response:
    """
    调整商品库存数量（所有用户可用）

    - **id**: 商品ID（必填）
    - **delta**: 库存变化量（正数增加，负数减少）
    - **reason**: 变更原因（选填）
    """
    product = db.query(Product).filter(Product.id == stock_update.id).first()
    if not product:
        raise NotFoundException("商品不存在")

    # 计算新库存
    new_stock = product.stock_qty + stock_update.delta
    if new_stock < 0:
        raise BadRequestException("库存不足")

    # 更新库存
    product.stock_qty = new_stock
    db.commit()
    db.refresh(product)

    # 转换为响应格式
    product_response = ProductResponse.model_validate(product)

    return success_response(
        data=product_response.model_dump(),
        msg="库存更新成功"
    )
