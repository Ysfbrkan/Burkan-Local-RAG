# Burkan Local AI

A lightweight local Retrieval-Augmented Generation (RAG) application developed by Yusuf Burkan.

The project retrieves relevant information from a local SQLite database using sentence embeddings and generates answers with a locally running Phi-3 model through Foundry Local.

## Features

- Local document retrieval
- SentenceTransformer embeddings
- Cosine similarity search
- SQLite vector storage
- Phi-3 integration through Foundry Local
- Similarity score display
- Response time measurement
- Low-similarity protection
- Continuous question-answer loop
- Local execution without a cloud API key

## Technologies

- Python
- SQLite
- SentenceTransformers
- NumPy
- OpenAI-compatible API
- Microsoft Foundry Local
- Phi-3 Mini

## Project Structure

```text
LocalRAG/
├── docs/
│   └── knowledge.txt
├── database.py
├── ingest.py
├── rag.py
├── main.py
├── database.db
├── requirements.txt
├── README.md
├── .gitignore
└── .env