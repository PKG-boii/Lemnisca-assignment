from rag import ingest_documents
from router import route_query
from llm import generate_answer
from evaluator import evaluate_answer

# Build knowledge base once
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

    # LLM call (now returns metadata)
    result = generate_answer(
        query=query,
        documents=decision["documents"],
        model_choice=decision["model"]
    )

    answer = result["answer"]

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

    # Logging (assignment requirement)
    log_entry = {
        "query": query,
        "classification": decision["model"],
        "model_used": result["model_used"],
        "tokens_input": result["tokens_input"],
        "tokens_output": result["tokens_output"],
        "latency_ms": result["latency_ms"]
    }

    print("\n📊 ROUTING LOG")
    print(log_entry)

    print(f"\n🟢 Confidence score: {evaluation['confidence']:.2f}")
    print("\n✅ Answer:\n", answer)