def retry_strategy(failure_type):
    if failure_type == "weak_retrieval":
        return {
            "chunking": "semantic",
            "top_k": 8
        }

    if failure_type == "hallucination_risk":
        return {
            "prompt": "cite_then_answer"
        }

    if failure_type == "low_confidence":
        return {
            "chunking": "section",
            "top_k": 10
        }

    return None
