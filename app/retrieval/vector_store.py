from dataclasses import dataclass
from pathlib import Path

from app.retrieval.embeddings import HashingEmbeddingModel, cosine_similarity


@dataclass(frozen=True)
class DocumentChunk:
    source: str
    text: str
    metadata: dict


@dataclass(frozen=True)
class SearchResult:
    source: str
    text: str
    score: float
    metadata: dict


class InMemoryVectorStore:
    def __init__(self, embedding_model: HashingEmbeddingModel | None = None) -> None:
        self.embedding_model = embedding_model or HashingEmbeddingModel()
        self._chunks: list[DocumentChunk] = []
        self._vectors: list[list[float]] = []

    def add_documents(self, chunks: list[DocumentChunk]) -> None:
        self._chunks.extend(chunks)
        self._vectors.extend(self.embedding_model.embed_documents([chunk.text for chunk in chunks]))

    def similarity_search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        query_vector = self.embedding_model.embed_text(query)
        ranked = []

        for chunk, vector in zip(self._chunks, self._vectors):
            ranked.append(
                SearchResult(
                    source=chunk.source,
                    text=chunk.text,
                    score=round(cosine_similarity(query_vector, vector), 4),
                    metadata=chunk.metadata,
                )
            )

        return sorted(ranked, key=lambda result: result.score, reverse=True)[:top_k]

    @classmethod
    def from_directory(
        cls,
        directory: Path,
        chunk_size: int = 700,
        overlap: int = 100,
    ) -> "InMemoryVectorStore":
        store = cls()
        chunks: list[DocumentChunk] = []

        for path in sorted(directory.glob("*.txt")):
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                continue
            for index, chunk_text in enumerate(_chunk_text(text, chunk_size, overlap)):
                chunks.append(
                    DocumentChunk(
                        source=path.name,
                        text=chunk_text,
                        metadata={"chunk": index, "path": str(path)},
                    )
                )

        store.add_documents(chunks)
        return store


def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(end - overlap, start + 1)
    return [chunk for chunk in chunks if chunk]
