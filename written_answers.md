Chunking Stratergy ->

Before implementing chunking, I first designed a document classification system because not all documents in the corpus serve the same purpose. The dataset contained a mix of FAQs, guides, policies, technical documentation, internal notes, and roadmap-related files. Treating all of these uniformly would lead to either over-chunking simple documents or under-chunking dense ones. To address this, I classified documents using a rule-based approach that combines filename heuristics, page count, and content keywords. For example, files containing terms like policy, handbook, or privacy are classified as POLICY documents, while files with API, webhook, or architecture are classified as TECHNICAL. This lightweight approach was deterministic, transparent, and sufficient for this domain.

Once documents were categorized, I applied category-specific chunking strategies. Instead of using a single chunk size across the corpus, I tuned chunk sizes and overlaps based on document type. Reference documents and FAQs use smaller chunks to preserve precision for short, factual queries. Guides and tutorials use medium-sized chunks to maintain step-by-step coherence. Policy and technical documents use larger chunks with higher overlap to avoid losing important contextual dependencies across sections.

Chunking is done at the token level rather than character or sentence level, using a tokenizer consistent with the LLM. Overlap is intentionally added to reduce context fragmentation at chunk boundaries. This approach balances retrieval accuracy, context completeness, and token efficiency, and significantly improves retrieval quality compared to a one-size-fits-all chunking strategy. 


Domain specfic check->
In this project, the domain-specific check I implemented is an Unsupported Product or Policy Claim check. After the model generates an answer, the evaluator verifies whether the answer introduces features, plans, or policy details that are not present in the retrieved documentation. If the answer claims something that cannot be grounded in the available product or policy documents, it is flagged as a potential hallucination. This check is important for a product-documentation domain because incorrect claims about features or policies can mislead users and cause real issues, even if the answer sounds confident.


Q1)
Ans)
The router classifies queries as simple (CHEAP model) or complex (EXPENSIVE model) using a deterministic, rule-based approach. The first rule checks for reasoning-oriented keywords such as why, explain, compare, difference, and impact. These keywords typically indicate analytical or explanatory queries that require multi-step reasoning, so they are routed to the expensive model.

The second rule uses query length as a proxy for complexity. Queries longer than 20 words are assumed to require broader context or synthesis and are therefore treated as complex.

Next, the router examines the categories of the top retrieved documents. If any document belongs to the POLICY or TECHNICAL category, the query is classified as complex, since these domains are more error-sensitive and often require precise interpretation.

Finally, the router considers context size. If more than two relevant chunks are retrieved, the query is assumed to involve aggregation across documents, which benefits from a stronger model.

I drew the boundary here to optimize for cost-efficiency while maintaining safety and accuracy, especially for policy and technical queries where hallucinations are more risky.

One misclassification example was the query “Who is the backend team lead?”. Although the intent was simple, it was routed as complex because the retrieved document category triggered the POLICY/TECHNICAL rule. This highlights a limitation where document type outweighs user intent.

To improve the router without using an LLM, I would add intent-based heuristics (e.g., detecting factoid questions), use weighted scoring instead of hard rules, and tune thresholds using real query distribution data.


Q2)
Ans)
One case where the RAG pipeline struggled was the query:
“Does the Free plan support biometric login?”

In this case, the system either retrieved low-relevance FAQ chunks or, in some runs, returned no sufficiently relevant chunks, causing the router to treat the query as unrelated to the corpus.

The retrieved chunks mostly came from Account Management FAQ and Pricing-related documents, but none of them explicitly mentioned biometric login. Since embeddings rely on semantic similarity, terms like login and account loosely matched authentication-related sections, even though biometric login is not a documented feature. As a result, similarity scores were low and the evaluator later flagged the answer as unsupported.

The retrieval failed primarily because the information does not exist in the documentation, not because of a bug in the embedding model. However, the system still attempted retrieval due to partial semantic overlap between authentication concepts.

What would fix this is a combination of improvements. First, adding stronger negative or absence detection, such as checking whether a feature is ever mentioned across the corpus before answering. Second, tightening the similarity threshold or requiring multiple high-confidence chunks before proceeding would reduce false retrievals. Finally, metadata-aware filtering (for example, checking plan-level feature documents explicitly) would help avoid pulling irrelevant chunks for unsupported features.

This case highlighted why retrieval confidence and post-answer evaluation are critical, especially for product and policy-related questions.


Q3)
Ans)
If this system handled 5,000 queries per day, I would estimate token usage by separating traffic between the CHEAP and EXPENSIVE models based on routing behavior. In my current setup, roughly 70% of queries are simple and routed to the cheap model, while 30% are complex and routed to the expensive model.

For a typical CHEAP-model query, the average prompt (retrieved chunks + question) is around 600 input tokens, and the response averages 100 output tokens, for about 700 tokens per query.
So daily usage for the cheap model would be:
5,000 × 70% × 700 ≈ 2.45 million tokens/day.

For the EXPENSIVE model, prompts are larger due to more context, averaging around 1,200 input tokens and 150 output tokens, or roughly 1,350 tokens per query.
So daily usage here would be:
5,000 × 30% × 1,350 ≈ 2.0 million tokens/day.

The biggest cost driver is clearly the expensive model, not just because of its higher per-token cost, but because policy and technical queries often require more context and longer prompts.

The single highest-ROI change to reduce cost without hurting quality would be more aggressive routing, especially for simple factual queries that currently get escalated due to document category heuristics. Improving intent detection would reduce unnecessary expensive-model calls.

An optimization I would avoid is aggressively truncating context to save tokens. While it reduces cost, it significantly increases the risk of incomplete or misleading answers, especially for policy and technical queries, which is worse than slightly higher inference cost.


Q4)
Ans)
The most significant flaw in my system lies in the answer evaluation layer, specifically in how rigid evaluation metrics can incorrectly penalize valid responses. Initially, I implemented an answer-length check that rejected responses below a fixed token threshold. The reasoning behind this was that extremely short answers often indicate low-quality or incomplete responses. However, this assumption does not always hold.

For example, for the query “Who is the frontend team lead?”, the correct answer may simply be a single name. In this case, the system generated a correct but short response, which was incorrectly flagged as invalid due to the length constraint. This demonstrated that answer length alone is not a reliable proxy for answer quality. As a result, I had to remove this metric to avoid false negatives.

Another issue arose with the grounding_hit metric, which attempted to verify grounding by checking whether keywords from the question appeared frequently in the generated answer. While this works for some informational queries, it breaks down for paraphrased or entity-based answers where lexical overlap is minimal. An answer can be well-grounded in retrieved documents without explicitly repeating query terms.

I shipped the system with these limitations initially because simple heuristic-based checks were fast to implement and helped catch obvious failure cases early on. However, they lacked semantic understanding.

If I had more time, the most direct fix would be to replace these heuristics with context-aware grounding validation, such as checking alignment between the answer and retrieved chunks using embedding similarity instead of surface-level rules. This would preserve flexibility while improving evaluator reliability.

AI usage->
prompts ->
1)I have a mixed document corpus including FAQs, policies, technical docs, and guides.
Can you compare different chunking strategies (fixed-size, overlap-based, and semantic),
and explain tradeoffs specifically for RAG systems over internal documentation?

2)I have a mixed document corpus including FAQs, policies, technical docs, and guides.
Can you compare different chunking strategies (fixed-size, overlap-based, and semantic),
and explain tradeoffs specifically for RAG systems over internal documentation?

3)I want to add a post-generation evaluator layer to a RAG system.
What are practical heuristic-based checks I can implement without another LLM,
and what are their limitations?

4)Help me think through realistic failure cases for a vector-based RAG pipeline
where retrieval succeeds but the answer is still incorrect.
Focus on absence-of-information scenarios.

There are more prompts but i think these many are enough.