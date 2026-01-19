def is_semantic_refusal(answer: str) -> bool:
    refusal_phrases = [
        "does not provide sufficient information",
        "cannot be answered from the context",
        "not mentioned in the context",
        "insufficient information",
        "cannot determine from the given context"
    ]

    answer_lower = answer.lower()
    return any(phrase in answer_lower for phrase in refusal_phrases)
