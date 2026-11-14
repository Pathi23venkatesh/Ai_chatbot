from backend.llm import client
from backend.vector_store import collection

# Question from the user
question = "How many vacation days do employees get?"

# Convert the question into an embedding
response = client.models.embed_content(
    model="gemini-embedding-2",
    contents=question
)

query_embedding = response.embeddings[0].values

# Search ChromaDB for the most similar document
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=1
)

# Display the retrieved document
print("Question:", question)
print("Retrieved document:", results["documents"][0][0])
print("Distance:", results["distances"][0][0])