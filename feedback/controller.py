from feedback.failure_classifier import classify_failure
from feedback.retry_policy import retry_strategy
from memory.schemas import MemoryRecord
from evaluation.answer_type import AnswerType


class SelfImprovingController:
    def __init__(self, memory_store):
        self.memory = memory_store

    def process(
        self,
        query,
        retrieval_report,
        faithfulness,
        confidence,
        answer_type: AnswerType
    ):
        failure = classify_failure(
            retrieval_report=retrieval_report,
            faithfulness=faithfulness,
            confidence=confidence,
            answer_type=answer_type
        )

        if failure == "no_failure":
            return None

        fix = retry_strategy(failure)

        return {
            "failure": failure,
            "fix": fix
        }

    def store_learning(
        self,
        query,
        failure,
        fix,
        conf_before,
        conf_after
    ):
        record = MemoryRecord(
            query=query,
            failure_type=failure,
            fix_applied=fix,
            confidence_before=conf_before,
            confidence_after=conf_after
        )

        self.memory.save(record)
