
import os
from utils import load_pdf, detect_doc_category

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

        documents.append({
            "filename": filename,
            "category": category,
            "page_count": pdf["page_count"],
            "text": pdf["text"]  # keep for next steps
        })

    return documents
