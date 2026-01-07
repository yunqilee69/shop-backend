# Service 依赖注入使用指南

## 概述

本项目使用 FastAPI 的依赖注入系统来管理 Service 层，避免在每个接口中重复创建 Service 实例。

## 添加新 Service 的步骤

### 1. 在 `app/api/deps.py` 中添加预定义依赖

```python
# 在 deps.py 中添加
get_product_service = get_service(ProductService)
get_order_service = get_service(OrderService)
```

### 2. 在 API 路由中使用

#### 方式一：使用预定义依赖（推荐）

```python
from app.api.deps import get_product_service, get_current_active_user
from app.service.product_service import ProductService

@router.get("/products")
async def list_products(
    product_service: ProductService = Depends(get_product_service),
    current_user: UserResponse = Depends(get_current_active_user),
):
    return product_service.list_all()
```

#### 方式二：直接使用工厂函数

```python
from app.api.deps import get_service
from app.service.product_service import ProductService

@router.get("/products")
async def list_products(
    product_service: ProductService = Depends(get_service(ProductService)),
):
    return product_service.list_all()
```

## 完整示例

### 1. 定义 Product Service

```python
# app/service/product_service.py
from sqlalchemy.orm import Session
from app.dao.product_dao import ProductDAO
from app.schemas.product import ProductResponse

class ProductService:
    def __init__(self, db: Session):
        self.db = db
        self.product_dao = ProductDAO(db)

    def list_all(self):
        return self.product_dao.list_all()

    def get_by_id(self, product_id: int):
        return self.product_dao.get_by_id(product_id)
```

### 2. 在 deps.py 中注册

```python
# app/api/deps.py
from app.service.product_service import ProductService

get_product_service = get_service(ProductService)
```

### 3. 创建 Product API

```python
# app/api/product.py
from fastapi import APIRouter, Depends
from app.service.product_service import ProductService
from app.api.deps import get_product_service
from app.schemas.product import ProductResponse

router = APIRouter(prefix="/products", tags=["商品管理"])

@router.get("/", response_model=list[ProductResponse])
async def list_products(
    product_service: ProductService = Depends(get_product_service),
):
    """获取商品列表"""
    return product_service.list_all()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends(get_product_service),
):
    """获取商品详情"""
    return product_service.get_by_id(product_id)
```

## 优势

1. **代码复用**：Service 实例自动创建和注入
2. **类型安全**：IDE 可以提供完整的类型提示
3. **易于测试**：可以轻松替换为 Mock 对象
4. **统一管理**：所有 Service 依赖集中在 deps.py 中

## 最佳实践

1. **常用 Service**：在 `deps.py` 中预定义（如 UserService）
2. **不常用 Service**：使用 `get_service(XXXService)` 直接注入
3. **认证相关**：使用 `get_current_user` 或 `get_current_active_user`
4. **无需认证**：只注入 Service，不注入用户信息

## 示例对比

### ❌ 不推荐：手动创建 Service

```python
@router.get("/products")
async def list_products(db: Session = Depends(get_db)):
    product_service = ProductService(db)  # 每个接口都要写
    return product_service.list_all()
```

### ✅ 推荐：使用依赖注入

```python
@router.get("/products")
async def list_products(
    product_service: ProductService = Depends(get_product_service)
):
    return product_service.list_all()  # 简洁清晰
```
