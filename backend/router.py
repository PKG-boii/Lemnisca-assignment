
from rag import retrieve_top_k

SIMILARITY_THRESHOLD = 0.4

# ---------------- MODEL ROUTER ----------------

def select_model(query: str, retrieved_docs: list):
    """
    Decide which model to use: CHEAP or EXPENSIVE
    """

    query_lower = query.lower()

    # 1️⃣ Reasoning keyword heuristic (NEW RULE)
    reasoning_keywords = ["why", "explain", "compare", "difference", "impact"]
    if any(k in query_lower for k in reasoning_keywords):
        return "EXPENSIVE"

    # 2️⃣ Query length heuristic
    if len(query.split()) > 20:
        return "EXPENSIVE"

    # 3️⃣ Document category heuristic
    categories = {doc["category"] for doc in retrieved_docs}

    technical_reasoning_keywords = [

        "how", "why", "explain", "architecture", "design",
        "flow", "working", "implementation"

    ]

    if (
        ("POLICY" in categories or "TECHNICAL" in categories)
        and any(k in query_lower for k in technical_reasoning_keywords)
    ):
        return "EXPENSIVE"

    # 4️⃣ Context size heuristic
    if len(retrieved_docs) > 5:
        return "EXPENSIVE"

    return "CHEAP"

# ---------------- RELEVANCE + MODEL ROUTER ----------------

def route_query(query: str):
    results = retrieve_top_k(query, k=3)

    if not results:
        return {
            "route": "NO_ANSWER",
            "reason": "No relevant documents found."
        }

    top_score = results[0]["score"]
    if top_score < SIMILARITY_THRESHOLD:
        return {
            "route": "NO_ANSWER",
            "reason": "Query is unrelated to the document corpus."
        }

    model = select_model(query, results)

    return {
        "route": "RAG",
        "model": model,
        "documents": results
    }