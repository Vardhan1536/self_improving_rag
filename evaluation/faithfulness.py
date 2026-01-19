import re

def faithfulness_score(answer, context):
    answer_terms = set(re.findall(r"\w+", answer.lower()))
    context_terms = set(re.findall(r"\w+", context.lower()))

    if not answer_terms:
        return 0.0

    supported = answer_terms & context_terms
    return round(len(supported) / len(answer_terms), 3)
