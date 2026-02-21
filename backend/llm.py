import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()  


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CHEAP_MODEL = "llama-3.1-8b-instant"
EXPENSIVE_MODEL = "llama-3.1-8b-instant"

def generate_answer(query: str, documents: list, model_choice: str):
    """
    Generate an answer using retrieved documents.
    """

    # Build context from retrieved chunks
    context = "\n\n".join(
        f"[Source: {doc['source']}]\n{doc['text']}"
        for doc in documents
    )

    prompt = f"""
You are an assistant answering questions using ONLY the provided context.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{query}

Answer:
"""

    model = CHEAP_MODEL if model_choice == "CHEAP" else EXPENSIVE_MODEL

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()