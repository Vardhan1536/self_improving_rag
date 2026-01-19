from evaluation.answer_type import AnswerType
from evaluation.refusal_detection import is_semantic_refusal

def decide_answer_type(answer: str, confidence: float) -> AnswerType:
    """
    Decision rules:
    1. If model explicitly refuses → REFUSAL
    2. If confidence extremely low → REFUSAL (unsafe to answer)
    3. Else → ANSWER
    """

    if is_semantic_refusal(answer):
        return AnswerType.REFUSAL

    if confidence < 0.4:
        return AnswerType.REFUSAL

    return AnswerType.ANSWER
