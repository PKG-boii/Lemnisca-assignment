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
    start = time.time()

    model = CHEAP_MODEL if model_choice == "CHEAP" else EXPENSIVE_MODEL

    context = "\n\n".join(d["text"] for d in documents)

    prompt = f"""
You are a ClearPath documentation assistant.
Answer ONLY using the documentation below.

Documentation:
{context}

Question:
{query}
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    latency_ms = int((time.time() - start) * 1000)

    return {
        "answer": response.choices[0].message.content.strip(),
        "model_used": model,
        "tokens_input": response.usage.prompt_tokens,
        "tokens_output": response.usage.completion_tokens,
        "latency_ms": latency_ms
    }