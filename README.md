# 超市后端管理系统

基于 FastAPI + PostgreSQL 的超市后端管理系统,采用分层架构设计。

## 技术栈

- **Web框架**: FastAPI 0.115+
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy 2.0+
- **认证**: JWT (JSON Web Tokens)
- **密码加密**: Bcrypt

## 项目结构

```
shop-backend/
├── app/
│   ├── api/              # API路由层(Controller)
│   │   ├── auth.py       # 认证相关API
│   │   └── deps.py       # 依赖注入
│   ├── core/             # 核心配置
│   │   ├── config.py     # 应用配置
│   │   └── database.py   # 数据库连接
│   ├── dao/              # 数据访问层
│   │   └── user_dao.py   # 用户DAO
│   ├── models/           # 数据模型
│   │   └── user.py       # 用户模型
│   ├── schemas/          # Pydantic schemas
│   │   └── user.py       # 用户Schema
│   ├── service/          # 业务逻辑层
│   │   └── user_service.py # 用户服务
│   └── main.py           # 应用入口
├── .env.example          # 环境变量示例
├── pyproject.toml        # 项目依赖
└── README.md             # 项目说明
```

## 分层架构说明

### Controller层 (app/api/)
- 处理HTTP请求和响应
- 参数验证
- 调用Service层处理业务逻辑
- 返回标准化响应

### Service层 (app/service/)
- 实现业务逻辑
- 调用DAO层访问数据
- 处理跨DAO的数据操作
- 事务管理

### DAO层 (app/dao/)
- 数据库访问对象
- 封装SQL操作
- CRUD操作
- 数据持久化

## 快速开始

### 1. 安装依赖

```bash
# 使用uv (推荐)
pip install uv
uv sync

# 或使用pip
pip install -r requirements.txt
```

### 2. 配置数据库

创建PostgreSQL数据库:
```sql
CREATE DATABASE shop_db;
```

**重要**: 数据库表需要在部署时通过数据库迁移工具创建,本应用不会自动创建表结构。

复制环境变量配置文件:
```bash
cp .env.example .env
```

编辑 `.env` 文件,配置数据库连接信息。

### 3. 启动应用

```bash
# 开发模式
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用Python
python -m uvicorn app.main:app --reload
```

访问 http://localhost:8000 查看 API文档。

### 4. 测试API

#### 用户注册
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "123456",
    "full_name": "测试用户"
  }'
```

#### 用户登录
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456"
  }'
```

#### 获取当前用户信息
```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer <your_token>"
```

## API文档

启动应用后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发规范

### 代码规范
- 遵循PEP 8代码风格
- 使用类型注解
- 函数和类添加docstring

### 提交规范
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具链相关

## 待实现功能

- [ ] 商品管理
- [ ] 订单管理
- [ ] 库存管理
- [ ] 用户权限管理
- [ ] 数据报表统计
- [ ] 单元测试
- [ ] Docker部署

## License

MIT
