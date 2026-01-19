from dataclasses import dataclass
from typing import Dict

@dataclass
class MemoryRecord:
    query: str
    failure_type: str
    fix_applied: Dict
    confidence_before: float
    confidence_after: float
