# 超市后端系统 · 需求设计文档

> **版本**: v1.0
> **最后更新**: 2025-01-07
> **状态**: 设计阶段

---

## 📋 目录

- [1. 项目概述](#1-项目概述)
- [2. 业务背景](#2-业务背景)
- [3. 功能需求](#3-功能需求)
  - [3.1 用户管理模块](#31-用户管理模块)
  - [3.2 会员等级管理模块](#32-会员等级管理模块)
  - [3.3 客户管理模块](#33-客户管理模块)
  - [3.4 商品管理模块](#34-商品管理模块)
  - [3.5 价格管理模块](#35-价格管理模块)
- [4. 非功能需求](#4-非功能需求)
- [5. 系统架构](#5-系统架构)
- [6. 数据模型](#6-数据模型)
- [7. 接口设计](#7-接口设计)
- [8. 业务流程](#8-业务流程)
- [9. 异常处理](#9-异常处理)
- [10. 安全设计](#10-安全设计)

---

## 1. 项目概述

### 1.1 项目名称

超市后端管理系统（Supermarket Backend System）

### 1.2 项目目标

构建一个轻量级、高效的超市后端管理系统，实现客户管理、商品管理、会员等级定价等核心业务功能，为超市日常运营提供数据支撑和业务管理能力。

**系统包含两个端：**

- **管理端（Admin Web）**：超市内部管理人员使用，进行系统配置、数据管理、报表查看等操作
  - 仅管理员账号可登录
  - 完整的数据管理权限
  - 支持用户、商品、客户、价格等所有功能

- **移动端（Mobile App）**：超市一线销售人员使用，进行日常销售、客户查询等操作
  - 所有登录用户均可访问
  - 只读查询 + 部分业务操作（如库存更新）
  - 简化的界面和操作流程

### 1.3 技术栈

| 类别 | 技术选型 | 说明 |
|------|---------|------|
| 后端框架 | FastAPI | 高性能 Python Web 框架 |
| 数据库 | PostgreSQL 16 | 关系型数据库 |
| ORM | SQLAlchemy | Python SQL 工具包和 ORM |
| 身份认证 | JWT | JSON Web Token |
| 密码加密 | bcrypt | 密码哈希算法 |
| API 文档 | OpenAPI/Swagger | 自动生成 API 文档 |
| 主键生成 | Snowflake | 分布式唯一 ID 生成算法 |

### 1.4 核心特性

- ✅ **双端支持**：管理端和移动端分离，权限明确
- ✅ **多级会员体系**：支持灵活的会员等级配置
- ✅ **差异化定价**：同一商品对不同等级设置不同价格
- ✅ **库存管理**：实时库存跟踪和管理
- ✅ **客户管理**：完整的客户信息管理
- ✅ **权限控制**：管理员和操作员权限分离

---

## 2. 业务背景

### 2.1 业务场景

中小型超市在日常运营中面临以下问题：

1. **客户管理混乱**
   - 客户信息记录不完整
   - 缺乏会员等级体系
   - 无法区分客户价值

2. **定价策略单一**
   - 所有客户统一价格
   - 无法实现差异化营销
   - 缺乏客户粘性

3. **库存管理困难**
   - 库存数据不准确
   - 缺乏成本核算
   - 补货不及时

### 2.2 解决方案

通过建立完善的后端管理系统：

- **会员等级体系**：将客户分为不同等级（普通会员、银卡会员、金卡会员、钻石会员）
- **差异化定价**：不同等级客户享受不同价格，提升客户忠诚度
- **统一管理**：商品、客户、价格集中管理，数据准确可靠
- **成本核算**：记录进价和售价，计算利润

### 2.3 业务价值

| 价值点 | 说明 |
|--------|------|
| 提升客户粘性 | 通过差异化定价激励客户升级等级 |
| 增加销售额 | 高等级客户享受优惠，增加消费频次 |
| 降低成本 | 精准的库存管理减少库存积压 |
| 数据决策 | 准确的业务数据支持经营决策 |

---

## 3. 功能需求

> **重要说明**：所有接口的响应均遵循统一的响应格式 `{"code": xxx, "msg": "xxx", "data": xxx}`。为简化文档阅读，以下各功能模块的"输出结果"示例仅展示 `data` 字段中的内容，实际返回时需包裹在统一格式中。
>
> **完整响应示例**：
> ```json
> {
>   "code": 200,
>   "msg": "success",
>   "data": {
>     // 以下示例中的内容
>   }
> }
> ```

### 3.1 用户管理模块

#### 3.1.1 用户注册

**功能描述**：管理员创建新的后台用户账号。

**业务规则**：
- 用户名必须唯一
- 密码必须加密存储（bcrypt）
- 区分管理员和操作员权限
- 管理员：可以管理用户、商品、客户、价格等所有数据
- 操作员：只能查看数据，不能修改

**输入参数**：
```json
{
  "username": "string (50)",    // 登录用户名，必填，唯一
  "name": "string (50)",        // 真实姓名，必填
  "password": "string (255)",   // 密码，必填
  "admin_flag": "boolean",      // 是否管理员，必填，默认 false
  "phone": "string (30)"        // 联系电话，选填
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "username": "string",
  "name": "string",
  "admin_flag": "boolean",
  "phone": "string",
  "created_at": "timestamp"
}
```
> 完整响应格式参考章节 7.1

**异常处理**：
- 用户名重复：返回 400 错误
- 密码强度不足：返回 400 错误
- 参数验证失败：返回 422 错误

---

#### 3.1.2 用户登录

**功能描述**：用户使用用户名和密码登录系统。

**业务规则**：
- 验证用户名和密码
- 生成 JWT Token（有效期 24 小时）
- 返回用户信息和 Token

**输入参数**：
```json
{
  "username": "string",  // 登录用户名，必填
  "password": "string"   // 密码，必填
}
```

**输出结果**：
```json
{
  "access_token": "string",    // JWT Token
  "token_type": "bearer",
  "user": {
    "id": "bigint",
    "username": "string",
    "name": "string",
    "admin_flag": "boolean"
  }
}
```

**异常处理**：
- 用户名不存在：返回 401 错误
- 密码错误：返回 401 错误
- 账户被禁用：返回 403 错误

---

#### 3.1.3 修改密码

**功能描述**：用户修改自己的登录密码。

**业务规则**：
- 需要提供旧密码验证
- 新密码不能与旧密码相同
- 密码必须加密存储

**输入参数**：
```json
{
  "old_password": "string",  // 旧密码，必填
  "new_password": "string"   // 新密码，必填
}
```

**输出结果**：
```json
{
  "message": "密码修改成功"
}
```

**异常处理**：
- 旧密码错误：返回 401 错误
- 新密码强度不足：返回 400 错误

---

#### 3.1.4 查询用户列表

**功能描述**：管理员查询所有用户列表（仅管理员可用）。

**业务规则**：
- 仅管理员可以访问
- 支持分页查询
- 支持按用户名、姓名搜索

**查询参数**：
- `page`: 页码（默认 1）
- `page_size`: 每页数量（默认 20）
- `search`: 搜索关键词（选填）

**输出结果**：
```json
{
  "total": 100,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "bigint",
      "username": "string",
      "name": "string",
      "admin_flag": "boolean",
      "phone": "string",
      "created_at": "timestamp"
    }
  ]
}
```

---

### 3.2 会员等级管理模块

#### 3.2.1 创建会员等级

**功能描述**：创建新的会员等级（仅管理员可用）。

**业务规则**：
- 等级名称必须唯一
- 等级名称不能为空
- 等级创建后可以被客户使用

**输入参数**：
```json
{
  "level_name": "string (30)"  // 等级名称，必填，唯一
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "level_name": "string",
  "created_at": "timestamp"
}
```

**异常处理**：
- 等级名称重复：返回 400 错误

---

#### 3.2.2 查询等级列表

**功能描述**：查询所有会员等级列表。

**业务规则**：
- 所有用户都可以访问
- 返回等级列表

**输出结果**：
```json
{
  "items": [
    {
      "id": "bigint",
      "level_name": "string",
      "created_at": "timestamp"
    }
  ]
}
```

---

#### 3.2.3 更新会员等级

**功能描述**：修改会员等级名称（仅管理员可用）。

**业务规则**：
- 仅管理员可以修改
- 新名称不能与其他等级重复
- 如果等级已有客户关联，修改需要谨慎

**输入参数**：
```json
{
  "level_name": "string (30)"  // 新等级名称，必填
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "level_name": "string",
  "updated_at": "timestamp"
}
```

**异常处理**：
- 等级不存在：返回 404 错误
- 等级名称重复：返回 400 错误

---

#### 3.2.4 删除会员等级

**功能描述**：删除会员等级（仅管理员可用）。

**业务规则**：
- 仅管理员可以删除
- 如果等级下有关联的客户，不能删除
- 如果等级下有关联的价格，不能删除

**异常处理**：
- 等级不存在：返回 404 错误
- 等级下有客户关联：返回 400 错误，提示"该等级下有客户，无法删除"
- 等级下有价格关联：返回 400 错误，提示"该等级下有价格设置，无法删除"

---

### 3.3 客户管理模块

#### 3.3.1 创建客户

**功能描述**：创建新的客户信息。

**业务规则**：
- 客户必须关联一个会员等级
- 手机号必填
- 地址必填（仅支持单个地址）
- 联系人可选（个人客户可与客户名称相同）

**输入参数**：
```json
{
  "level_id": "bigint",           // 会员等级ID，必填
  "name": "string (50)",          // 客户名称，必填
  "phone": "string (30)",         // 联系电话，必填
  "contact_person": "string (50)", // 联系人，选填
  "address": "text"               // 地址，必填
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "level_id": "bigint",
  "name": "string",
  "phone": "string",
  "contact_person": "string",
  "address": "text",
  "created_at": "timestamp"
}
```

**异常处理**：
- 会员等级不存在：返回 404 错误
- 手机号格式错误：返回 400 错误

---

#### 3.3.2 查询客户列表

**功能描述**：查询客户列表，支持搜索和筛选。

**业务规则**：
- 支持分页查询
- 支持按客户名称、手机号搜索
- 支持按会员等级筛选

**查询参数**：
- `page`: 页码（默认 1）
- `page_size`: 每页数量（默认 20）
- `search`: 搜索关键词（选填）
- `level_id`: 会员等级ID（选填）

**输出结果**：
```json
{
  "total": 100,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "bigint",
      "level_id": "bigint",
      "level_name": "string",
      "name": "string",
      "phone": "string",
      "contact_person": "string",
      "address": "text",
      "created_at": "timestamp"
    }
  ]
}
```

---

#### 3.3.3 查询客户详情

**功能描述**：查询单个客户的详细信息。

**输出结果**：
```json
{
  "id": "bigint",
  "level_id": "bigint",
  "level_name": "string",
  "name": "string",
  "phone": "string",
  "contact_person": "string",
  "address": "text",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

**异常处理**：
- 客户不存在：返回 404 错误

---

#### 3.3.4 更新客户信息

**功能描述**：修改客户信息（仅管理员可用）。

**业务规则**：
- 仅管理员可以修改
- 可以修改等级、名称、电话、联系人、地址
- 修改后记录更新时间

**输入参数**：
```json
{
  "level_id": "bigint",           // 新会员等级ID，选填
  "name": "string (50)",          // 新客户名称，选填
  "phone": "string (30)",         // 新联系电话，选填
  "contact_person": "string (50)", // 新联系人，选填
  "address": "text"               // 新地址，选填
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "level_id": "bigint",
  "name": "string",
  "phone": "string",
  "contact_person": "string",
  "address": "text",
  "updated_at": "timestamp"
}
```

**异常处理**：
- 客户不存在：返回 404 错误
- 会员等级不存在：返回 404 错误

---

#### 3.3.5 删除客户

**功能描述**：删除客户信息（仅管理员可用）。

**业务规则**：
- 仅管理员可以删除
- 删除前需要确认
- 删除后客户信息不可恢复

**异常处理**：
- 客户不存在：返回 404 错误

---

### 3.4 商品管理模块

#### 3.4.1 创建商品

**功能描述**：创建新的商品信息。

**业务规则**：
- 商品名称和简称必填
- 条形码唯一（选填）
- 图片URL选填
- 进价必填，用于成本核算
- 库存默认为 0

**输入参数**：
```json
{
  "name": "string (100)",      // 商品全称，必填
  "short_name": "string (50)", // 商品简称，必填
  "spec": "string (50)",       // 规格型号，选填
  "barcode": "string (64)",    // 条形码，选填，唯一
  "image_url": "string (512)", // 商品图片URL，选填
  "purchase_price": "decimal(12,2)", // 进价，必填
  "stock_qty": "int"           // 库存数量，选填，默认 0
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "name": "string",
  "short_name": "string",
  "spec": "string",
  "barcode": "string",
  "image_url": "string",
  "purchase_price": "decimal(12,2)",
  "stock_qty": "int",
  "created_at": "timestamp"
}
```

**异常处理**：
- 条形码重复：返回 400 错误
- 进价必须大于 0：返回 400 错误

---

#### 3.4.2 查询商品列表

**功能描述**：查询商品列表，支持搜索和筛选。

**业务规则**：
- 支持分页查询
- 支持按商品名称、简称、条形码搜索
- 支持按库存状态筛选（有库存/无库存）

**查询参数**：
- `page`: 页码（默认 1）
- `page_size`: 每页数量（默认 20）
- `search`: 搜索关键词（选填）
- `in_stock`: 是否有库存（选填，true/false）

**输出结果**：
```json
{
  "total": 100,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "bigint",
      "name": "string",
      "short_name": "string",
      "spec": "string",
      "barcode": "string",
      "image_url": "string",
      "purchase_price": "decimal(12,2)",
      "stock_qty": "int",
      "created_at": "timestamp"
    }
  ]
}
```

---

#### 3.4.3 查询商品详情

**功能描述**：查询单个商品的详细信息。

**业务规则**：
- 返回商品基本信息
- 返回所有等级的价格列表

**输出结果**：
```json
{
  "id": "bigint",
  "name": "string",
  "short_name": "string",
  "spec": "string",
  "barcode": "string",
  "image_url": "string",
  "purchase_price": "decimal(12,2)",
  "stock_qty": "int",
  "created_at": "timestamp",
  "prices": [
    {
      "level_id": "bigint",
      "level_name": "string",
      "sale_price": "decimal(12,2)"
    }
  ]
}
```

**异常处理**：
- 商品不存在：返回 404 错误

---

#### 3.4.4 更新商品信息

**功能描述**：修改商品信息（仅管理员可用）。

**业务规则**：
- 仅管理员可以修改
- 可以修改名称、规格、条形码、图片、进价、库存
- 修改后记录更新时间

**输入参数**：
```json
{
  "name": "string (100)",      // 新商品全称，选填
  "short_name": "string (50)", // 新商品简称，选填
  "spec": "string (50)",       // 新规格型号，选填
  "barcode": "string (64)",    // 新条形码，选填
  "image_url": "string (512)", // 新图片URL，选填
  "purchase_price": "decimal(12,2)", // 新进价，选填
  "stock_qty": "int"           // 新库存数量，选填
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "name": "string",
  "short_name": "string",
  "spec": "string",
  "barcode": "string",
  "image_url": "string",
  "purchase_price": "decimal(12,2)",
  "stock_qty": "int",
  "updated_at": "timestamp"
}
```

**异常处理**：
- 商品不存在：返回 404 错误
- 条形码重复：返回 400 错误

---

#### 3.4.5 删除商品

**功能描述**：删除商品信息（仅管理员可用）。

**业务规则**：
- 仅管理员可以删除
- 如果商品下有关联的价格，需要先删除价格才能删除商品
- 删除前需要确认

**异常处理**：
- 商品不存在：返回 404 错误
- 商品下有价格关联：返回 400 错误，提示"该商品有价格设置，请先删除价格"

---

#### 3.4.6 更新库存

**功能描述**：调整商品库存数量。

**业务规则**：
- 仅管理员可以修改
- 支持增加库存（进货）
- 支持减少库存（销售）
- 库存不能为负数

**输入参数**：
```json
{
  "delta": "int",  // 库存变化量（正数增加，负数减少）
  "reason": "string" // 变更原因，选填
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "stock_qty": "int",
  "updated_at": "timestamp"
}
```

**异常处理**：
- 商品不存在：返回 404 错误
- 库存不足（减少后为负）：返回 400 错误

---

### 3.5 价格管理模块

#### 3.5.1 设置商品等级价格

**功能描述**：为指定商品设置某个等级的销售价格。

**业务规则**：
- 仅管理员可以设置
- 同一商品同一等级只能有一个价格
- 价格必须大于 0
- 如果价格已存在，则更新

**输入参数**：
```json
{
  "product_id": "bigint",      // 商品ID，必填
  "level_id": "bigint",        // 等级ID，必填
  "sale_price": "decimal(12,2)" // 销售价格，必填
}
```

**输出结果**：
```json
{
  "id": "bigint",
  "product_id": "bigint",
  "level_id": "bigint",
  "sale_price": "decimal(12,2)",
  "created_at": "timestamp"
}
```

**异常处理**：
- 商品不存在：返回 404 错误
- 等级不存在：返回 404 错误
- 价格必须大于 0：返回 400 错误

---

#### 3.5.2 批量设置商品价格

**功能描述**：为商品批量设置所有等级的价格。

**业务规则**：
- 仅管理员可以设置
- 一次传入所有等级的价格
- 验证所有等级ID和价格的有效性

**输入参数**：
```json
{
  "product_id": "bigint",  // 商品ID，必填
  "prices": [
    {
      "level_id": "bigint",
      "sale_price": "decimal(12,2)"
    }
  ]
}
```

**输出结果**：
```json
{
  "product_id": "bigint",
  "created_count": 4,
  "updated_count": 0
}
```

**异常处理**：
- 商品不存在：返回 404 错误
- 等级不存在：返回 404 错误
- 价格数据不完整：返回 400 错误

---

#### 3.5.3 查询商品价格列表

**功能描述**：查询指定商品的所有等级价格。

**业务规则**：
- 所有用户都可以访问
- 返回该商品所有等级的价格

**输出结果**：
```json
{
  "product_id": "bigint",
  "product_name": "string",
  "prices": [
    {
      "id": "bigint",
      "level_id": "bigint",
      "level_name": "string",
      "sale_price": "decimal(12,2)",
      "updated_at": "timestamp"
    }
  ]
}
```

**异常处理**：
- 商品不存在：返回 404 错误

---

#### 3.5.4 删除商品等级价格

**功能描述**：删除指定商品的某个等级价格（仅管理员可用）。

**业务规则**：
- 仅管理员可以删除
- 删除后该等级客户无法购买该商品（或使用默认价格）

**异常处理**：
- 商品不存在：返回 404 错误
- 等级不存在：返回 404 错误
- 价格不存在：返回 404 错误

---

## 4. 非功能需求

### 4.1 性能要求

| 指标 | 要求 | 说明 |
|------|------|------|
| 响应时间 | < 200ms | 普通 API 请求（P95） |
| 并发用户 | 100+ | 支持同时在线用户数 |
| 数据库连接 | 20+ | 连接池大小 |
| 查询性能 | < 100ms | 列表查询（P95） |

### 4.2 可用性要求

| 指标 | 要求 | 说明 |
|------|------|------|
| 系统可用性 | 99%+ | 年度目标 |
| 故障恢复时间 | < 10分钟 | 服务重启时间 |
| 数据备份 | 每日一次 | 自动备份 |

### 4.3 安全性要求

| 安全项 | 要求 |
|--------|------|
| 身份认证 | JWT Token 认证 |
| 密码存储 | bcrypt 加密 |
| API 访问 | 基于 Token 的访问控制 |
| SQL 注入 | 使用 ORM 防止 |
| XSS 防护 | 输入验证和转义 |

### 4.4 可扩展性要求

| 扩展项 | 要求 |
|--------|------|
| 水平扩展 | 支持多实例部署 |
| 数据库扩展 | 支持读写分离 |
| 缓存支持 | 预留 Redis 接口 |

### 4.5 可维护性要求

| 维护项 | 要求 |
|--------|------|
| 代码规范 | 遵循 PEP 8 |
| 日志记录 | 完整的操作日志 |
| 错误处理 | 统一的异常处理 |
| API 文档 | 自动生成并保持更新 |

---

## 5. 系统架构

### 5.1 分层架构

```
┌─────────────────────────────────────────┐
│           API Gateway / 负载均衡          │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│          FastAPI 应用层 (多实例)          │
│  ┌──────────┬──────────┬──────────┐     │
│  │ 用户管理  │ 商品管理  │ 客户管理  │     │
│  └──────────┴──────────┴──────────┘     │
│  ┌──────────┬──────────┬──────────┐     │
│  │ 权限控制  │ 业务逻辑  │ 数据验证  │     │
│  └──────────┴──────────┴──────────┘     │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         SQLAlchemy ORM 层                │
│  ┌──────────┬──────────┬──────────┐     │
│  │ User Model│ Product  │ Customer │     │
│  └──────────┴──────────┴──────────┘     │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│       PostgreSQL 数据库层                 │
│  ┌──────────┬──────────┬──────────┐     │
│  │   users  │ products │customers │     │
│  └──────────┴──────────┴──────────┘     │
└─────────────────────────────────────────┘
```

### 5.2 目录结构

```
shop-backend/
├── app/
│   ├── api/                 # API 路由
│   │   ├── v1/
│   │   │   ├── auth.py      # 认证相关
│   │   │   ├── users.py     # 用户管理
│   │   │   ├── customers.py # 客户管理
│   │   │   ├── products.py  # 商品管理
│   │   │   └── prices.py    # 价格管理
│   ├── core/                # 核心配置
│   │   ├── config.py        # 配置文件
│   │   ├── security.py      # 安全相关
│   │   └── snowflake.py     # ID生成器
│   ├── models/              # 数据模型
│   │   ├── user.py
│   │   ├── customer.py
│   │   └── product.py
│   ├── schemas/             # Pydantic 模式
│   │   ├── user.py
│   │   ├── customer.py
│   │   └── product.py
│   ├── services/            # 业务逻辑
│   │   ├── user_service.py
│   │   └── product_service.py
│   └── utils/               # 工具函数
│       ├── password.py      # 密码加密
│       └── validators.py    # 数据验证
├── docs/                    # 文档
│   ├── SQL_DESIGN.md
│   └── REQUIREMENTS.md
├── tests/                   # 测试
│   ├── api/
│   └── services/
├── alembic/                 # 数据库迁移
├── .env                     # 环境变量
├── main.py                  # 应用入口
└── requirements.txt         # 依赖列表
```

---

## 6. 数据模型

### 6.1 ER 图

```
┌─────────────────┐
│     users       │ 后台用户
├─────────────────┤
│ id (PK)         │
│ username        │
│ password        │
│ name            │
│ admin_flag      │
│ phone           │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐
│customer_levels  │ 会员等级
├─────────────────┤
│ id (PK)         │
│ level_name      │
│ created_at      │
│ updated_at      │
└─────────────────┘
       │
       │ 1:N
       │
       ↓
┌─────────────────┐
│   customers     │ 客户
├─────────────────┤
│ id (PK)         │
│ level_id (FK)   │──→ customer_levels.id
│ name            │
│ phone           │
│ contact_person  │
│ address         │
│ created_at      │
│ updated_at      │
└─────────────────┘

┌─────────────────┐
│    products     │ 商品
├─────────────────┤
│ id (PK)         │
│ name            │
│ short_name      │
│ spec            │
│ barcode         │
│ purchase_price  │
│ stock_qty       │
│ created_at      │
│ updated_at      │
└─────────────────┘
       │
       │ 1:N
       │
       ↓
┌─────────────────────────────────────┐
│      product_level_prices           │ 商品等级价格
├─────────────────────────────────────┤
│ id (PK)                             │
│ product_id (FK)         │──→ products.id
│ level_id (FK)           │──→ customer_levels.id
│ sale_price                          │
│ created_at                          │
│ updated_at                          │
│ UNIQUE (product_id, level_id)       │
└─────────────────────────────────────┘
```

### 6.2 数据字典

详见 `SQL_DESIGN.md` 文档。

---

## 7. 接口设计

### 7.1 API 基础信息

**Base URL**: `http://localhost:8000/api/v1`

**认证方式**: JWT Bearer Token

**请求头**:
```
Content-Type: application/json
Authorization: Bearer <access_token>
```

**统一响应格式**:

所有接口响应均遵循以下格式（成功和失败）：

```json
{
  "code": 200,          // 状态码
  "msg": "success",     // 消息描述
  "data": {}            // 实际数据，放在data字段中
}
```

**响应状态码说明**：

| code | msg | 说明 |
|------|-----|------|
| 200 | success | 请求成功 |
| 400 | bad request | 请求参数错误 |
| 401 | unauthorized | 未认证或Token失效 |
| 403 | forbidden | 权限不足 |
| 404 | not found | 资源不存在 |
| 409 | conflict | 资源冲突（如重复） |
| 500 | internal error | 服务器内部错误 |

**成功响应示例**：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "id": 123456789012345678,
    "username": "admin",
    "name": "管理员"
  }
}
```

**分页响应示例**：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 20,
    "items": [...]
  }
}
```

**错误响应示例**：

```json
{
  "code": 400,
  "msg": "用户名已存在",
  "data": null
}
```

**重要说明**：
- 所有业务数据必须放在 `data` 字段中
- 列表接口返回的 items 也放在 `data.items` 中
- 即使没有返回数据，也要返回 `data: null` 或 `data: {}`
- 不要在根级别直接返回业务数据

### 7.2 API 列表

**端说明**：
- 🔒 **管理端独有**：仅管理员可访问，用于管理端 Web 系统
- 📱 **移动端独有**：所有登录用户可访问，用于移动端 App
- 🔄 **共用**：管理端和移动端都可访问

#### 7.2.1 认证模块（共用）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /auth/register | 用户注册 | 🔒 管理员 |
| POST | /auth/login | 用户登录 | 公开 |
| POST | /auth/change-password | 修改密码 | 🔄 登录用户 |
| POST | /auth/refresh | 刷新Token | 🔄 登录用户 |

#### 7.2.2 用户管理模块（管理端独有）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /users | 查询用户列表 | 🔒 管理员 |
| GET | /users/{id} | 查询用户详情 | 🔒 管理员 |
| PUT | /users/{id} | 更新用户信息 | 🔒 管理员 |
| DELETE | /users/{id} | 删除用户 | 🔒 管理员 |

#### 7.2.3 会员等级管理模块（共用）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /customer-levels | 创建等级 | 🔒 管理员 |
| GET | /customer-levels | 查询等级列表 | 🔄 所有用户 |
| GET | /customer-levels/{id} | 查询等级详情 | 🔄 所有用户 |
| PUT | /customer-levels/{id} | 更新等级 | 🔒 管理员 |
| DELETE | /customer-levels/{id} | 删除等级 | 🔒 管理员 |

#### 7.2.4 客户管理模块（共用）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /customers | 创建客户 | 🔄 所有用户 |
| GET | /customers | 查询客户列表 | 🔄 所有用户 |
| GET | /customers/{id} | 查询客户详情 | 🔄 所有用户 |
| PUT | /customers/{id} | 更新客户信息 | 🔒 管理员 |
| DELETE | /customers/{id} | 删除客户 | 🔒 管理员 |

#### 7.2.5 商品管理模块（共用）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /products | 创建商品 | 🔒 管理员 |
| GET | /products | 查询商品列表 | 🔄 所有用户 |
| GET | /products/{id} | 查询商品详情 | 🔄 所有用户 |
| PUT | /products/{id} | 更新商品信息 | 🔒 管理员 |
| DELETE | /products/{id} | 删除商品 | 🔒 管理员 |
| POST | /products/{id}/stock | 更新库存 | 🔄 所有用户 |

#### 7.2.6 价格管理模块（共用）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /prices | 设置商品等级价格 | 🔒 管理员 |
| POST | /prices/batch | 批量设置价格 | 🔒 管理员 |
| GET | /products/{id}/prices | 查询商品价格列表 | 🔄 所有用户 |
| DELETE | /prices/{id} | 删除价格 | 🔒 管理员 |

---

## 8. 业务流程

### 8.1 新用户注册流程

```mermaid
sequenceDiagram
    participant Admin as 管理员
    participant API as 后端API
    participant DB as 数据库

    Admin->>API: POST /auth/register<br/>{username, password, name, admin_flag}
    API->>API: 验证参数
    API->>API: 检查用户名是否重复
    API->>API: 加密密码 (bcrypt)
    API->>DB: 生成雪花ID
    API->>DB: 插入用户记录
    DB-->>API: 返回用户信息
    API-->>Admin: 返回创建结果
```

### 8.2 用户登录流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant API as 后端API
    participant DB as 数据库

    User->>API: POST /auth/login<br/>{username, password}
    API->>DB: 查询用户
    DB-->>API: 返回用户信息
    API->>API: 验证密码
    API->>API: 生成JWT Token
    API-->>User: 返回Token和用户信息
```

### 8.3 创建商品并设置价格流程

```mermaid
sequenceDiagram
    participant Admin as 管理员
    participant API as 后端API
    participant DB as 数据库

    Admin->>API: 1. POST /products 创建商品
    API->>DB: 插入商品记录
    DB-->>API: 返回商品ID

    Admin->>API: 2. POST /prices/batch 批量设置价格
    API->>API: 验证所有等级ID
    API->>DB: 批量插入价格记录
    DB-->>API: 返回成功数量

    API-->>Admin: 返回创建结果
```

### 8.4 客户购买商品流程（查询价格）

```mermaid
sequenceDiagram
    participant Operator as 操作员
    participant API as 后端API
    participant DB as 数据库

    Operator->>API: 输入客户信息和商品条码
    API->>DB: 查询客户等级
    DB-->>API: 返回等级ID

    API->>DB: 查询商品信息
    DB-->>API: 返回商品信息

    API->>DB: 查询商品在该等级的价格
    DB-->>API: 返回销售价格

    API-->>Operator: 显示价格和库存
```

---

## 9. 异常处理

### 9.1 异常分类

所有异常均使用统一的响应格式，通过 `code` 字段区分不同类型：

| code | msg | HTTP状态码 | 说明 |
|------|-----|-----------|------|
| 400 | bad request | 400 | 参数验证失败 |
| 401 | unauthorized | 401 | 未认证或Token失效 |
| 403 | forbidden | 403 | 权限不足 |
| 404 | not found | 404 | 资源不存在 |
| 409 | conflict | 409 | 资源冲突（如重复） |
| 500 | internal error | 500 | 服务器内部错误 |

### 9.2 异常响应格式

所有异常响应均遵循统一格式：

```json
{
  "code": 400,
  "msg": "用户名已存在",
  "data": null
}
```

---

## 10. 部署配置

### 环境变量

```bash
# .env 文件
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Snowflake 配置
DATACENTER_ID=1
WORKER_ID=1
```

### 启动命令

```bash
# 开发环境
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 生产环境
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 11. 项目计划

| 阶段 | 任务 | 预计工期 |
|------|------|---------|
| 第一阶段 | 搭建项目框架、数据库设计 | 3天 |
| 第二阶段 | 用户认证、权限管理 | 2天 |
| 第三阶段 | 会员等级、客户管理 | 3天 |
| 第四阶段 | 商品、价格管理 | 4天 |
| 第五阶段 | 测试、优化、文档 | 3天 |

**总计**：约 15 个工作日

---
