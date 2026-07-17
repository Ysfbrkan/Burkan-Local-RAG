import sqlite3
import ast
import numpy as np
from sentence_transformers import SentenceTransformer


print("📥 Embedding modeli yükleniyor...")
model = SentenceTransformer("all-MiniLM-L6-v2")


def search_documents(question: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    question_embedding = model.encode(question)

    cursor.execute("SELECT content, embedding FROM documents")
    rows = cursor.fetchall()

    if not rows:
        conn.close()
        raise ValueError("Veritabanında aranacak belge bulunamadı.")

    best_score = -1.0
    best_content = ""

    for content, embedding_str in rows:
        embedding = np.array(ast.literal_eval(embedding_str))

        similarity = np.dot(question_embedding, embedding)
        similarity /= (
            np.linalg.norm(question_embedding)
            * np.linalg.norm(embedding)
        )

        if similarity > best_score:
            best_score = float(similarity)
            best_content = content

    conn.close()

    return best_content, best_score


if __name__ == "__main__":
    question = input("💬 Sorunuzu yazın: ")

    best_content, best_score = search_documents(question)

    print("\n==============================")
    print("📚 En alakalı bilgi")
    print("==============================\n")

    print(best_content)
    print(f"\n📈 Similarity Score: {best_score:.4f}")