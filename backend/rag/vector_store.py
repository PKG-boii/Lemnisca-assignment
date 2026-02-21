import numpy as np
from .embeddings import embed_text

VECTOR_STORE = []

def reset_store():
    global VECTOR_STORE
    VECTOR_STORE = []

def add_chunk(text: str, source: str, category: str):
    embedding = embed_text(text)
    VECTOR_STORE.append({
        "embedding": embedding,
        "text": text,
        "source": source,
        "category": category
    })

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))  # normalized vectors → dot = cosine

def retrieve_top_k(query: str, k: int = 3):
    query_embedding = embed_text(query)

    scored = []
    for item in VECTOR_STORE:
        score = cosine_similarity(query_embedding, item["embedding"])
        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
    {**item, "score": score}
    for score, item in scored[:k]
]

