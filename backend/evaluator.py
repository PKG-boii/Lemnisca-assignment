# backend/evaluator.py

def evaluate_answer(query: str, answer: str, documents: list):
    """
    Layer 3: Output Evaluator
    - Generic quality checks
    - Domain-specific hallucination prevention
    """

    # ---------- Generic check: empty / too short ----------
    if not answer or len(answer.strip()) < 30:
        return {
            "valid": False,
            "confidence": 0.0,
            "reason": "Answer too short or empty"
        }

    # ---------- Generic check: grounding ----------
    context_text = " ".join(doc["text"].lower() for doc in documents)
    grounding_hits = sum(
        1 for word in answer.lower().split()
        if word in context_text
    )

    if grounding_hits < 5:
        return {
            "valid": False,
            "confidence": 0.3,
            "reason": "Answer not sufficiently grounded in retrieved documents"
        }

    # ======================================================
    # DOMAIN-SPECIFIC CHECK: Unsupported feature / claim
    # ======================================================

    claim_keywords = [
        "supports", "includes", "available", "enabled",
        "plan", "pricing", "cost", "limit", "maximum",
        "requires", "allowed", "restricted", "policy"
    ]

    answer_lower = answer.lower()

    # If the answer is making product / policy claims
    if any(k in answer_lower for k in claim_keywords):
        unsupported = [
            k for k in claim_keywords
            if k in answer_lower and k not in context_text
        ]

        if unsupported:
            return {
                "valid": False,
                "confidence": 0.25,
                "reason": (
                    "Answer contains unsupported product or policy claims: "
                    + ", ".join(unsupported)
                )
            }

    # ---------- Confidence score ----------
    confidence = min(1.0, grounding_hits / 20)

    return {
        "valid": True,
        "confidence": confidence
    }