import sqlite3
from sentence_transformers import SentenceTransformer


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("📥 Embedding modeli yükleniyor...")
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("docs/knowledge.txt", "r", encoding="utf-8") as file:
    text = file.read()

chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

print(f"📄 {len(chunks)} chunk bulundu.")

cursor.execute("DELETE FROM documents")

for chunk in chunks:
    embedding = model.encode(chunk).tolist()

    cursor.execute(
        """
        INSERT INTO documents (content, embedding)
        VALUES (?, ?)
        """,
        (chunk, str(embedding))
    )

conn.commit()
conn.close()


