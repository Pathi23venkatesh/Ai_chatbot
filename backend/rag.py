
from backend.llm import get_llm_response
from backend.hybrid_search import hybrid_search


# Step 1: Retrieve relevant documents using Hybrid Search
def retrieve_documents(question):

    results = hybrid_search(question, top_k=5)

    # Extract document text from (document, score) results
    documents = [
        document
        for document, score in results
    ]

    return documents


# Step 2: Generate answer using Gemini
def generate_answer(question):

    # Retrieve documents
    documents = retrieve_documents(question)

    print("Retrieved documents:", documents)

    # Check if documents exist
    if not documents:
        return "I don't have enough information."

    # Combine documents into context
    context = "\n".join(documents)

    # Send question and context to Gemini
    answer = get_llm_response(question, context)

    return answer
