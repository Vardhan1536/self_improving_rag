import json
import logging
from retrieval.vector_store import VectorStore
from retrieval.retriever import Retriever
from retrieval.quality import retrieval_report

logging.basicConfig(
    filename="logs/retrieval.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

vector_store = VectorStore()
vector_store.build(chunks)

retriever = Retriever(vector_store)

query = "Why does bad chunking break RAG systems?"

retrieved = retriever.retrieve(query, top_k=5)
report = retrieval_report(query, retrieved)

logging.info(f"Query: {query}")
logging.info(f"Retrieval report: {report}")

print("\nRetrieved Chunks:")
for c in retrieved:
    print("-" * 60)
    print(f"Score: {round(c.similarity,3)} | Strategy: {c.strategy}")
    print(c.text[:200])

print("\nQuality Report:", report)
