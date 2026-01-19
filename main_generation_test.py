import json
from retrieval.vector_store import VectorStore
from retrieval.retriever import Retriever
from retrieval.quality import retrieval_report
from generation.generator import Generator
from evaluation.faithfulness import faithfulness_score
from evaluation.grounding import grounding_score
from evaluation.confidence import confidence_score, should_refuse

with open("chunks.json") as f:
    chunks = json.load(f)

vector_store = VectorStore()
vector_store.build(chunks)

retriever = Retriever(vector_store)
generator = Generator()

query = "Why does bad chunking break RAG systems?"

retrieved = retriever.retrieve(query)
report = retrieval_report(query, retrieved)

answer = generator.generate(query, retrieved)

context = "\n".join([c.text for c in retrieved])

faith = faithfulness_score(answer, context)
ground = grounding_score(retrieved)
conf = confidence_score(report, faith, ground)

print("\nAnswer:\n", answer)
print("\nEvaluation:")
print("Faithfulness:", faith)
print("Grounding:", ground)
print("Confidence:", conf)
print("Refuse:", should_refuse(conf))


