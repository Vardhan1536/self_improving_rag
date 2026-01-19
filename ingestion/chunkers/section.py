import uuid
from typing import List
from ingestion.chunkers.base import BaseChunker
from ingestion.schemas import Chunk

class SectionChunker(BaseChunker):
    def chunk(self, text: str, source_doc: str) -> List[Chunk]:
        sections = text.split("\n\n")
        chunks = []

        for idx, section in enumerate(sections):
            words = section.split()
            if not words:
                continue

            if len(words) <= self.chunk_size:
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        text=section.strip(),
                        source_doc=source_doc,
                        section=f"section_{idx}",
                        strategy="section",
                        token_count=len(words),
                        metadata={}
                    )
                )
            else:
                start = 0
                while start < len(words):
                    end = start + self.chunk_size
                    chunk_words = words[start:end]
                    chunks.append(
                        Chunk(
                            chunk_id=str(uuid.uuid4()),
                            text=" ".join(chunk_words),
                            source_doc=source_doc,
                            section=f"section_{idx}",
                            strategy="section",
                            token_count=len(chunk_words),
                            metadata={"subsection": True}
                        )
                    )
                    start = end - self.overlap

        return chunks
