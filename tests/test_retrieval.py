from pathlib import Path

from app.retrieval.retriever import get_document_retriever
from app.retrieval.vector_store import InMemoryVectorStore


def test_vector_store_can_save_and_load_faiss_index(tmp_path):
    documents_dir = tmp_path / "documents"
    documents_dir.mkdir()
    (documents_dir / "policy.txt").write_text(
        "Refundable business fares prioritize reliability and flexibility.",
        encoding="utf-8",
    )

    index_dir = tmp_path / "faiss_index"
    store = InMemoryVectorStore.from_directory(documents_dir)
    store.save(index_dir)

    loaded_store = InMemoryVectorStore.load(index_dir)
    results = loaded_store.similarity_search("business refundable reliability", top_k=1)

    assert (index_dir / "index.faiss").exists()
    assert (index_dir / "chunks.json").exists()
    assert results
    assert results[0].text


def test_retriever_prefers_saved_index_when_available(tmp_path):
    documents_dir = tmp_path / "documents"
    documents_dir.mkdir()
    (documents_dir / "pricing.txt").write_text(
        "Cheapest fares usually come with more restrictions than refundable tickets.",
        encoding="utf-8",
    )

    index_dir = tmp_path / "faiss_index"
    store = InMemoryVectorStore.from_directory(documents_dir)
    store.save(index_dir)

    get_document_retriever.cache_clear()
    retriever = get_document_retriever(str(documents_dir), str(index_dir))
    results = retriever.retrieve("cheapest restrictions refundable", top_k=1)

    assert results
    assert "refundable" in results[0].text.lower()
