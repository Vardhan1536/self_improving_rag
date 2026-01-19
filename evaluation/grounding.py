def grounding_score(retrieved_chunks):
    if not retrieved_chunks:
        return 0.0

    covered_chunks = sum(
        1 for c in retrieved_chunks if len(c.text.strip()) > 30
    )

    return round(covered_chunks / len(retrieved_chunks), 3)
