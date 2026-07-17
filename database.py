import sqlite3

DB_NAME = "database.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            embedding TEXT
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("✅ Database oluşturuldu.")
    




