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
    "order" INT NOT NULL,
    CONSTRAINT fk_alleys_orders_alley_id FOREIGN KEY (alley_id)
    REFERENCES alleys(id)
);

CREATE TABLE items (
    name TEXT NOT NULL,
    alley_id INT NULL,
    CONSTRAINT fk_items_alley_id FOREIGN KEY (alley_id)
    REFERENCES alleys(id)
);

CREATE TABLE lists (
    "date" DATE NOT NULL,
    archived BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE lists_items (
    list_id INT NOT NULL,
    item_id INT NOT NULL,
    CONSTRAINT fk_lists_items_list_id FOREIGN KEY (list_id)
    REFERENCES lists(id),
    CONSTRAINT fk_lists_items_item_id FOREIGN KEY (item_id)
    REFERENCES items(id)
);