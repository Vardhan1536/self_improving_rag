import uuid
import nltk
from typing import List
from ingestion.chunkers.base import BaseChunker
from ingestion.schemas import Chunk

nltk.download("punkt")

class SemanticChunker(BaseChunker):
    def chunk(self, text: str, source_doc: str) -> List[Chunk]:
        sentences = nltk.sent_tokenize(text)
        chunks = []
        buffer = []
        buffer_len = 0

        for sentence in sentences:
            words = sentence.split()
            if buffer_len + len(words) > self.chunk_size:
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        text=" ".join(buffer),
                        source_doc=source_doc,
                        section="semantic",
                        strategy="semantic",
                        token_count=buffer_len,
                        metadata={}
                    )
                )
                buffer = []
                buffer_len = 0

            buffer.extend(words)
            buffer_len += len(words)

        if buffer:
            chunks.append(
                Chunk(
                    chunk_id=str(uuid.uuid4()),
                    text=" ".join(buffer),
                    source_doc=source_doc,
                    section="semantic",
                    strategy="semantic",
                    token_count=buffer_len,
                    metadata={}
                )
            )

        return chunks
