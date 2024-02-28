CREATE TABLE inputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    input TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    category TEXT NOT NULL
);

CREATE TABLE category_tags (
    input_id INTEGER NOT NULL,
    cat_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(cat_id) REFERENCES categories(id),
    FOREIGN KEY(input_id) REFERENCES inputs(id)
);

CREATE TABLE input_tags (
    item_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(tag_id) REFERENCES inputs(id),
    FOREIGN KEY(item_id) REFERENCES inputs(id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);