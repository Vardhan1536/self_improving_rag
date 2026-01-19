from dataclasses import dataclass
from typing import Dict

@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    similarity: float
    strategy: str
    metadata: Dict
