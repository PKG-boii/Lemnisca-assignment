README = """
# ClearPath RAG Assistant

This project implements a Retrieval-Augmented Generation (RAG) system over internal ClearPath documentation. It includes document ingestion, rule-based document classification, category-aware chunking, semantic retrieval, query routing between multiple Groq-hosted LLMs, an answer evaluation layer, and a Streamlit-based user interface.

------------------------------------------------------------
HOW TO RUN THE PROJECT LOCALLY
------------------------------------------------------------

Prerequisites:
- Python 3.10 or higher
- pip
- A valid Groq API key

Setup Steps:

1. Clone the repository and move into the backend folder:
   git clone <your-repo-url>
   cd backend

2. (Optional but recommended) Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate        # Windows: venv\\Scripts\\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Create a .env file inside the backend directory:
   GROQ_API_KEY=your_groq_api_key_here

5. Run the Streamlit application:
   streamlit run streamlit_app.py

The application will be available at:
http://localhost:8501

On first run, all documents inside the docs/ directory are ingested, classified, chunked, and embedded. This happens once per session.

------------------------------------------------------------
GROQ MODELS AND ENVIRONMENT CONFIGURATION
------------------------------------------------------------

The system uses two Groq-hosted LLMs with a rule-based router:

- Cheap model: llama-3.1-8b-instant
  Used for simple, factual, and short queries.

- Expensive model: llama-3.1-70b-versatile
  Used for policy, technical, or reasoning-heavy queries.

Routing decisions are based on:
- Query intent (reasoning keywords)
- Query length
- Retrieved document categories
- Number of retrieved chunks

Environment variables:
- GROQ_API_KEY (required)

------------------------------------------------------------
BONUS CHALLENGES ATTEMPTED
------------------------------------------------------------


------------------------------------------------------------
KNOWN ISSUES AND LIMITATIONS
------------------------------------------------------------

- Answer absence detection:
  The system cannot perfectly detect when information is completely missing from the document corpus. Semantic similarity may retrieve loosely related chunks even when no direct answer exists.

- Heuristic routing limitations:
  The router is rule-based and may misclassify simple queries as complex due to document category heuristics.

- In-memory vector store:
  Embeddings are stored in memory and rebuilt on restart. This is sufficient for the assignment but not suitable for production-scale systems.

- Evaluator heuristics:
  The evaluation layer relies on heuristic checks rather than deep semantic validation, which may result in false positives or negatives in edge cases.

