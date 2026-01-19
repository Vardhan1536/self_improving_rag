from ingestion.pipeline import IngestionPipeline
from ingestion.chunkers.fixed import FixedChunker
from ingestion.chunkers.section import SectionChunker
from ingestion.chunkers.semantic import SemanticChunker

def main():
    chunkers = [
        FixedChunker(chunk_size=200, overlap=50),
        SectionChunker(chunk_size=300, overlap=50),
        SemanticChunker(chunk_size=250, overlap=0),
    ]

    pipeline = IngestionPipeline(chunkers)

    pipeline.run(
        file_path="docs/sample.txt",
        output_path="chunks.json"
    )

if __name__ == "__main__":
    main()
