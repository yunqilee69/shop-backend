# 项目 API 接口规范文档

## 1. 概述

本文档定义了 shop-backend 项目的 API 接口开发规范，所有接口开发必须严格遵守本规范。

## 2. 核心规范

### 2.1 HTTP 方法使用规范

项目**只允许使用 GET 和 POST** 两种 HTTP 方法：

- **GET**: 用于查询类接口，不会改变服务器数据
  - 列表查询（带分页、搜索、筛选）
  - 详情查询

- **POST**: 用于会改变服务器数据的接口
  - 新增数据
  - 更新数据
  - 删除数据
  - 修改操作（如库存调整）

**不允许使用 PUT、DELETE、PATCH 等其他 HTTP 方法**

### 2.2 路径规范

**禁止使用路径参数**，所有参数都通过以下方式传递：

- GET 请求：使用查询参数（Query Parameters）
- POST 请求：统一使用请求体（Request Body）

#### 示例：

✅ **正确做法**:
```python
# 查询详情 - GET 使用查询参数
@router.get("/detail")
async def get_detail(id: int = Query(...)): ...

# 更新数据 - POST 使用请求体
@router.post("/update")
async def update(item: ItemUpdate): ...
```

❌ **错误做法**:
```python
# 不允许使用路径参数
@router.get("/{id}")
async def get_detail(id: int): ...

@router.put("/{id}")
async def update(id: int, item: ItemUpdate): ...
```

### 2.3 命名规范

#### 2.3.1 接口层面（驼峰命名）

- **请求参数**: 使用驼峰命名（camelCase）
- **响应字段**: 使用驼峰命名（camelCase）
- **查询参数**: 使用驼峰命名（camelCase）

#### 示例：
```json
// 请求示例
{
  "productId": 123,
  "levelName": "VIP",
  "purchasePrice": 100.50,
  "stockQty": 50
}

// 响应示例
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": 123,
    "productName": "商品名称",
    "createdAt": "2024-01-01T00:00:00Z"
  }
}
```

#### 2.3.2 项目内部（蛇形命名）

- **数据库字段**: 使用蛇形命名（snake_case）
- **Python 变量**: 使用蛇形命名（snake_case）
- **Model 属性**: 使用蛇形命名（snake_case）

#### 示例：
```python
# Model 定义（蛇形命名）
class Product(Base):
    product_name: str
    purchase_price: Decimal
    stock_qty: int
    created_at: datetime

# 内部代码（蛇形命名）
product_name = "商品名称"
purchase_price = Decimal("100.50")
```

#### 2.3.3 命名转换

在 Schema 层使用 Pydantic 的 `alias` 功能实现命名转换：

```python
class ProductResponse(BaseModel):
    id: int = Field(..., alias="id")
    product_name: str = Field(..., alias="productName")
    purchase_price: Decimal = Field(..., alias="purchasePrice")

    class Config:
        from_attributes = True
        populate_by_name = True
```

## 3. 分页规范

### 3.1 分页参数

所有分页查询接口必须包含以下参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pageIndex | int | 是 | 页码，从 1 开始 |
| pageSize | int | 是 | 每页数量，通常 1-100 |

**示例**:
```
GET /api/products/list?pageIndex=1&pageSize=20
```

### 3.2 分页响应

分页响应只包含以下字段：

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| total | int | 是 | 总记录数 |
| items | array | 是 | 数据列表 |

**不返回** `pageIndex` 和 `pageSize` 字段

**示例**:
```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "total": 100,
    "items": [...]
  }
}
```

## 4. 鉴权规范

### 4.1 Token 验证

所有接口（除登录/注册外）必须进行 Token 验证：

- 使用 JWT Token
- Token 放在 HTTP Header: `Authorization: Bearer <token>`
- Token 验证失败返回 401

### 4.2 权限控制

根据接口的功能要求，使用不同的权限依赖：

#### get_current_user
- **适用**: 所有登录用户可访问的接口
- **用途**: 查询类接口、部分操作接口
- **示例**: 客户列表、商品列表、库存调整

#### get_current_admin
- **适用**: 仅管理员可访问的接口
- **用途**: 新增、修改、删除类接口
- **示例**: 创建商品、更新客户、删除价格

### 4.3 权限分配示例

```python
# 查询类 - 所有用户
@router.get("/list")
async def get_list(current_user: User = Depends(get_current_user)): ...

# 详情查询 - 所有用户
@router.post("/detail")
async def get_detail(query: Query, current_user: User = Depends(get_current_user)): ...

# 创建 - 仅管理员
@router.post("/create")
async def create(item: ItemCreate, current_admin: User = Depends(get_current_admin)): ...

# 更新 - 仅管理员
@router.post("/update")
async def update(item: ItemUpdate, current_admin: User = Depends(get_current_admin)): ...

# 删除 - 仅管理员
@router.post("/delete")
async def delete(item: ItemDelete, current_admin: User = Depends(get_current_admin)): ...
```

## 5. 统一响应格式

### 5.1 成功响应

```json
{
  "code": 200,
  "msg": "success",
  "data": { ... }
}
```

### 5.2 错误响应

```json
{
  "code": 400/401/403/404/409/500,
  "msg": "错误描述",
  "data": null
}
```

### 5.3 响应状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权（Token 无效或过期） |
| 403 | 禁止访问（权限不足） |
| 404 | 资源不存在 |
| 409 | 资源冲突（如重复创建） |
| 500 | 服务器内部错误 |

## 6. 接口路由规范

### 6.1 路由命名

采用资源导向的 RESTful 风格（但只使用 GET/POST）：

```
模块前缀/操作名
```

### 6.2 常见路由模式

| 操作 | 路由 | 方法 | 说明 |
|------|------|------|------|
| 列表查询 | /list | GET | 分页列表 |
| 详情查询 | /detail | POST | 单条详情（参数在请求体） |
| 创建 | /create | POST | 新增资源 |
| 更新 | /update | POST | 更新资源 |
| 删除 | /delete | POST | 删除资源 |

### 6.3 实际路由示例

```python
# 会员等级管理
GET  /customer-levels/list        # 查询等级列表
POST /customer-levels/detail      # 查询等级详情
POST /customer-levels/create      # 创建等级
POST /customer-levels/update      # 更新等级
POST /customer-levels/delete      # 删除等级

# 客户管理
GET  /customers/list              # 查询客户列表
POST /customers/detail            # 查询客户详情
POST /customers/create            # 创建客户
POST /customers/update            # 更新客户
POST /customers/delete            # 删除客户

# 商品管理
GET  /products/list               # 查询商品列表
POST /products/detail             # 查询商品详情
POST /products/create             # 创建商品
POST /products/update             # 更新商品
POST /products/delete             # 删除商品
POST /products/stock              # 更新库存

# 价格管理
POST /prices/set                  # 设置价格
POST /prices/batch                # 批量设置价格
POST /prices/product-prices       # 查询商品价格
POST /prices/delete               # 删除价格

# 认证
POST /auth/register               # 用户注册
POST /auth/login                  # 用户登录
POST /auth/change-password        # 修改密码
```

## 7. 开发注意事项

### 7.1 Schema 设计

- 请求 Schema: 字段名使用蛇形命名，配置 `populate_by_name = True`
- 响应 Schema: 字段名使用蛇形命名，添加 `alias` 实现驼峰输出

```python
# 请求 Schema
class ProductCreate(BaseModel):
    product_name: str = Field(...)
    purchase_price: Decimal = Field(...)

    class Config:
        populate_by_name = True

# 响应 Schema
class ProductResponse(BaseModel):
    product_name: str = Field(..., alias="productName")
    purchase_price: Decimal = Field(..., alias="purchasePrice")

    class Config:
        from_attributes = True
        populate_by_name = True
```

### 7.2 参数验证

- 使用 Pydantic 进行参数验证
- 必填字段使用 `Field(...)` 标记
- 可选字段使用 `Field(None)` 标记
- 添加长度、范围等验证规则

### 7.3 错误处理

- 使用统一的异常类（`NotFoundException`、`BadRequestException` 等）
- 异常会被全局异常处理器捕获并转换为标准响应格式
- 不要在接口中直接返回 `Response(code=400, ...)`，应该抛出异常

### 7.4 数据库操作

- 内部使用蛇形命名的字段
- 不要在 SQL 查询中使用驼峰命名
- 使用 ORM 的 `from_attributes` 特性自动映射

## 8. 代码示例

### 8.1 完整的接口示例

```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.response import Response, success_response, PageResponse
from app.schemas.product import ProductCreate, ProductResponse, ProductById
from app.models.product import Product
from app.api.deps import get_current_user, get_current_admin

router = APIRouter(prefix="/products", tags=["商品管理"])

# 列表查询 - GET，所有用户可访问
@router.get("/list", summary="查询商品列表")
async def get_products(
    page_index: int = Query(1, ge=1, alias="pageIndex", description="页码"),
    page_size: int = Query(20, ge=1, le=100, alias="pageSize", description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[PageResponse[ProductResponse]]:
    # 构建查询
    query = db.query(Product)

    # 搜索条件
    if search:
        query = query.filter(Product.name.like(f"%{search}%"))

    # 计算总数
    total = query.count()

    # 分页
    offset = (page_index - 1) * page_size
    products = query.offset(offset).limit(page_size).all()

    # 转换为响应格式
    items = [ProductResponse.model_validate(p) for p in products]

    page_response = PageResponse[ProductResponse](
        total=total,
        items=items,
    )

    return success_response(data=page_response)

# 详情查询 - POST，所有用户可访问
@router.post("/detail", summary="查询商品详情")
async def get_product(
    query: ProductById,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Response[ProductResponse]:
    product = db.query(Product).filter(Product.id == query.id).first()
    if not product:
        raise NotFoundException("商品不存在")

    product_response = ProductResponse.model_validate(product)
    return success_response(data=product_response)

# 创建 - POST，仅管理员可访问
@router.post("/create", summary="创建商品")
async def create_product(
    product_create: ProductCreate,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
) -> Response[ProductResponse]:
    # 创建逻辑...

    product_response = ProductResponse.model_validate(new_product)
    return success_response(data=product_response, msg="商品创建成功")
```

## 9. 测试规范

### 9.1 接口测试

使用工具测试时注意：

1. **路径**: 不要使用路径参数，所有 ID 等参数放在请求体或查询参数中
2. **方法**: 只使用 GET 和 POST
3. **命名**: 请求和响应都使用驼峰命名
4. **分页**: 分页参数使用 `pageIndex` 和 `pageSize`

### 9.2 测试示例

```bash
# 列表查询（使用 GET 和查询参数）
curl -X GET "http://localhost:8000/api/products/list?pageIndex=1&pageSize=20&search=手机" \
  -H "Authorization: Bearer <token>"

# 详情查询（使用 POST 和请求体）
curl -X POST "http://localhost:8000/api/products/detail" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"id": 123}'

# 创建商品（使用 POST）
curl -X POST "http://localhost:8000/api/products/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "商品名称",
    "shortName": "简称",
    "purchasePrice": 100.50,
    "stockQty": 50
  }'
```

## 10. 版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2024-01-08 | 初始版本，定义核心规范 |

---

**注意**: 本规范为项目强制标准，所有开发人员必须严格遵守。如有需要修改或补充，请经团队讨论后更新本文档。
