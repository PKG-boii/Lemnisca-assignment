from rag.ingest import ingest_documents

docs = ingest_documents("docs")

for d in docs:
    print(d["filename"], d["category"], d["num_chunks"])
