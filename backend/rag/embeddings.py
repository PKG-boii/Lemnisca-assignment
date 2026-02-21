from sentence_transformers import SentenceTransformer
import numpy as np

# Lightweight, fast, widely used
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> np.ndarray:
    """
    Convert text into a normalized vector embedding.
    """
    return _model.encode(text, normalize_embeddings=True)
