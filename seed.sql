-- CREATE DATABASE groceries;

DROP TABLE IF EXISTS lists_items;
DROP TABLE IF EXISTS alleys_orders;
DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS alleys;
DROP TABLE IF EXISTS lists;
DROP TABLE IF EXISTS meals;

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

CREATE TABLE meals (
    day INT NOT NULL,
    day_part TEXT NOT NULL,
    meal TEXT NULL
)

INSERT INTO meals (day, day_part, meal) 
VALUES 
(0, 'LUNCH', NULL),
(0, 'DINNER', NULL),
(1, 'LUNCH', NULL),
(1, 'DINNER', NULL),
(2, 'LUNCH', NULL),
(2, 'DINNER', NULL),
(3, 'LUNCH', NULL),
(3, 'DINNER', NULL),
(4, 'LUNCH', NULL),
(4, 'DINNER', NULL),
(5, 'LUNCH', NULL),
(5, 'DINNER', NULL),
(6, 'LUNCH', NULL),
(6, 'DINNER', NULL);