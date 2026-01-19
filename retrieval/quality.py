import numpy as np
import re

def avg_similarity(retrieved_chunks):
    if not retrieved_chunks:
        return 0.0
    return float(np.mean([c.similarity for c in retrieved_chunks]))


def redundancy_score(retrieved_chunks):
    texts = [c.text for c in retrieved_chunks]
    unique_ratio = len(set(texts)) / max(len(texts), 1)
    return round(1 - unique_ratio, 3)


def coverage_score(query, retrieved_chunks):
    query_terms = set(re.findall(r"\w+", query.lower()))
    retrieved_terms = set()

    for c in retrieved_chunks:
        retrieved_terms.update(re.findall(r"\w+", c.text.lower()))

    if not query_terms:
        return 0.0

    coverage = len(query_terms & retrieved_terms) / len(query_terms)
    return round(coverage, 3)


def retrieval_report(query, retrieved_chunks):
    return {
        "avg_similarity": avg_similarity(retrieved_chunks),
        "coverage": coverage_score(query, retrieved_chunks),
        "redundancy": redundancy_score(retrieved_chunks),
        "num_chunks": len(retrieved_chunks)
    }
