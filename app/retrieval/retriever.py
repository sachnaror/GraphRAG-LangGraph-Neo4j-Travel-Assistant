from functools import lru_cache
from pathlib import Path

from app.config import ROOT_DIR
from app.retrieval.vector_store import InMemoryVectorStore, SearchResult


DOCUMENTS_DIR = ROOT_DIR / "data" / "documents"


class DocumentRetriever:
    def __init__(self, vector_store: InMemoryVectorStore) -> None:
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 3) -> list[SearchResult]:
        return [
            result
            for result in self.vector_store.similarity_search(query, top_k)
            if result.score > 0
        ]


@lru_cache
def get_document_retriever(documents_dir: str | None = None) -> DocumentRetriever:
    directory = Path(documents_dir) if documents_dir else DOCUMENTS_DIR
    return DocumentRetriever(InMemoryVectorStore.from_directory(directory))
