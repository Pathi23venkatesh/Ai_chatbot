
from rank_bm25 import BM25Okapi

# Step 1: Create sample documents
documents = [
    "Employees receive 20 paid leaves per year.",
    "Employees receive health insurance.",
    "The company provides annual salary bonuses."
]

# Step 2: Tokenize documents
tokenized_documents = [
    document.lower().split()
    for document in documents
]

# Step 3: Create BM25 model
bm25 = BM25Okapi(tokenized_documents)

# Step 4: Search query
query = "What is the annual salary?"

tokenized_query = query.lower().split()

# Step 5: Calculate document scores
scores = bm25.get_scores(tokenized_query)

# Step 6: Display ranked results
for index in scores.argsort()[::-1]:
    print(f"Score: {scores[index]:.4f}")
    print(f"Document: {documents[index]}")
    print()
