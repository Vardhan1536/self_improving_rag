def classify_failure(retrieval_report, faithfulness, confidence):
    if retrieval_report["coverage"] < 0.5:
        return "weak_retrieval"

    if faithfulness < 0.6:
        return "hallucination_risk"

    if confidence < 0.55:
        return "low_confidence"

    return "no_failure"
