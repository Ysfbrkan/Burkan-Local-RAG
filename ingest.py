
import sqlite3
from pathlib import Path

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from database import create_database


DATABASE_NAME = "database.db"
DOCS_DIRECTORY = Path("docs")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

SUPPORTED_EXTENSIONS = {".txt", ".pdf"}

CHUNK_SIZE = 700
CHUNK_OVERLAP = 100


def read_txt(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def read_pdf(file_path: Path) -> str:
    reader = PdfReader(file_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            pages.append(
                f"[Page {page_number}]\n{page_text.strip()}"
            )

    return "\n\n".join(pages)


def read_document(file_path: Path) -> str:
    extension = file_path.suffix.lower()

    if extension == ".txt":
        return read_txt(file_path)

    if extension == ".pdf":
        return read_pdf(file_path)

    raise ValueError(f"Unsupported file type: {extension}")


def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP
):
    clean_text = " ".join(text.split())

    if not clean_text:
        return []

    chunks = []
    start = 0

    while start < len(clean_text):
        end = start + chunk_size
        chunk = clean_text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(clean_text):
            break

        start = end - overlap

    return chunks


def find_documents():
    DOCS_DIRECTORY.mkdir(parents=True, exist_ok=True)

    return sorted(
        file_path
        for file_path in DOCS_DIRECTORY.rglob("*")
        if (
            file_path.is_file()
            and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
        )
    )


def ingest_documents():
    create_database()

    documents = find_documents()

    if not documents:
        print("⚠️ docs/ klasöründe TXT veya PDF bulunamadı.")
        return

    print("📥 Embedding modeli yükleniyor...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM documents")

        total_chunks = 0
        successful_files = 0

        for file_path in documents:
            print(f"\n📄 İşleniyor: {file_path}")

            try:
                text = read_document(file_path)
            except Exception as error:
                print(f"❌ Dosya okunamadı: {error}")
                continue

            chunks = split_text(text)

            if not chunks:
                print("⚠️ Bu dosyada okunabilir metin bulunamadı.")
                continue

            embeddings = model.encode(
                chunks,
                show_progress_bar=False
            )

            for chunk_index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings),
                start=1
            ):
                cursor.execute(
                    """
                    INSERT INTO documents (
                        content,
                        embedding,
                        source,
                        chunk_index
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        chunk,
                        str(embedding.tolist()),
                        str(file_path),
                        chunk_index
                    )
                )

            total_chunks += len(chunks)
            successful_files += 1

            print(f"✅ {len(chunks)} chunk oluşturuldu.")

        conn.commit()

        print("\n" + "=" * 55)
        print("✅ Ingestion tamamlandı.")
        print(f"📚 Başarılı dosya sayısı: {successful_files}")
        print(f"🧩 Toplam chunk sayısı: {total_chunks}")
        print("=" * 55)

    finally:
        conn.close()


if __name__ == "__main__":
    ingest_documents()
