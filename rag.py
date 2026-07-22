import ast
import sqlite3

import numpy as np
from sentence_transformers import SentenceTransformer


DB_NAME = "database.db"
MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_TOP_K = 3

print("📥 Embedding modeli yükleniyor...")
model = SentenceTransformer(MODEL_NAME)


def search_documents(question: str, top_k: int = DEFAULT_TOP_K):
    """
    Return the most relevant document chunks for a question.

    Args:
        question: User question.
        top_k: Maximum number of chunks to return.

    Returns:
        A list of dictionaries containing content, score, source and chunk id.
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(
    """
    SELECT id, content, embedding, source, chunk_index
    FROM documents
    """
)
        rows = cursor.fetchall()

        if not rows:
            raise ValueError("Veritabanında aranacak belge bulunamadı.")

        question_embedding = model.encode(question)

        results = []

        for chunk_id, content, embedding_str, source, chunk_index in rows:
            embedding = np.array(
                ast.literal_eval(embedding_str),
                dtype=np.float32
            )

            denominator = (
                np.linalg.norm(question_embedding)
                * np.linalg.norm(embedding)
            )

            if denominator == 0:
                similarity = 0.0
            else:
                similarity = float(
                    np.dot(question_embedding, embedding) / denominator
                )

            results.append(
    {
        "chunk_id": chunk_id,
        "chunk_index": chunk_index,
        "content": content,
        "score": similarity,
        "source": source,
    }
)

        results.sort(key=lambda item: item["score"], reverse=True)

        return results[: min(top_k, len(results))]

    finally:
        conn.close()


if __name__ == "__main__":
    question = input("💬 Sorunuzu yazın: ").strip()

    results = search_documents(question, top_k=3)

    print("\n" + "=" * 55)
    print("📚 En alakalı bilgiler")
    print("=" * 55)

    for index, result in enumerate(results, start=1):
        print(f"\n#{index}")
        print(f"📄 Source: {result['source']}")
        print(f"🧩 Chunk ID: {result['chunk_id']}")
        print(f"📈 Similarity Score: {result['score']:.4f}")
        print(f"\n{result['content']}")