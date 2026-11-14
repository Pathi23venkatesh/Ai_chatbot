from backend.llm import client
import math

# Two sentences
text1 = "Employees receive 20 paid leaves per year."
text2 = "How many vacation days do employees get?"

# Generate first embedding
response1 = client.models.embed_content(
    model="gemini-embedding-2",
    contents=text1
)

# Generate second embedding
response2 = client.models.embed_content(
    model="gemini-embedding-2",
    contents=text2
)

# Get vectors
embedding1 = response1.embeddings[0].values
embedding2 = response2.embeddings[0].values

# Calculate cosine similarity
dot_product = sum(a * b for a, b in zip(embedding1, embedding2))

magnitude1 = math.sqrt(sum(a * a for a in embedding1))
magnitude2 = math.sqrt(sum(b * b for b in embedding2))

similarity = dot_product / (magnitude1 * magnitude2)

print("Cosine Similarity:", similarity)