import os
from dotenv import load_dotenv
from groq import Groq
import time
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

load_dotenv()  


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CHEAP_MODEL = "llama-3.1-8b-instant"
EXPENSIVE_MODEL = "llama-3.1-8b-instant"

def generate_answer(query, documents, model_choice):
    MODEL_MAP = {
        "CHEAP": "llama-3.1-8b-instant",
        "EXPENSIVE": "llama-3.1-8b-instant"  # free-tier fallback
    }

    model = MODEL_MAP[model_choice]

    context = "\n".join(doc["text"] for doc in documents)
    prompt = f"""
Use the following documentation to answer the question.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{query}
"""

    tokens_input = len(encoding.encode(prompt))

    start = time.time()

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    latency_ms = int((time.time() - start) * 1000)

    answer = response.choices[0].message.content
    tokens_output = len(encoding.encode(answer))

    return {
        "answer": answer,
        "model_used": model,
        "tokens_input": tokens_input,
        "tokens_output": tokens_output,
        "latency_ms": latency_ms
    }