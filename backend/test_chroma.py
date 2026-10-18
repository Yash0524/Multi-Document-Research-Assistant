
import chromadb
from sentence_transformers import SentenceTransformer

# Load the same embedding model we tested earlier.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Create an in-memory ChromaDB database.
client = chromadb.Client()

# Create a collection to store our text.
collection = client.create_collection(name="research_documents")

documents = [
    "Employees receive their salary every month.",
    "The company provides annual performance bonuses.",
    "The weather forecast predicts heavy rainfall.",
]

# Convert each sentence into an embedding.
embeddings = model.encode(documents).tolist()

# Store the sentences and their embeddings.
collection.add(
    ids=["chunk_1", "chunk_2", "chunk_3"],
    documents=documents,
    embeddings=embeddings,
    metadatas=[
        {"filename": "hr_policy.pdf", "page_number": 1},
        {"filename": "hr_policy.pdf", "page_number": 2},
        {"filename": "weather_report.pdf", "page_number": 1},
    ],
)

# Search for information by meaning.
question = "When are workers paid?"
question_embedding = model.encode([question]).tolist()

results = collection.query(
    query_embeddings=question_embedding,
    n_results=2,
)

print("Question:", question)
print("\nSearch results:")

for document, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
):
    print("\nText:", document)
    print("Source:", metadata["filename"])
    print("Page:", metadata["page_number"])
    print("Distance:", round(distance, 3))
