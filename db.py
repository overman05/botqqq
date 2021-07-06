import sqlite3
import config
import os


def create_db():
    os.system(f"cat {config.SQL_SCRIPT} | sqlite3 {config.DB_NAME}")


def init_db():
    if os.path.exists(config.DB_NAME):
        try:
            conn = sqlite3.connect(config.DB_NAME)
            cur = conn.cursor()
            cur.execute("SELECT * FROM user")
        except sqlite3.OperationalError:
            create_db()
        else:
            print("Database already exists")
    else:
        create_db()
        print("Database created")


def is_user_exist(user_id):
    with sqlite3.connect(config.DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user WHERE tele_id=?", (user_id,))
        uid = cursor.fetchone()
        if uid is None:
            return False
        else:
            return True


def create_user(tele_id):
    with sqlite3.connect(config.DB_NAME) as conn:
        cursor = conn.cursor()
        print("user created")
        cursor.execute("INSERT INTO user(tele_id) VALUES(?)", (tele_id,))
        conn.commit()


def add_cell_to_user(user_id, cell_id):
    with sqlite3.connect(config.DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user WHERE tele_id=?", (user_id,))
        uid = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO cells(user_id, cell_id) VALUES(?,?)", (uid, cell_id)
        )
        conn.commit()


def delete_cell_from_user(user_id, cell_id):
    with sqlite3.connect(config.DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user WHERE tele_id=?", (user_id,))
        uid = cursor.fetchone()[0]
        cursor.execute(
            "DELETE FROM cells WHERE user_id=? AND cell_id=?", (uid, cell_id)
        )
        conn.commit()


def get_user_cell(user_id):
    with sqlite3.connect(config.DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM user WHERE tele_id=?", (user_id,))
        uid = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM cells WHERE user_id=?", (uid,))
        return cursor.fetchall()


if __name__ == "__main__":
    init_db()
