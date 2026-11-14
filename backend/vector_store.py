import chromadb
from pathlib import Path

# Create a persistent ChromaDB database
DB_PATH = Path(__file__).resolve().parent.parent / "chroma_db"

chroma_client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

# Create or connect to a collection
collection = chroma_client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

print("ChromaDB connected successfully!")
print("Collection:", collection.name)
print("Database location:", DB_PATH)