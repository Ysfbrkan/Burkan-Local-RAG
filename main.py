import time

from openai import OpenAI
from rag import search_documents


PROJECT_NAME = "Burkan Local AI"
DEVELOPER = "Yusuf Burkan"
VERSION = "1.1.0"

SIMILARITY_THRESHOLD = 0.30
TOP_K = 3

MODEL_NAME = "Phi-3-mini-4k-instruct-generic-gpu:2"
BASE_URL = "http://127.0.0.1:49540/v1"

client = OpenAI(
    base_url=BASE_URL,
    api_key="not-needed"
)


def build_context(results):
    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"""
Source {index}
File: {result['source']}
Chunk ID: {result['chunk_id']}
Similarity Score: {result['score']:.4f}

Content:
{result['content']}
""".strip()
        )

    return "\n\n---\n\n".join(context_parts)


def print_retrieved_sources(results):
    print("\n" + "=" * 55)
    print("📚 Retrieved Sources")
    print("=" * 55)

    for index, result in enumerate(results, start=1):
        print(f"\n#{index}")
        print(f"📄 Source: {result['source']}")
        print(f"🧩 Chunk ID: {result['chunk_id']}")
        print(f"📈 Similarity Score: {result['score']:.4f}")
        print(f"📝 Preview: {result['content'][:180]}...")


print("\n" + "=" * 55)
print(f"🤖 {PROJECT_NAME}")
print(f"👨‍💻 Developed by {DEVELOPER}")
print(f"📦 Version: {VERSION}")
print("📚 SQLite + SentenceTransformers + Foundry Local")
print("=" * 55)

user_name = input("\n👤 What is your name? ").strip()

if not user_name:
    user_name = "User"

print(f"\n👋 Welcome, {user_name}!")
print("You can ask questions based on the local knowledge base.")
print("Type 'exit' to close the application.")

question_count = 0


while True:
    question = input(f"\n💬 {user_name}, ask a question: ").strip()

    if question.lower() in {"exit", "quit"}:
        print("\n" + "=" * 55)
        print(f"👋 Goodbye, {user_name}!")
        print(f"📊 Total questions asked: {question_count}")
        print(f"🤖 Thank you for using {PROJECT_NAME}.")
        print("=" * 55)
        break

    if not question:
        print("⚠️ Please enter a question.")
        continue

    question_count += 1
    start_time = time.time()

    try:
        results = search_documents(question, top_k=TOP_K)
    except Exception as error:
        print("\n❌ The knowledge base could not be searched.")
        print(f"Error: {error}")
        continue

    best_score = results[0]["score"]

    print_retrieved_sources(results)

    if best_score < SIMILARITY_THRESHOLD:
        print("\n⚠️ I could not find the answer in the local knowledge base.")

        response_time = time.time() - start_time
        print(f"\n⏱ Response time: {response_time:.2f} seconds")
        continue

    context = build_context(results)

    prompt = f"""
You are {PROJECT_NAME}, a local artificial intelligence assistant
developed by {DEVELOPER}.

Answer the user's question using only the supplied context.

Rules:
- Do not invent information.
- Use only information contained in the context.
- If the answer is not contained in the context, say exactly:
  I could not find the answer in the local knowledge base.
- Give a short and clear answer.
- Answer in the same language as the user's question.
- Cite only the sources actually used.
- At the end, mention the relevant source numbers in this format:
  Sources: [1], [2]

Context:
{context}

Question:
{question}
""".strip()

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=250,
            temperature=0.1
        )

        answer = response.choices[0].message.content

        print("\n" + "=" * 55)
        print(f"🤖 {PROJECT_NAME} Response")
        print("=" * 55)
        print(f"\n{answer}")

        print("\n" + "=" * 55)
        print("📎 Source Attribution")
        print("=" * 55)

        for index, result in enumerate(results, start=1):
            print(
                f"[{index}] {result['source']} "
                f"| Chunk {result['chunk_id']} "
                f"| Score {result['score']:.4f}"
            )

    except Exception as error:
        print("\n❌ The AI model could not generate a response.")
        print(f"Error: {error}")

    response_time = time.time() - start_time

    print(f"\n⏱ Response time: {response_time:.2f} seconds")
    print(f"🔢 Question number: {question_count}")
