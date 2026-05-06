from functools import lru_cache
from pathlib import Path

from app.config import ROOT_DIR, get_settings
from app.retrieval.vector_store import InMemoryVectorStore, SearchResult


DOCUMENTS_DIR = ROOT_DIR / "data" / "documents"
FAISS_INDEX_DIR = ROOT_DIR / "data" / "embeddings" / "faiss_index"


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
def get_document_retriever(
    documents_dir: str | None = None,
    index_dir: str | None = None,
) -> DocumentRetriever:
    settings = get_settings()
    directory = Path(documents_dir or settings.retrieval_documents_dir or DOCUMENTS_DIR)
    resolved_index_dir = Path(index_dir or settings.retrieval_index_dir or FAISS_INDEX_DIR)

    if InMemoryVectorStore.has_saved_index(resolved_index_dir):
        return DocumentRetriever(InMemoryVectorStore.load(resolved_index_dir))

    store = InMemoryVectorStore.from_directory(directory)
    if settings.retrieval_build_on_startup:
        store.save(resolved_index_dir)
    return DocumentRetriever(store)
