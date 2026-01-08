# 超市后端管理系统

基于 FastAPI + PostgreSQL 的超市后端管理系统，支持会员等级、差异化定价、客户管理等核心功能。

## 📋 项目简介

本系统是一个轻量级、高效的超市后端管理系统，实现了以下核心功能：

- ✅ **用户管理**：用户注册、登录、权限控制
- ✅ **会员等级管理**：灵活的会员等级配置
- ✅ **客户管理**：完整的客户信息管理
- ✅ **商品管理**：商品信息、进价、库存管理
- ✅ **价格管理**：差异化定价，不同等级享受不同价格
- ✅ **权限控制**：管理员和操作员权限分离

## 🛠️ 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.115+ | 高性能 Python Web 框架 |
| PostgreSQL | 16+ | 关系型数据库 |
| SQLAlchemy | 2.0+ | Python SQL 工具包和 ORM |
| JWT | - | JSON Web Token 身份认证 |
| bcrypt | - | 密码哈希算法 |
| Snowflake | - | 分布式唯一 ID 生成算法 |

## 📁 项目结构

```
shop-backend/
├── app/
│   ├── api/                  # API 路由层
│   │   ├── auth.py           # 认证相关 API
│   │   ├── customer_levels.py # 会员等级管理 API
│   │   ├── customers.py      # 客户管理 API
│   │   ├── products.py       # 商品管理 API
│   │   ├── prices.py         # 价格管理 API
│   │   └── deps.py           # 依赖注入
│   ├── core/                 # 核心配置
│   │   ├── config.py         # 应用配置
│   │   ├── database.py       # 数据库连接
│   │   ├── security.py       # JWT 和密码加密
│   │   ├── snowflake.py      # Snowflake ID 生成器
│   │   ├── response.py       # 统一响应格式
│   │   ├── exceptions.py     # 自定义异常
│   │   └── handlers.py       # 全局异常处理器
│   ├── models/               # 数据模型 (ORM)
│   │   ├── user.py           # 用户模型
│   │   ├── customer_level.py # 会员等级模型
│   │   ├── customer.py       # 客户模型
│   │   ├── product.py        # 商品模型
│   │   └── product_level_price.py # 价格模型
│   ├── schemas/              # Pydantic Schema
│   │   ├── user.py           # 用户 Schema
│   │   ├── customer_level.py # 会员等级 Schema
│   │   ├── customer.py       # 客户 Schema
│   │   ├── product.py        # 商品 Schema
│   │   └── price.py          # 价格 Schema
│   └── main.py               # 应用入口
├── docs/                     # 文档
│   ├── REQUIREMENTS.md       # 需求文档
│   └── SQL_DESIGN.md         # 数据库设计文档
├── .env.example              # 环境变量示例
├── pyproject.toml            # 项目依赖
└── README.md                 # 项目说明
```

## 🚀 快速开始

### 1. 安装依赖

使用 [uv](https://github.com/astral-sh/uv) (推荐):

```bash
# 安装 uv
pip install uv

# 同步依赖
uv sync
```

或使用 pip:

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

创建 PostgreSQL 数据库:

```sql
CREATE DATABASE shop_db;
```

复制环境变量配置文件:

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置数据库连接信息:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/shop_db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 3. 创建数据库表

```bash
# 进入 Python 交互环境
uv run python

# 在 Python 中执行
from app.core.database import engine
from app.models import Base
Base.metadata.create_all(bind=engine)

# 退出
exit()
```

### 4. 启动应用

```bash
# 开发模式（自动重载）
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 访问 API 文档

启动成功后，访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API 端点

### 认证模块 (`/api/v1/auth`)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/register` | 用户注册 | 管理员 |
| POST | `/login` | 用户登录 | 公开 |
| POST | `/change-password` | 修改密码 | 登录用户 |

### 会员等级管理 (`/api/v1/customer-levels`)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/` | 创建等级 | 管理员 |
| GET | `/` | 查询等级列表 | 所有用户 |
| GET | `/{level_id}` | 查询等级详情 | 所有用户 |
| PUT | `/{level_id}` | 更新等级 | 管理员 |
| DELETE | `/{level_id}` | 删除等级 | 管理员 |

### 客户管理 (`/api/v1/customers`)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/` | 创建客户 | 所有用户 |
| GET | `/` | 查询客户列表 | 所有用户 |
| GET | `/{customer_id}` | 查询客户详情 | 所有用户 |
| PUT | `/{customer_id}` | 更新客户 | 管理员 |
| DELETE | `/{customer_id}` | 删除客户 | 管理员 |

### 商品管理 (`/api/v1/products`)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/` | 创建商品 | 管理员 |
| GET | `/` | 查询商品列表 | 所有用户 |
| GET | `/{product_id}` | 查询商品详情 | 所有用户 |
| PUT | `/{product_id}` | 更新商品 | 管理员 |
| DELETE | `/{product_id}` | 删除商品 | 管理员 |
| POST | `/{product_id}/stock` | 更新库存 | 所有用户 |

### 价格管理 (`/api/v1/prices`)

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/` | 设置商品等级价格 | 管理员 |
| POST | `/batch` | 批量设置价格 | 管理员 |
| GET | `/products/{product_id}/prices` | 查询商品价格列表 | 所有用户 |
| DELETE | `/{price_id}` | 删除价格 | 管理员 |

## 📝 统一响应格式

所有接口响应均遵循以下格式：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    // 业务数据
  }
}
```

**状态码说明**：

| code | msg | 说明 |
|------|-----|------|
| 200 | success | 请求成功 |
| 400 | bad request | 请求参数错误 |
| 401 | unauthorized | 未认证或 Token 失效 |
| 403 | forbidden | 权限不足 |
| 404 | not found | 资源不存在 |
| 409 | conflict | 资源冲突（如重复） |
| 500 | internal error | 服务器内部错误 |

## 🔐 认证方式

使用 JWT Bearer Token 认证：

```bash
# 1. 登录获取 Token
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'

# 2. 使用 Token 访问需要认证的接口
curl -X GET "http://localhost:8000/api/v1/products" \
  -H "Authorization: Bearer <your_access_token>"
```

## 📚 文档

- [需求文档](docs/REQUIREMENTS.md) - 详细的功能需求和接口设计
- [数据库设计](docs/SQL_DESIGN.md) - 数据库表结构设计

## 🧪 测试

```bash
# 运行测试（待实现）
uv run pytest

# 查看测试覆盖率
uv run pytest --cov=app --cov-report=html
```

## 🐳 Docker 部署

```bash
# 构建镜像
docker build -t shop-backend .

# 运行容器
docker run -d \
  --name shop-backend \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  shop-backend
```

## 📄 License

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 联系方式

如有问题，请提交 Issue 或联系项目维护者。
