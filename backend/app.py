from rag import ingest_documents
from router import route_query
from llm import generate_answer

# Build knowledge base
ingest_documents("docs")

while True:
    query = input("\nAsk a question (or 'exit'): ")
    if query.lower() == "exit":
        break

    decision = route_query(query)

    if decision["route"] == "NO_ANSWER":
        print("\n❌", decision["reason"])
        continue

    answer = generate_answer(
        query=query,
        documents=decision["documents"],
        model_choice=decision["model"]
    )

    print("\n✅ Answer:\n", answer)