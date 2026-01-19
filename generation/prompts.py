BASE_PROMPT = """
You are a retrieval-augmented assistant.

Answer the question using ONLY the provided context.
If the context is insufficient, say so clearly.

Context:
{context}

Question:
{question}

Answer:
"""

CITE_PROMPT = """
You are a careful assistant.

First extract relevant facts from the context.
Then answer the question strictly from those facts.

Context:
{context}

Question:
{question}

Facts:
"""

