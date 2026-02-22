import streamlit as st
import time

from rag import ingest_documents
from router import route_query
from llm import generate_answer
from evaluator import evaluate_answer

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="ClearPath RAG Assistant",
    layout="centered"
)

st.title("📘 ClearPath Documentation Assistant")
st.caption("RAG + Routing + Evaluation (Assignment Interface)")

# ---------------------------------------------------------
# Initialize knowledge base ONCE
# ---------------------------------------------------------
if "kb_loaded" not in st.session_state:
    with st.spinner("📚 Indexing documents..."):
        ingest_documents("docs")
    st.session_state.kb_loaded = True
    st.success("Knowledge base ready")

# ---------------------------------------------------------
# Query input
# ---------------------------------------------------------
query = st.text_input(
    "Ask a question about ClearPath documentation:",
    placeholder="e.g. How do I reset my password?"
)

if not query:
    st.stop()

# ---------------------------------------------------------
# Handle query (routing + timing)
# ---------------------------------------------------------
with st.spinner("🤖 Thinking..."):
    start_time = time.time()
    decision = route_query(query)

# ---------------------------------------------------------
# No-answer case
# ---------------------------------------------------------
if decision["route"] == "NO_ANSWER":
    st.error(decision["reason"])
    st.stop()

# ---------------------------------------------------------
# Generate answer
# ---------------------------------------------------------
result = generate_answer(
    query=query,
    documents=decision["documents"],
    model_choice=decision["model"]
)

latency_ms = int((time.time() - start_time) * 1000)
answer = result["answer"]
model_used = result["model_used"]
tokens_in = result["tokens_input"]
tokens_out = result["tokens_output"]
latency_ms = result["latency_ms"]


# ---------------------------------------------------------
# Evaluate answer (Layer 3)
# ---------------------------------------------------------
evaluation = evaluate_answer(
    query=query,
    answer=answer,
    documents=decision["documents"]
)

# ---------------------------------------------------------
# Display answer
# ---------------------------------------------------------
st.subheader("✅ Answer")
st.write(answer)

# ---------------------------------------------------------
# Confidence score
# ---------------------------------------------------------
st.subheader("🟢 Confidence score")
st.progress(evaluation["confidence"])
st.write(f"{evaluation['confidence']:.2f}")

# ---------------------------------------------------------
# Evaluation warnings
# ---------------------------------------------------------
issues = evaluation.get("issues", [])

if issues:
    st.subheader("⚠️ Evaluation warnings")
    for issue in issues:
        st.warning(issue)

# ---------------------------------------------------------
# Debug / routing panel (Assignment requirement)
# ---------------------------------------------------------
with st.expander("📊 Routing & Debug Info"):
    st.json({
        "query": query,
        "classification": decision["model"],
        "model_used": model_used,
        "tokens_input": tokens_in,
        "tokens_output": tokens_out,
        "latency_ms": latency_ms
    })