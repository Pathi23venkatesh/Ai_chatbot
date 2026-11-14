
from rank_bm25 import BM25Okapi
from backend.vector_store import collection

# Step 1: Get actual documents from ChromaDB
results = collection.get(include=["documents"])

documents = results["documents"]

print("Documents from ChromaDB:", documents)

# Step 2: Check whether documents exist
if not documents:
    print("No documents found in ChromaDB.")
    raise SystemExit

# Step 3: Tokenize documents
tokenized_documents = [
    document.lower().split()
    for document in documents
]

# Step 4: Create BM25 model
bm25 = BM25Okapi(tokenized_documents)

# Step 5: Search question
query = "How many paid leaves do employees get?"

tokenized_query = query.lower().split()

# Step 6: Calculate relevance scores
scores = bm25.get_scores(tokenized_query)

# Step 7: Display ranked documents
ranked_indices = scores.argsort()[::-1]

for index in ranked_indices:
    print("Score:", round(float(scores[index]), 4))
    print("Document:", documents[index])
    print("-------------------------")
