from dataclasses import dataclass
from typing import Dict

@dataclass
class Chunk:
    chunk_id: str
    text: str
    source_doc: str
    section: str
    strategy: str
    token_count: int
    metadata: Dict
