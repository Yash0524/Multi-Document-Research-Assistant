
from sentence_transformers import SentenceTransformer

# Load a small model that creates text embeddings.
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences = [
    "The employee earns a monthly salary.",
    "The worker receives pay every month.",
    "The weather is sunny today.",
]

embeddings = model.encode(sentences)

print("Number of sentences:", len(sentences))
print("Embedding dimensions:", embeddings.shape)
print("First embedding preview:", embeddings[0][:5])



from sklearn.metrics.pairwise import cosine_similarity

similarity_matrix = cosine_similarity(embeddings)

print("\nSimilarity between sentence 1 and 2:")
print(round(float(similarity_matrix[0, 1]), 3))

print("Similarity between sentence 1 and 3:")
print(round(float(similarity_matrix[0, 2]), 3))
