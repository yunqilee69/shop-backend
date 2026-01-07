# 超市后端系统 · 数据库设计文档

> **PostgreSQL 16** | 最小化表结构设计 | **主键策略：雪花算法 (Snowflake)**

---

## 📋 目录

- [1. 表结构概览](#1-表结构概览)
- [2. 字段详细设计](#2-字段详细设计)
  - [2.1 users - 后台用户表](#21-users---后台用户表)
  - [2.2 customer_levels - 会员等级表](#22-customer_levels---会员等级表)
  - [2.3 customers - 会员客户表](#23-customers---会员客户表)
  - [2.4 products - 商品表](#24-products---商品表)
  - [2.5 product_level_prices - 商品等级价格表](#25-product_level_prices---商品等级价格表)
- [3. 主键设计说明](#3-主键设计说明)
- [4. 表关系说明](#4-表关系说明)
- [5. 索引建议](#5-索引建议)

---

## 1. 表结构概览

| 表名                     | 中文名    | 说明              | 
|------------------------|--------|-----------------|
| `users`                | 后台用户   | 系统管理员和操作员       | 
| `customer_levels`      | 会员等级   | 客户等级定义（仅ID+名称）  | 
| `customers`            | 会员客户   | 客户信息（单地址，无折扣字段） |
| `products`             | 商品     | 商品主表（含库存、进价）    | 
| `product_level_prices` | 商品等级价格 | 一品多级一价          | 

---

## 2. 字段详细设计

### 2.1 users - 后台用户表

```sql
CREATE TABLE users (
    id          bigint primary key,
    username    varchar(50) not null unique,
    name        varchar(50) not null,
    password    varchar(255) not null,
    admin_flag  boolean not null default false,
    phone       varchar(30),
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);
```

**字段说明：**
- `id`: 主键，使用雪花算法生成的64位唯一ID
- `username`: 登录用户名，唯一
- `name`: 真实姓名
- `password`: 密码（加密存储）
- `admin_flag`: 管理员标识
- `phone`: 联系电话
- `created_at`: 创建时间
- `updated_at`: 更新时间

---

### 2.2 customer_levels - 会员等级表

```sql
CREATE TABLE customer_levels (
    id          bigint primary key,
    level_name  varchar(30) not null unique,
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);
```

**字段说明：**
- `id`: 主键，使用雪花算法生成的64位唯一ID
- `level_name`: 等级名称（如：普通会员、银卡会员、金卡会员）
- `created_at`: 创建时间
- `updated_at`: 更新时间

**设计要点：**
- 仅保留 id 和名称，保持最小化
- 等级名称唯一，防止重复

---

### 2.3 customers - 会员客户表

```sql
CREATE TABLE customers (
    id             bigint primary key,
    level_id       bigint not null references customer_levels(id),
    name           varchar(50) not null,
    phone          varchar(30) not null,
    contact_person varchar(50),
    address        text not null,
    created_at     timestamptz not null default now(),
    updated_at     timestamptz not null default now()
);
```

**字段说明：**
- `id`: 主键，使用雪花算法生成的64位唯一ID
- `level_id`: 会员等级ID，外键关联 `customer_levels(id)`
- `name`: 客户名称（企业或个人）
- `phone`: 联系电话
- `contact_person`: 联系人（可与 name 相同）
- `address`: 配送地址（单地址）
- `created_at`: 创建时间
- `updated_at`: 更新时间

**设计要点：**
- 每个客户仅支持一个地址
- 无折扣字段，折扣通过等级价格实现
- `contact_person` 可用于企业客户的联系人

---

### 2.4 products - 商品表

```sql
CREATE TABLE products (
    id              bigint primary key,
    name            varchar(100) not null,
    short_name      varchar(50) not null,
    spec            varchar(50),
    barcode         varchar(64) unique,
    image_url       varchar(512),
    purchase_price  numeric(12,2) not null,
    stock_qty       int not null default 0,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now()
);
```

**字段说明：**
- `id`: 主键，使用雪花算法生成的64位唯一ID
- `name`: 商品全称
- `short_name`: 商品简称
- `spec`: 规格型号
- `barcode`: 条形码（唯一）
- `image_url`: 商品图片URL（可选）
- `purchase_price`: 进价（采购成本价）
- `stock_qty`: 库存数量
- `created_at`: 创建时间
- `updated_at`: 更新时间

**设计要点：**
- `barcode` 设置唯一索引，防止商品重复
- `image_url` 存储商品图片的完整URL地址（如：https://example.com/images/product.jpg）
- 进价用于成本核算
- 库存数量默认为 0

---

### 2.5 product_level_prices - 商品等级价格表

```sql
CREATE TABLE product_level_prices (
    id          bigint primary key,
    product_id  bigint not null references products(id),
    level_id    bigint not null references customer_levels(id),
    sale_price  numeric(12,2) not null,
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now(),
    unique (product_id, level_id)
);
```

**字段说明：**
- `id`: 主键，使用雪花算法生成的64位唯一ID
- `product_id`: 商品ID，外键关联 `products(id)`
- `level_id`: 等级ID，外键关联 `customer_levels(id)`
- `sale_price`: 销售价格
- `created_at`: 创建时间
- `updated_at`: 更新时间

**设计要点：**
- **一品多级一价**：同一商品对不同等级设置不同价格
- 联合唯一约束 `(product_id, level_id)` 确保每个商品在每个等级只有一个价格
- 删除商品或等级前，需要先删除关联的价格记录

---

## 3. 主键设计说明

### 3.1 为什么不使用数据库自增？

**自增主键的问题：**

| 问题 | 说明 | 影响 |
|------|------|------|
| 分布式冲突 | 多个数据库实例自增ID会重复 | 数据合并时冲突 |
| 暴露业务量 | ID连续可推断订单量、用户量 | 商业机密泄露 |
| 性能瓶颈 | 高并发插入时锁竞争 | 系统吞吐量下降 |
| 迁移困难 | 依赖数据库序列 | 数据迁移复杂 |

### 3.2 雪花算法 (Snowflake) 设计

**ID 结构（64位）：**

```
0 | 0000000000 0000000000 0000000000 0000000000 0 | 0000000000 | 000000000000
↑   ←────────────── 41位时间戳(毫秒) ────────────→   ←─ 10位机器ID →  ←─ 12位序列 →
│
└─ 符号位(永远为0)
```

**组成部分：**
- **1位符号位**：始终为0
- **41位时间戳**：毫秒级精度，可用69年
- **10位机器ID**：支持1024台机器
- **12位序列号**：每毫秒可生成4096个ID

**优点：**
- ✅ 全局唯一，分布式安全
- ✅ 时间有序，索引性能好
- ✅ 高性能，本地生成无需网络请求
- ✅ 64位整数，存储空间小
- ✅ 不暴露业务量

**Python 实现示例：**

```python
import time
import threading

class SnowflakeGenerator:
    def __init__(self, datacenter_id=1, worker_id=1, epoch=1609459200000):
        """
        初始化雪花ID生成器
        :param datacenter_id: 数据中心ID (0-31)
        :param worker_id: 工作机器ID (0-31)
        :param epoch: 起始时间戳（毫秒），默认2021-01-01 00:00:00
        """
        self.datacenter_id = datacenter_id & 0x1F  # 5位
        self.worker_id = worker_id & 0x1F          # 5位
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _current_millis(self):
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp):
        timestamp = self._current_millis()
        while timestamp <= last_timestamp:
            timestamp = self._current_millis()
        return timestamp

    def generate_id(self):
        with self.lock:
            timestamp = self._current_millis()

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & 0xFFF
                if self.sequence == 0:
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            # 组装ID
            snowflake_id = (
                ((timestamp - self.epoch) << 22) |
                (self.datacenter_id << 17) |
                (self.worker_id << 12) |
                self.sequence
            )

            return snowflake_id

# 使用示例
id_generator = SnowflakeGenerator(datacenter_id=1, worker_id=1)
new_id = id_generator.generate_id()
print(f"Generated ID: {new_id}")
```

### 3.3 使用建议

**配置管理：**
- 每个服务实例配置唯一的 `datacenter_id` 和 `worker_id`
- 可以通过配置文件或环境变量管理
- 建议使用注册中心自动分配避免冲突

**示例配置：**

```python
# config.py
SNOWFLAKE = {
    'datacenter_id': 1,  # 数据中心ID
    'worker_id': 1,      # 机器ID
}
```

---

## 4. 表关系说明

```
customer_levels (1) ----< (N) customers
                           |
                           V
                        (1) customers

products (1) ----< (N) product_level_prices
                           |
                           V
customer_levels (1) ----< (N) product_level_prices
```

**关系说明：**

1. **customer_levels → customers**
   - 一对多关系：一个等级可对应多个客户
   - 客户必须属于某个等级

2. **products → product_level_prices**
   - 一对多关系：一个商品可设置多个等级价格
   - 每个等级对应一个价格

3. **customer_levels → product_level_prices**
   - 一对多关系：一个等级可对应多个商品的价格
   - 通过此表实现不同等级的客户购买同一商品享受不同价格

---

## 5. 索引建议

为了提升查询性能，建议添加以下索引：

```sql
-- customers 表
CREATE INDEX idx_customers_level_id ON customers(level_id);
CREATE INDEX idx_customers_phone ON customers(phone);

-- products 表
CREATE INDEX idx_products_barcode ON products(barcode);
CREATE INDEX idx_products_name ON products(name);

-- product_level_prices 表
CREATE INDEX idx_product_level_prices_product_id ON product_level_prices(product_id);
CREATE INDEX idx_product_level_prices_level_id ON product_level_prices(level_id);
```

---

## 6. 数据完整性约束

### 6.1 检查约束（可选）

```sql
-- 确保价格为正数
ALTER TABLE products ADD CONSTRAINT chk_purchase_price_positive CHECK (purchase_price > 0);
ALTER TABLE product_level_prices ADD CONSTRAINT chk_sale_price_positive CHECK (sale_price > 0);

-- 确保库存非负
ALTER TABLE products ADD CONSTRAINT chk_stock_qty_non_negative CHECK (stock_qty >= 0);
```

### 6.2 触发器建议

```sql
-- 自动更新 updated_at 字段
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_customer_levels_updated_at BEFORE UPDATE ON customer_levels
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_level_prices_updated_at BEFORE UPDATE ON product_level_prices
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## 7. 初始化数据示例

```sql
-- 插入会员等级
INSERT INTO customer_levels (level_name) VALUES
    ('普通会员'),
    ('银卡会员'),
    ('金卡会员'),
    ('钻石会员');

-- 插入测试商品
INSERT INTO products (name, short_name, spec, barcode, purchase_price, stock_qty) VALUES
    ('可口可乐500ml', '可口可乐', '500ml/瓶', '6901234567890', 2.50, 100),
    ('康师傅红烧牛肉面', '红烧牛肉面', '105g/桶', '6901234567891', 3.00, 200),
    ('伊利纯牛奶250ml', '伊利牛奶', '250ml/盒', '6901234567892', 2.00, 150);

-- 为不同等级设置价格（以可口可乐为例）
INSERT INTO product_level_prices (product_id, level_id, sale_price) VALUES
    (1, 1, 3.50),  -- 普通会员价格
    (1, 2, 3.30),  -- 银卡会员价格
    (1, 3, 3.00),  -- 金卡会员价格
    (1, 4, 2.80);  -- 钻石会员价格
```

---

**文档版本**：v1.0
**最后更新**：2025-01-07
**维护者**：超市后端开发团队
