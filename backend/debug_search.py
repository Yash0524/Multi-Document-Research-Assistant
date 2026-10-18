
from app.vector_store import collection, embedding_model

question = "What does the company do?"

embedding = embedding_model.encode([question]).tolist()

results = collection.query(
    query_embeddings=embedding,
    n_results=min(5, collection.count()),
    include=["documents", "metadatas", "distances"],
)

for document, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
):
    print(f"Distance: {distance:.3f}")
    print(f"File: {metadata['filename']}")
    print(f"Page: {metadata['page_number']}")
    print(f"Text: {document[:250]}")
    print("-" * 50)
