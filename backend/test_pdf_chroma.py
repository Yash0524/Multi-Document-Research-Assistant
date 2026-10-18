
from app.document_processor import process_pdf
from app.vector_store import collection, embedding_model

# 1. Process the PDF using the improved chunker.
chunks = process_pdf(
    file_path="../data/sample.pdf",
    chunk_size=500,
    overlap=50,
)

# 2. Remove old sample.pdf chunks so stale chunks cannot remain.
existing = collection.get(
    where={"filename": "sample.pdf"},
    include=["metadatas"],
)

old_ids = existing["ids"]

if old_ids:
    collection.delete(ids=old_ids)

# 3. Prepare the new chunk text and metadata.
documents = [chunk["text"] for chunk in chunks]

ids = [
    f"{chunk['filename']}_page{chunk['page_number']}_chunk{chunk['chunk_index']}"
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

# 4. Generate embeddings and store the new chunks.
embeddings = embedding_model.encode(documents).tolist()

if documents:
    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

print(f"Re-indexed {len(chunks)} chunks from sample.pdf.")
print("Total chunks in collection:", collection.count())

# 5. Search for relevant evidence.
question = "What does the company do?"

if collection.count() > 0:
    question_embedding = embedding_model.encode([question]).tolist()

    results = collection.query(
        query_embeddings=question_embedding,
        n_results=min(3, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    print("\nQuestion:", question)
    print("\nSearch results:")

    for document, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        print("\nText:", document)
        print("Source:", metadata["filename"])
        print("Page:", metadata["page_number"])
        print("Chunk:", metadata["chunk_index"])
        print("Distance:", round(distance, 3))
