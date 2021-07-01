import sqlite3
import config
import os


def init_db():
    if os.path.exists(config.DB_NAME):
        print("Database already exist")

    else:
        os.system(f"cat {config.SQL_SCRIPT} | sqlite3 {config.DB_NAME}")


class DB:
    def create_user(self, tele_id):
        with sqlite3.connect(config.DB_NAME) as conn:
            cursor = conn.cursor()
            print("user created")
            cursor.execute("INSERT INTO user(tele_id) VALUES(?)", (tele_id,))
            conn.commit()

    def add_cell_to_user(self, user_id, cell_id):
        with sqlite3.connect(config.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM user WHERE tele_id=?", (user_id,))
            uid = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO cells(user_id, cell_id) VALUES(?,?)", (uid, cell_id)
            )
            conn.commit()

    def delete_cell_from_user(self, user_id, cell_id):
        with sqlite3.connect(config.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM user WHERE tele_id=?", (user_id,))
            uid = cursor.fetchone()[0]
            cursor.execute(
                "DELETE FROM cells WHERE user_id=? AND cell_id=?", (uid, cell_id)
            )
            conn.commit()

    def get_user_cell(self, user_id):
        with sqlite3.connect(config.DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM user WHERE tele_id=?", (user_id,))
            uid = cursor.fetchone()[0]
            cursor.execute("SELECT * FROM cells WHERE user_id=?", (uid,))
            return cursor.fetchall()


if __name__ == "__main__":
    init_db()
