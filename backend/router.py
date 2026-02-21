from rag import retrieve_top_k

# Tuneable threshold
SIMILARITY_THRESHOLD = 0.4

def route_query(query: str):
    """
    Decide how the query should be handled.
    Returns a routing decision dict.
    """

    # 1️⃣ Retrieve top chunks
    results = retrieve_top_k(query, k=3)

    # 2️⃣ If nothing was retrieved
    if not results:
        return {
            "route": "NO_ANSWER",
            "reason": "No relevant documents found."
        }

    # 3️⃣ Check similarity score of best match
    top_score = results[0]["score"]

    if top_score < SIMILARITY_THRESHOLD:
        return {
            "route": "NO_ANSWER",
            "reason": "Query is unrelated to the document corpus."
        }

    # 4️⃣ Otherwise, use RAG
    return {
        "route": "RAG",
        "documents": results
    }