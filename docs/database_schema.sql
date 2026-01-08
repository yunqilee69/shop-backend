-- ============================================
-- 超市管理系统数据库初始化脚本
-- ============================================

-- 1. 创建会员等级表
CREATE TABLE customer_levels (
    id BIGINT PRIMARY KEY,
    level_name VARCHAR(30) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE customer_levels IS '会员等级表';
COMMENT ON COLUMN customer_levels.id IS '主键ID (Snowflake ID)';
COMMENT ON COLUMN customer_levels.level_name IS '等级名称';

-- 2. 创建用户表
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(200) NOT NULL,
    admin_flag BOOLEAN DEFAULT FALSE NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE users IS '用户表';
COMMENT ON COLUMN users.username IS '登录账号';
COMMENT ON COLUMN users.name IS '用户名称';
COMMENT ON COLUMN users.password IS '密码(加密)';
COMMENT ON COLUMN users.admin_flag IS '是否为管理员';
COMMENT ON COLUMN users.phone IS '手机号';

CREATE INDEX idx_users_username ON users(username);

-- 3. 创建客户表
CREATE TABLE customers (
    id BIGINT PRIMARY KEY,
    level_id BIGINT NOT NULL,
    name VARCHAR(50) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    contact_person VARCHAR(50),
    address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (level_id) REFERENCES customer_levels(id)
);

COMMENT ON TABLE customers IS '客户表';
COMMENT ON COLUMN customers.level_id IS '会员等级ID';
COMMENT ON COLUMN customers.name IS '客户名称';
COMMENT ON COLUMN customers.phone IS '联系电话';
COMMENT ON COLUMN customers.contact_person IS '联系人';
COMMENT ON COLUMN customers.address IS '地址';

-- 4. 创建商品表
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    short_name VARCHAR(50) NOT NULL,
    spec VARCHAR(50),
    barcode VARCHAR(64) UNIQUE,
    image_url VARCHAR(512),
    purchase_price NUMERIC(12, 2) NOT NULL,
    stock_qty INTEGER DEFAULT 0 NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE products IS '商品表';
COMMENT ON COLUMN products.name IS '商品全称';
COMMENT ON COLUMN products.short_name IS '商品简称';
COMMENT ON COLUMN products.spec IS '规格型号';
COMMENT ON COLUMN products.barcode IS '条形码';
COMMENT ON COLUMN products.image_url IS '商品图片URL';
COMMENT ON COLUMN products.purchase_price IS '进价';
COMMENT ON COLUMN products.stock_qty IS '库存数量';

-- 5. 创建商品等级价格表
CREATE TABLE product_level_prices (
    id BIGINT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    level_id BIGINT NOT NULL,
    sale_price NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (level_id) REFERENCES customer_levels(id),
    UNIQUE (product_id, level_id)
);

COMMENT ON TABLE product_level_prices IS '商品等级价格表';
COMMENT ON COLUMN product_level_prices.product_id IS '商品ID';
COMMENT ON COLUMN product_level_prices.level_id IS '会员等级ID';
COMMENT ON COLUMN product_level_prices.sale_price IS '销售价格';

-- ============================================
-- 插入默认管理员账号
-- ============================================
-- 用户名: admin
-- 密码: 123456 (bcrypt加密后的值)
INSERT INTO users (id, username, name, password, admin_flag, phone)
VALUES (
    1,
    'admin',
    '系统管理员',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLaEmc9i',
    TRUE,
    '13800138000'
);

-- ============================================
-- 插入示例会员等级数据
-- ============================================
INSERT INTO customer_levels (id, level_name) VALUES
(1, '普通会员'),
(2, '银卡会员'),
(3, '金卡会员'),
(4, '钻石会员');

COMMIT;
