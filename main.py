import time
from openai import OpenAI
from rag import search_documents


# ---------------------------------
# Project information
# ---------------------------------

PROJECT_NAME = "Burkan Local AI"
DEVELOPER = "Yusuf Burkan"
VERSION = "1.0.0"
SIMILARITY_THRESHOLD = 0.45


# ---------------------------------
# Foundry Local connection
# ---------------------------------

client = OpenAI(
    base_url="http://127.0.0.1:54200/v1",
    api_key="not-needed"
)


# ---------------------------------
# Welcome screen
# ---------------------------------

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


# ---------------------------------
# Main application loop
# ---------------------------------

while True:

    question = input(f"\n💬 {user_name}, ask a question: ").strip()

    if question.lower() in ["exit", "quit"]:
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

    context, similarity_score = search_documents(question)

    print("\n" + "=" * 55)
    print("📚 Retrieved Context")
    print("=" * 55)
    print(f"\n{context}")

    print(f"\n📈 Similarity Score : {similarity_score:.4f}")

    if similarity_score < SIMILARITY_THRESHOLD:
        print("\n⚠️ Relevant information could not be found.")
        print("The question may not exist in the local knowledge base.")

        response_time = time.time() - start_time
        print(f"\n⏱ Response time: {response_time:.2f} seconds")
        continue

    prompt = f"""
You are {PROJECT_NAME}, a local artificial intelligence assistant
developed by {DEVELOPER}.

Answer the user's question using only the supplied context.

Rules:
- Do not invent information.
- If the context is insufficient, state that clearly.
- Give a short and clear answer.
- Answer in the same language as the user's question.

Context:
{context}

Question:
{question}
"""

    try:
        response = client.chat.completions.create(
            model="Phi-3-mini-4k-instruct-generic-gpu:2",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=200,
            temperature=0.1
        )

        answer = response.choices[0].message.content

        print("\n" + "=" * 55)
        print(f"🤖 {PROJECT_NAME} Response")
        print("=" * 55)
        print(f"\n{answer}")

    except Exception as error:
        print("\n❌ The AI model could not generate a response.")
        print(f"Error: {error}")

    response_time = time.time() - start_time

    print(f"\n⏱ Response time: {response_time:.2f} seconds")
    print(f"🔢 Question number: {question_count}")