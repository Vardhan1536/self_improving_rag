import json

from retrieval.vector_store import VectorStore
from retrieval.retriever import Retriever
from retrieval.quality import retrieval_report

from generation.generator import Generator

from evaluation.faithfulness import faithfulness_score
from evaluation.grounding import grounding_score
from evaluation.confidence import confidence_score, should_refuse

from feedback.controller import SelfImprovingController
from memory.store import MemoryStore

# Load chunks
with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Core systems
vector_store = VectorStore()
vector_store.build(chunks)

retriever = Retriever(vector_store)
generator = Generator()

memory_store = MemoryStore()
controller = SelfImprovingController(memory_store)

# query = "Why does bad chunking break RAG systems?"
query = "How does bad chunking affect gradient flow in transformer attention layers?"

# --- Retrieval ---
retrieved = retriever.retrieve(query)
retrieval_metrics = retrieval_report(query, retrieved)

# --- Generation ---
answer = generator.generate(query, retrieved)

# --- Evaluation ---
context = "\n".join(c.text for c in retrieved)
faithfulness = faithfulness_score(answer, context)
grounding = grounding_score(retrieved)
confidence = confidence_score(retrieval_metrics, faithfulness, grounding)

print("\n=== INITIAL ANSWER ===")
print(answer)

print("\n=== EVALUATION ===")
print("Retrieval:", retrieval_metrics)
print("Faithfulness:", faithfulness)
print("Grounding:", grounding)
print("Confidence:", confidence)
print("Refuse:", should_refuse(confidence))

decision = controller.process(
    query=query,
    retrieval_report=retrieval_metrics,
    faithfulness=faithfulness,
    confidence=confidence
)

if decision is None:
    print("\nNo failure detected. No retry needed.")
    exit()

print("\n=== FAILURE DETECTED ===")
print("Failure type:", decision["failure"])
print("Applying fix:", decision["fix"])

# Apply retry parameters
retry_top_k = decision["fix"].get("top_k", 5)

improved_retrieved = retriever.retrieve(
    query,
    top_k=retry_top_k
)

improved_answer = generator.generate(query, improved_retrieved)

improved_context = "\n".join(c.text for c in improved_retrieved)

improved_faithfulness = faithfulness_score(
    improved_answer,
    improved_context
)

improved_grounding = grounding_score(improved_retrieved)

improved_retrieval_metrics = retrieval_report(
    query,
    improved_retrieved
)

improved_confidence = confidence_score(
    improved_retrieval_metrics,
    improved_faithfulness,
    improved_grounding
)

controller.store_learning(
    query=query,
    failure=decision["failure"],
    fix=decision["fix"],
    conf_before=confidence,
    conf_after=improved_confidence
)

print("\n=== IMPROVED ANSWER ===")
print(improved_answer)

print("\n=== IMPROVED EVALUATION ===")
print("Faithfulness:", improved_faithfulness)
print("Grounding:", improved_grounding)
print("Confidence:", improved_confidence)
print("Refuse:", should_refuse(improved_confidence))
