
from app.vector_store import collection, embedding_model
# Starting threshold; validate against more questions before relying on it.
MAX_DISTANCE = 1.15


def search_documents(question: str, top_k: int = 3) -> list[dict]:
    """Find relevant document chunks and return their citation metadata."""

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    # If no document chunks exist, return an empty result.
    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    # Convert the question into an embedding using our shared model.
    question_embedding = embedding_model.encode(
        [question]
    ).tolist()

    # Retrieve the most similar document chunks.
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=min(top_k, total_chunks),
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Attach citation details to every retrieved passage.
    for document, metadata, distance in zip(
        documents, metadatas, distances
    ):
        matches.append({
            "text": document,
            "filename": metadata["filename"],
            "page_number": metadata["page_number"],
            "chunk_index": metadata["chunk_index"],
            "distance": round(distance, 3),
        })

    # Keep only passages close enough to be potentially relevant.
    relevant_matches = [
        match for match in matches
        if match["distance"] <= MAX_DISTANCE
    ]

    return relevant_matches
