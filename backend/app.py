from rag import ingest_documents
from router import route_query
from llm import generate_answer
from evaluator import evaluate_answer

# Build knowledge base (runs once on startup)
ingest_documents("docs")

while True:
    query = input("\nAsk a question (or 'exit'): ")
    if query.lower() == "exit":
        break

    decision = route_query(query)

    # Layer 2: Retrieval rejection
    if decision["route"] == "NO_ANSWER":
        print("\n❌", decision["reason"])
        continue

    # LLM generation
    answer = generate_answer(
        query=query,
        documents=decision["documents"],
        model_choice=decision["model"]
    )

    # Layer 3: Output evaluation
    evaluation = evaluate_answer(
        query=query,
        answer=answer,
        documents=decision["documents"]
    )

    if not evaluation["valid"]:
        print("\n⚠️ Answer rejected by evaluator")
        print("Reason:", evaluation["reason"])
        print("Confidence:", evaluation["confidence"])
        continue

    print(f"\n🟢 Confidence score: {evaluation['confidence']:.2f}")
    print("\n✅ Answer:\n", answer)