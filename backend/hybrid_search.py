
from rank_bm25 import BM25Okapi

from backend.vector_store import collection
from backend.llm import client


# ==========================================
# STEP 1: Get documents from ChromaDB
# ==========================================

results = collection.get(include=["documents"])

documents = results["documents"]

print("Total documents:", len(documents))


# ==========================================
# STEP 2: Create BM25 index
# ==========================================

tokenized_documents = [
    document.lower().split()
    for document in documents
]

bm25 = BM25Okapi(tokenized_documents)

print("BM25 index created successfully!")


# ==========================================
# STEP 3: BM25 keyword search
# ==========================================

def bm25_search(query, top_k=10):

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    top_indexes = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:top_k]

    return [
        documents[i]
        for i in top_indexes
        if scores[i] > 0
    ]


# ==========================================
# STEP 4: Semantic search using Gemini
# ==========================================

def semantic_search(query, top_k=10):

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=query
    )

    query_embedding = response.embeddings[0].values

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]


# ==========================================
# STEP 5: Reciprocal Rank Fusion (RRF)
# ==========================================

def reciprocal_rank_fusion(
    bm25_results,
    semantic_results,
    k=60
):

    scores = {}

    # Add BM25 ranking scores
    for rank, document in enumerate(bm25_results):

        if document not in scores:
            scores[document] = 0

        scores[document] += 1 / (k + rank + 1)

    # Add semantic ranking scores
    for rank, document in enumerate(semantic_results):

        if document not in scores:
            scores[document] = 0

        scores[document] += 1 / (k + rank + 1)

    # Sort documents by combined score
    ranked_documents = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return ranked_documents


# ==========================================
# STEP 6: Complete Hybrid Search
# ==========================================

def hybrid_search(query, top_k=5):

    print("\nSearching with BM25...")

    bm25_results = bm25_search(query, top_k=10)

    print("BM25 results:", len(bm25_results))

    print("\nSearching with Semantic Search...")

    semantic_results = semantic_search(query, top_k=10)

    print("Semantic results:", len(semantic_results))

    print("\nCombining results using RRF...")

    final_results = reciprocal_rank_fusion(
        bm25_results,
        semantic_results
    )

    return final_results[:top_k]


# ==========================================
# STEP 7: Test Hybrid Search
# ==========================================

if __name__ == "__main__":

    query = "How many vacation days do employees get?"

    print("\nUser Question:", query)

    results = hybrid_search(query)

    print("\n========== HYBRID SEARCH RESULTS ==========")

    for rank, (document, score) in enumerate(results, start=1):

        print(f"\nRank: {rank}")

        print("Document:", document)

        print("RRF Score:", round(score, 6))
