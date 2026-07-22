import sqlite3


DATABASE_NAME = "database.db"


def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'unknown',
            chunk_index INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    cursor.execute("PRAGMA table_info(documents)")
    existing_columns = {column[1] for column in cursor.fetchall()}

    if "source" not in existing_columns:
        cursor.execute(
            """
            ALTER TABLE documents
            ADD COLUMN source TEXT NOT NULL DEFAULT 'unknown'
            """
        )

    if "chunk_index" not in existing_columns:
        cursor.execute(
            """
            ALTER TABLE documents
            ADD COLUMN chunk_index INTEGER NOT NULL DEFAULT 0
            """
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("✅ Database oluşturuldu.")
