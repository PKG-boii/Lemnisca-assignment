import os
import tiktoken
from utils import load_pdf, detect_doc_category

# ---------------- TOKENIZER ----------------

encoding = tiktoken.get_encoding("cl100k_base")

# ---------------- CHUNKING CONFIG ----------------

CHUNKING_CONFIG = {
    "REFERENCE": {"chunk_size": 250, "overlap": 25},
    "GUIDE": {"chunk_size": 450, "overlap": 75},
    "POLICY": {"chunk_size": 700, "overlap": 120},
    "TECHNICAL": {"chunk_size": 500, "overlap": 80},
    "INTERNAL_NOTES": {"chunk_size": 350, "overlap": 50},
    "ROADMAP_RELEASES": {"chunk_size": 400, "overlap": 60},
}

# ---------------- CHUNKING FUNCTION ----------------

def chunk_text(text: str, chunk_size: int, overlap: int):
    tokens = encoding.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunks.append(encoding.decode(chunk_tokens))
        start += chunk_size - overlap

    return chunks

# ---------------- DOCUMENT INGESTION ----------------

def ingest_documents(docs_path="docs"):
    documents = []

    for filename in os.listdir(docs_path):
        if not filename.endswith(".pdf"):
            continue

        path = os.path.join(docs_path, filename)
        pdf = load_pdf(path)

        text = pdf["text"].strip()
        if len(text) < 100:
            print(f"⚠️ Skipping low-text PDF: {filename}")
            continue

        category = detect_doc_category(
            filename=filename,
            page_count=pdf["page_count"],
            preview_text=text[:500]
        )

        cfg = CHUNKING_CONFIG[category]
        tokens = encoding.encode(text)

        # Avoid unnecessary chunking for short docs
        if len(tokens) <= cfg["chunk_size"]:
            chunks = [text]
        else:
            chunks = chunk_text(
                text=text,
                chunk_size=cfg["chunk_size"],
                overlap=cfg["overlap"]
            )

        documents.append({
            "filename": filename,
            "category": category,
            "page_count": pdf["page_count"],
            "num_chunks": len(chunks),
            "chunks": chunks
        })

    return documents
