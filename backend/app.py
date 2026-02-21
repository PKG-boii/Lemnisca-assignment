# app.py (TEMP TEST)
from rag import ingest_documents

docs = ingest_documents("docs")

for doc in docs:
    print(
        f"{doc['filename']} | "
        f"{doc['category']} | "
        f"chunks: {doc['num_chunks']}"
    )

# Print one sample chunk
print("\nSAMPLE CHUNK:\n")
print(docs[0]["chunks"][0][:500])
