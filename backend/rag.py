
import os
from utils import load_pdf, detect_doc_category
import tiktoken

def ingest_documents(docs_path="docs"):
    documents = []

    for filename in os.listdir(docs_path):
        if not filename.endswith(".pdf"):
            continue

        path = os.path.join(docs_path, filename)
        pdf = load_pdf(path)

        category = detect_doc_category(
            filename=filename,
            page_count=pdf["page_count"],
            preview_text=pdf["text"][:500]
        )

        config = CHUNKING_CONFIG[category]

        chunks = chunk_text(
            text=pdf["text"],
            chunk_size=config["chunk_size"],
            overlap=config["overlap"]
        )

        documents.append({
            "filename": filename,
            "category": category,
            "page_count": pdf["page_count"],
            "num_chunks": len(chunks),
            "chunks": chunks
        })

    return documents




#Different chunk for differrent categories of documents.


encoding = tiktoken.get_encoding("cl100k_base")

CHUNKING_CONFIG = {
    "REFERENCE": {
        "chunk_size": 250,
        "overlap": 25
    },
    "GUIDE": {
        "chunk_size": 450,
        "overlap": 75
    },
    "POLICY": {
        "chunk_size": 700,
        "overlap": 120
    },
    "TECHNICAL": {
        "chunk_size": 500,
        "overlap": 80
    },
    "INTERNAL_NOTES": {
        "chunk_size": 350,
        "overlap": 50
    },
    "ROADMAP_RELEASES": {
        "chunk_size": 400,
        "overlap": 60
    }
}


#Chunking function

def chunk_text(text: str, chunk_size: int, overlap: int):
    tokens = encoding.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)

        chunks.append(chunk_text)
        start += chunk_size - overlap

    return chunks


#Preventing prevents bad PDFs and short documents from ruining your chunking statistics and retrieval quality.

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

        config = CHUNKING_CONFIG[category]
        tokens = encoding.encode(text)

        if len(tokens) <= config["chunk_size"]:
            chunks = [text]
        else:
            chunks = chunk_text(
                text=text,
                chunk_size=config["chunk_size"],
                overlap=config["overlap"]
            )

        documents.append({
            "filename": filename,
            "category": category,
            "page_count": pdf["page_count"],
            "num_chunks": len(chunks),
            "chunks": chunks
        })

    return documents