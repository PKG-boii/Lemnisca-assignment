from rag import ingest_documents, retrieve_top_k

ingest_documents("docs")

query = "How do I reset my password?"
results = retrieve_top_k(query, k=3)

print("\nTop results:\n")
for r in results:
    print(r["source"], "→", r["category"])
    print(r["text"][:200])
    print("-----")
