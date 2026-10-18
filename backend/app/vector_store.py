
import chromadb
from sentence_transformers import SentenceTransformer

# Resolve the database path relative to this file,
# so it doesn't depend on the terminal's working directory.
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "chroma_db"

# Load the embedding model once.
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Open the persistent ChromaDB database.
chroma_client = chromadb.PersistentClient(
    path=str(DATABASE_PATH)
)

# Create or access the document collection.
collection = chroma_client.get_or_create_collection(
    name="research_documents"
)


def store_chunks(chunks: list[dict]) -> int:
    """Generate embeddings and store document chunks with metadata."""

    if not chunks:
        return 0

    documents = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.encode(documents).tolist()

    ids = [
        (
            f"{chunk['filename']}_page{chunk['page_number']}"
            f"_chunk{chunk['chunk_index']}"
        )
        for chunk in chunks
    ]

    metadatas = [
        {
            "filename": chunk["filename"],
            "page_number": chunk["page_number"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)
