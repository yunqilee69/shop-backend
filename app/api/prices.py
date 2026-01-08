"""
价格管理 API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.response import Response, success_response
from app.core.snowflake import generate_snowflake_id
from app.core.exceptions import NotFoundException, BadRequestException
from app.schemas.price import (
    PriceCreate,
    PriceDelete,
    PriceByProduct,
    PriceItem,
    BatchPriceCreate,
    PriceResponse,
    BatchPriceResponse,
    ProductPriceListResponse,
    PriceItemResponse,
)
from app.models.product_level_price import ProductLevelPrice
from app.models.product import Product
from app.models.customer_level import CustomerLevel
from app.api.deps import get_current_user, get_current_admin
from decimal import Decimal

router = APIRouter(prefix="/prices", tags=["价格管理"])


@router.post("/set", summary="设置商品等级价格")
async def set_price(
    price_create: PriceCreate,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response[PriceResponse]:
    """
    为指定商品设置某个等级的销售价格（仅管理员可用）

    - **product_id**: 商品ID（必填）
    - **level_id**: 会员等级ID（必填）
    - **sale_price**: 销售价格（必填，必须大于0）

    如果价格已存在，则更新；否则创建新价格
    """
    # 验证商品是否存在
    product = db.query(Product).filter(Product.id == price_create.product_id).first()
    if not product:
        raise NotFoundException("商品不存在")

    # 验证等级是否存在
    level = db.query(CustomerLevel).filter(CustomerLevel.id == price_create.level_id).first()
    if not level:
        raise NotFoundException("会员等级不存在")

    # 查找是否已存在该商品该等级的价格
    existing_price = db.query(ProductLevelPrice).filter(
        ProductLevelPrice.product_id == price_create.product_id,
        ProductLevelPrice.level_id == price_create.level_id
    ).first()

    if existing_price:
        # 更新现有价格
        existing_price.sale_price = price_create.sale_price
        db.commit()
        db.refresh(existing_price)
        price_response = PriceResponse.model_validate(existing_price)
        return success_response(data=price_response, msg="价格更新成功")
    else:
        # 创建新价格
        new_price = ProductLevelPrice(
            id=generate_snowflake_id(),
            product_id=price_create.product_id,
            level_id=price_create.level_id,
            sale_price=price_create.sale_price,
        )
        db.add(new_price)
        db.commit()
        db.refresh(new_price)
        price_response = PriceResponse.model_validate(new_price)
        return success_response(data=price_response, msg="价格设置成功")


@router.post("/batch", summary="批量设置商品价格")
async def set_batch_prices(
    batch_price: BatchPriceCreate,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response[BatchPriceResponse]:
    """
    为商品批量设置所有等级的价格（仅管理员可用）

    - **product_id**: 商品ID（必填）
    - **prices**: 价格列表，每个包含 level_id 和 sale_price

    返回创建和更新的数量
    """
    # 验证商品是否存在
    product = db.query(Product).filter(Product.id == batch_price.product_id).first()
    if not product:
        raise NotFoundException("商品不存在")

    # 验证所有等级是否存在
    level_ids = [p.level_id for p in batch_price.prices]
    levels = db.query(CustomerLevel).filter(CustomerLevel.id.in_(level_ids)).all()
    level_id_set = {level.id for level in levels}

    if len(level_id_set) != len(level_ids):
        raise NotFoundException("部分会员等级不存在")

    # 批量设置价格
    created_count = 0
    updated_count = 0

    for price_item in batch_price.prices:
        # 查找是否已存在
        existing_price = db.query(ProductLevelPrice).filter(
            ProductLevelPrice.product_id == batch_price.product_id,
            ProductLevelPrice.level_id == price_item.level_id
        ).first()

        if existing_price:
            # 更新
            existing_price.sale_price = price_item.sale_price
            updated_count += 1
        else:
            # 创建
            new_price = ProductLevelPrice(
                id=generate_snowflake_id(),
                product_id=batch_price.product_id,
                level_id=price_item.level_id,
                sale_price=price_item.sale_price,
            )
            db.add(new_price)
            created_count += 1

    db.commit()

    batch_response = BatchPriceResponse(
        product_id=batch_price.product_id,
        created_count=created_count,
        updated_count=updated_count,
    )

    return success_response(data=batch_response, msg="批量价格设置成功")


@router.post("/product-prices", summary="查询商品价格列表")
async def get_product_prices(
    query: PriceByProduct,
    current_user: CustomerLevel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[ProductPriceListResponse]:
    """
    查询指定商品的所有等级价格（所有用户可用）

    - **product_id**: 商品ID（必填）
    """
    # 验证商品是否存在
    product = db.query(Product).filter(Product.id == query.product_id).first()
    if not product:
        raise NotFoundException("商品不存在")

    # 查询所有价格
    prices = db.query(ProductLevelPrice).filter(
        ProductLevelPrice.product_id == query.product_id
    ).all()

    # 构建价格列表
    price_items = []
    for price in prices:
        price_item = PriceItemResponse(
            id=price.id,
            level_id=price.level_id,
            level_name=price.level.level_name if price.level else None,
            sale_price=price.sale_price,
            updated_at=price.updated_at,
        )
        price_items.append(price_item)

    response = ProductPriceListResponse(
        product_id=product.id,
        product_name=product.name,
        prices=price_items,
    )

    return success_response(data=response)


@router.post("/delete", summary="删除价格")
async def delete_price(
    price_delete: PriceDelete,
    current_admin: CustomerLevel = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response:
    """
    删除指定商品的某个等级价格（仅管理员可用）

    - **id**: 价格ID（必填）
    """
    price = db.query(ProductLevelPrice).filter(ProductLevelPrice.id == price_delete.id).first()
    if not price:
        raise NotFoundException("价格不存在")

    db.delete(price)
    db.commit()

    return success_response(data={"message": "价格删除成功"})
