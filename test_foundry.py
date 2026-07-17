from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:54200/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="Phi-3-mini-4k-instruct-generic-gpu:2",
    messages=[
        {
            "role": "user",
            "content": "RAG nedir? Kısaca açıkla."
        }
    ],
    max_tokens=300
)

print(response.choices[0].message.content)