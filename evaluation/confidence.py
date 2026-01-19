def confidence_score(retrieval_report, faithfulness, grounding):
    return round(
        0.4 * retrieval_report["coverage"] +
        0.3 * faithfulness +
        0.3 * grounding,
        3
    )
