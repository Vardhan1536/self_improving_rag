from pathlib import Path

class DocumentLoader:
    def load(self, file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"{file_path} not found")

        with open(path, "r", encoding="utf-8") as f:
            return f.read()
