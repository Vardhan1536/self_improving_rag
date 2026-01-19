# Retrieval Analysis

## Why Top-K Retrieval Is Insufficient
High similarity does not guarantee coverage of query intent.

## Silent Failure Modes
- Redundant chunks
- Partial grounding
- Missing query sub-questions

## Why We Measure Coverage
Coverage approximates whether retrieved context can answer the question.

## Role in Self-Improving RAG
Low coverage triggers re-chunking or strategy switching.
