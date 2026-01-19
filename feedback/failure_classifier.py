from evaluation.answer_type import AnswerType

def classify_failure(retrieval_report, faithfulness, confidence, answer_type):
    if answer_type == AnswerType.REFUSAL and retrieval_report["coverage"] < 0.5:
        return "weak_retrieval"

    if faithfulness < 0.6:
        return "hallucination_risk"

    if confidence < 0.4:
        return "low_confidence"

    return "no_failure"
