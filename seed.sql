-- CREATE DATABASE groceries;

DROP TABLE IF EXISTS lists_items;
DROP TABLE IF EXISTS alleys_orders;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS alleys;
DROP TABLE IF EXISTS lists;

CREATE TABLE alleys (
    name TEXT NOT NULL
);

CREATE TABLE alleys_orders (
    alley_id INT NOT NULL,
    "order" INT NOT NULL
);

CREATE TABLE products (
    name TEXT NOT NULL,
    alley_id INT NULL
);

CREATE TABLE lists (
    "date" DATE NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE lists_products (
    list_id INT NOT NULL,
    products_id INT NOT NULL
);