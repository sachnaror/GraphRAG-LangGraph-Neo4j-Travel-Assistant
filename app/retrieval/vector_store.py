import json
from dataclasses import asdict, dataclass
from pathlib import Path

import faiss
import numpy as np

from app.retrieval.embeddings import HashingEmbeddingModel


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
        self._index: faiss.IndexFlatIP | None = None

    def add_documents(self, chunks: list[DocumentChunk]) -> None:
        if not chunks:
            return

        vectors = self.embedding_model.embed_documents([chunk.text for chunk in chunks])
        matrix = _to_float32_matrix(vectors)
        if matrix.size == 0:
            return

        if self._index is None:
            self._index = faiss.IndexFlatIP(matrix.shape[1])

        self._index.add(matrix)
        self._chunks.extend(chunks)

    def similarity_search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if self._index is None or not self._chunks:
            return []

        limit = max(1, min(top_k, len(self._chunks)))
        query_matrix = _to_float32_matrix([self.embedding_model.embed_text(query)])
        scores, indices = self._index.search(query_matrix, limit)
        results: list[SearchResult] = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0 or index >= len(self._chunks):
                continue
            chunk = self._chunks[index]
            results.append(
                SearchResult(
                    source=chunk.source,
                    text=chunk.text,
                    score=round(float(score), 4),
                    metadata=chunk.metadata,
                )
            )

        return results

    @classmethod
    def from_directory(
        cls,
        directory: Path,
        chunk_size: int = 700,
        overlap: int = 100,
    ) -> "InMemoryVectorStore":
        store = cls()
        store.add_documents(collect_document_chunks(directory, chunk_size, overlap))
        return store

    def save(self, index_dir: Path) -> None:
        if self._index is None:
            raise ValueError("Cannot save an empty vector store.")

        index_dir.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self._index, str(index_dir / "index.faiss"))
        (index_dir / "chunks.json").write_text(
            json.dumps([asdict(chunk) for chunk in self._chunks], indent=2),
            encoding="utf-8",
        )
        (index_dir / "manifest.json").write_text(
            json.dumps(
                {
                    "embedding_dimensions": self.embedding_model.dimensions,
                    "chunk_count": len(self._chunks),
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, index_dir: Path) -> "InMemoryVectorStore":
        index_path = index_dir / "index.faiss"
        chunks_path = index_dir / "chunks.json"

        if not index_path.exists() or not chunks_path.exists():
            raise FileNotFoundError(f"Missing FAISS index files in {index_dir}")

        store = cls()
        store._index = faiss.read_index(str(index_path))
        chunks_payload = json.loads(chunks_path.read_text(encoding="utf-8"))
        store._chunks = [DocumentChunk(**chunk) for chunk in chunks_payload]

        if store._index.ntotal != len(store._chunks):
            raise ValueError(
                f"FAISS index/document metadata mismatch in {index_dir}: "
                f"{store._index.ntotal} vectors vs {len(store._chunks)} chunks."
            )

        return store

    @staticmethod
    def has_saved_index(index_dir: Path) -> bool:
        return (index_dir / "index.faiss").exists() and (index_dir / "chunks.json").exists()


def collect_document_chunks(
    directory: Path,
    chunk_size: int = 700,
    overlap: int = 100,
) -> list[DocumentChunk]:
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

    return chunks


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


def _to_float32_matrix(vectors: list[list[float]]) -> np.ndarray:
    if not vectors:
        return np.empty((0, 0), dtype="float32")
    return np.asarray(vectors, dtype="float32")
