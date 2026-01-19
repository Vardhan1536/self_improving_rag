import json
from memory.schemas import MemoryRecord

class MemoryStore:
    def __init__(self, path="memory/memory.json"):
        self.path = path

    def save(self, record: MemoryRecord):
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(record.__dict__)

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)
