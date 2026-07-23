# 🤖 Burkan Local AI

> A fully local Retrieval-Augmented Generation (RAG) application powered by SentenceTransformers, SQLite, and Microsoft's Phi-3 running through Foundry Local.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-Embeddings-orange)
![Foundry Local](https://img.shields.io/badge/LLM-Foundry_Local-purple)
![License](https://img.shields.io/badge/License-Educational-lightgrey)

---

## 📖 Overview

Burkan Local AI is a lightweight Retrieval-Augmented Generation (RAG) application that runs completely on your local machine.

Instead of sending data to cloud services, the application:

- Stores documents locally
- Generates semantic embeddings
- Retrieves the most relevant context
- Uses a locally running Phi-3 model to generate answers

Everything runs **100% locally** without requiring an external AI API.

---

## ✨ Features

- Fully Local RAG Pipeline
- SQLite Vector Storage
- SentenceTransformer Embeddings
- Cosine Similarity Retrieval
- Microsoft Phi-3 Integration
- Foundry Local Support
- Similarity Threshold Filtering
- Response Time Measurement
- Interactive CLI
- No Cloud API Required

---

## 🏗 System Architecture

```text
               +-----------------------+
               |   knowledge.txt       |
               +-----------+-----------+
                           |
                           v
              SentenceTransformer
                           |
                           v
                Embedding Generation
                           |
                           v
                   SQLite Database
                           |
                           v
                  Cosine Similarity
                           |
                           v
                 Relevant Context
                           |
                           v
                Phi-3 (Foundry Local)
                           |
                           v
                  Generated Response
```

---
## Project Structure

```text
LocalRAG/
├── docs/                     # PDF and TXT knowledge base
├── presentation/
│   └── Burkan Local AI Microsoft Summer School Project Presentation.pdf
├── database.py               # SQLite database operations
├── ingest.py                 # Document ingestion and embedding generation
├── rag.py                    # Retrieval and answer generation pipeline
├── main.py                   # Command-line application
├── test_foundry.py           # Foundry Local connection test
├── database.db               # Stored document chunks and embeddings
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore                # Git ignored files
```

## ⚙️ Requirements

- Python 3.10+
- Foundry Local
- Phi-3 Model
- macOS / Linux / Windows

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Ysfbrkan/Burkan-Local-RAG.git
cd Burkan-Local-RAG
```

Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📚 Generate the Knowledge Database

```bash
python ingest.py
```

This command automatically:

- Creates the SQLite database
- Creates the documents table
- Reads `docs/knowledge.txt`
- Splits the document into chunks
- Generates embeddings
- Stores everything locally

---

## 🤖 Start Foundry Local

Verify that your local model is available:

```bash
curl http://127.0.0.1:54200/v1/models
```

Current model:

```text
Phi-3-mini-4k-instruct-generic-gpu:2
```

---

## ▶️ Run

```bash
python main.py
```

---

## 💬 Example

```text
=======================================================
🤖 Burkan Local AI
👨‍💻 Developed by Yusuf Burkan
📦 Version: 1.0.0
📚 SQLite + SentenceTransformers + Foundry Local
=======================================================

👤 What is your name?

Yusuf

💬 Yusuf, ask a question:

What is RAG?

🤖 RAG (Retrieval-Augmented Generation) combines
semantic search with language models by retrieving
relevant documents before generating an answer.
```

---

## ✅ Features Demonstrated

- Local semantic search
- Embedding generation
- Context retrieval
- Local LLM inference
- Interactive command-line interface
- Offline execution
- Zero cloud dependency

---

## 🛠 Technologies

- Python
- SQLite
- SentenceTransformers
- Scikit-learn
- OpenAI SDK
- Foundry Local
- Phi-3 Mini
- NumPy

---

## 🧪 Clean Installation Test

The project has been successfully tested using a completely fresh installation.

Verified steps:

- Repository cloned
- Virtual environment created
- Dependencies installed
- Database automatically created
- Embeddings generated
- Local model connected
- Application launched successfully

---

## 🚀 Roadmap

- [x] Local RAG Pipeline
- [x] SQLite Storage
- [x] SentenceTransformer Embeddings
- [x] Cosine Similarity Search
- [x] Foundry Local Integration
- [x] Interactive CLI
- [x] Automatic Database Initialization
- [x] Clean Installation Support
- [x] Source Attribution
- [x] Top-K Retrieval
- [x] Multiple Document Support
- [x] PDF Support
- [ ] GitHub Actions
- [ ] Unit Tests
- [ ] Performance Benchmark
- [ ] Docker Support

---

## 👨‍💻 Author

**Yusuf Burkan**

Management Student @ Boğaziçi University

Interested in

- Artificial Intelligence
- Product Management
- Machine Learning
- Large Language Models
- Retrieval-Augmented Generation

GitHub

**https://github.com/Ysfbrkan**

---

## 📄 License
