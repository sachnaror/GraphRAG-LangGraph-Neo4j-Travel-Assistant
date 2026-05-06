import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import get_settings
from app.retrieval.retriever import DOCUMENTS_DIR, FAISS_INDEX_DIR
from app.retrieval.vector_store import InMemoryVectorStore, collect_document_chunks


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build or rebuild the FAISS document index.")
    parser.add_argument(
        "--documents-dir",
        default=None,
        help="Directory containing .txt documents to index.",
    )
    parser.add_argument(
        "--index-dir",
        default=None,
        help="Directory where the FAISS index and chunk metadata should be written.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=700,
        help="Maximum chunk size for document splitting.",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=100,
        help="Character overlap between chunks.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = get_settings()

    documents_dir = Path(args.documents_dir or settings.retrieval_documents_dir or DOCUMENTS_DIR)
    index_dir = Path(args.index_dir or settings.retrieval_index_dir or FAISS_INDEX_DIR)

    chunks = collect_document_chunks(
        directory=documents_dir,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
    if not chunks:
        print(f"No documents found to index in {documents_dir}")
        return 1

    store = InMemoryVectorStore()
    store.add_documents(chunks)
    store.save(index_dir)

    print(f"Indexed {len(chunks)} chunks from {documents_dir}")
    print(f"Wrote FAISS index to {index_dir / 'index.faiss'}")
    print(f"Wrote chunk metadata to {index_dir / 'chunks.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
