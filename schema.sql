CREATE TABLE user
(
    id INTEGER PRIMARY KEY
);
CREATE TABLE cells
(
    id INTEGER PRIMARY KEY,
    user_key TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES user(id)
);
