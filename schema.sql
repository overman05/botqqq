CREATE TABLE user(id INTEGER PRIMARY KEY, tele_id TEXT NOT NULL);
CREATE TABLE cells(id INTEGER PRIMARY KEY, cell_id INTEGER, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES user(id));
CREATE TABLE phone(id INTEGER PRIMARY KEY, number INTEGER, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES user(id));