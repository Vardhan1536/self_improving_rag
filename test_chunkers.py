from ingestion.chunkers.fixed import FixedChunker
from ingestion.chunkers.section import SectionChunker
from ingestion.chunkers.semantic import SemanticChunker
from ingestion.document_loader import DocumentLoader

loader = DocumentLoader()
text = loader.load("docs/sample.txt")

chunkers = [
    FixedChunker(chunk_size=40, overlap=10),
    SectionChunker(chunk_size=60, overlap=10),
    SemanticChunker(chunk_size=50, overlap=0),
]

for chunker in chunkers:
    chunks = chunker.chunk(text, "sample.txt")
    print(f"\n{chunker.__class__.__name__}: {len(chunks)} chunks")
    for c in chunks[:2]:
        print("-" * 40)
        print(c.strategy, "| tokens:", c.token_count)
        print(c.text[:120])
