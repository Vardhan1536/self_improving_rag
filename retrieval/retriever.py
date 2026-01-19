from retrieval.schemas import RetrievedChunk

class Retriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k=5):
        results = self.vector_store.search(query, top_k)

        retrieved = []
        for chunk, score in results:
            retrieved.append(
                RetrievedChunk(
                    chunk_id=chunk["chunk_id"],
                    text=chunk["text"],
                    similarity=score,
                    strategy=chunk["strategy"],
                    metadata=chunk["metadata"]
                )
            )
        return retrieved
