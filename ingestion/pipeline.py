import json
import logging
from typing import List
from ingestion.schemas import Chunk
from ingestion.document_loader import DocumentLoader

logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class IngestionPipeline:
    def __init__(self, chunkers: List):
        self.chunkers = chunkers
        self.loader = DocumentLoader()

    def run(self, file_path: str, output_path: str):
        text = self.loader.load(file_path)
        all_chunks = []

        for chunker in self.chunkers:
            chunks = chunker.chunk(text, file_path)
            logging.info(
                f"Chunker={chunker.__class__.__name__} produced {len(chunks)} chunks"
            )
            all_chunks.extend(chunks)

        serialized = [chunk.__dict__ for chunk in all_chunks]

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f, indent=2)

        logging.info(f"Total chunks stored: {len(all_chunks)}")
    