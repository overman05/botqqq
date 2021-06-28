import sqlite3
import config

con = sqlite3.connect(config.DB_NAME)


def create_user(id):
    cursor = con.cursor()
    cursor.execute("INSERT INTO user VALUES(?)", (id,))


def add_cell_to_user(user_id, cell_id):
    cursor = con.cursor()
    cursor.execute("INSERT INTO cells(user_id, id) VALUES(?,?)", (user_id, cell_id))
