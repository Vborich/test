from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "username" VARCHAR(256) NOT NULL UNIQUE,
    "password" VARCHAR(256) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "products" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "price_rub" DECIMAL(10,2) NOT NULL,
    "owner_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "carts" (
    "id" UUID NOT NULL  PRIMARY KEY,
    "product_id" UUID NOT NULL REFERENCES "products" ("id") ON DELETE CASCADE,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
ALTER TABLE users ALTER COLUMN id SET DEFAULT uuid_generate_v4();
ALTER TABLE products ALTER COLUMN id SET DEFAULT uuid_generate_v4();
ALTER TABLE carts ALTER COLUMN id SET DEFAULT uuid_generate_v4();

INSERT INTO users(username, password)
VALUES
('user', 'user'),
('user1', 'user1'),
('user2', 'user2');

INSERT INTO products(name, price_rub, owner_id)
VALUES
('product1', 100000.25, (select id from users OFFSET (0) ROWS FETCH NEXT (1) ROWS ONLY)),
('product2', 50010.36, (select id from users OFFSET (0) ROWS FETCH NEXT (1) ROWS ONLY)),
('product3', 90000, (select id from users OFFSET (1) ROWS FETCH NEXT (1) ROWS ONLY));

INSERT INTO carts(product_id, user_id)
VALUES
((select id from products OFFSET (0) ROWS FETCH NEXT (1) ROWS ONLY), (select id from users OFFSET (2) ROWS FETCH NEXT (1) ROWS ONLY)),
((select id from products OFFSET (1) ROWS FETCH NEXT (1) ROWS ONLY), (select id from users OFFSET (2) ROWS FETCH NEXT (1) ROWS ONLY)),
((select id from products OFFSET (2) ROWS FETCH NEXT (1) ROWS ONLY), (select id from users OFFSET (0) ROWS FETCH NEXT (1) ROWS ONLY));
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
