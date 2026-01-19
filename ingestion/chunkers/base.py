from abc import ABC, abstractmethod
from typing import List
from ingestion.schemas import Chunk

class BaseChunker(ABC):
    def __init__(self, chunk_size: int, overlap: int):
        self.chunk_size = chunk_size
        self.overlap = overlap

    @abstractmethod
    def chunk(self, text: str, source_doc: str) -> List[Chunk]:
        pass
