import uuid
from typing import List
from ingestion.chunkers.base import BaseChunker
from ingestion.schemas import Chunk

class FixedChunker(BaseChunker):
    def chunk(self, text: str, source_doc: str) -> List[Chunk]:
        words = text.split()
        chunks = []
        start = 0
        chunk_idx = 0

        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    text=chunk_text,
                    source_doc=source_doc,
                    section="N/A",
                    strategy="fixed",
                    token_count=len(chunk_words),
                    metadata={
                        "chunk_index": chunk_idx,
                        "start_token": start,
                        "end_token": end
                    }
                )
            )

            start = end - self.overlap
            chunk_idx += 1

        return chunks
