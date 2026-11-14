
import time
from pathlib import Path

from pypdf import PdfReader
from google.genai import types

from backend.llm import client
from backend.vector_store import collection


# STEP 1: Read PDF
BASE_DIR = Path(__file__).resolve().parent.parent
file_path = BASE_DIR / "documents" / "company_policy.pdf"

print("Reading PDF...")

reader = PdfReader(str(file_path))
full_text = ""

for page in reader.pages:
    full_text += (page.extract_text() or "") + "\n"

print("PDF reading completed!")


# STEP 2: Split text into chunks
chunk_size = 500
overlap = 100

chunks = []
start = 0

while start < len(full_text):
    end = start + chunk_size
    chunk = full_text[start:end]

    if chunk.strip():
        chunks.append(chunk)

    start = end - overlap

print("Total chunks:", len(chunks))


# STEP 3: Generate and save embeddings batch by batch
batch_size = 20


# STEP 3: Find chunks not already saved

existing = collection.get(include=[])

saved_ids = set(existing["ids"])

pending_chunks = []
pending_ids = []

for i, chunk in enumerate(chunks):

    chunk_id = f"company_policy_chunk_{i}"

    if chunk_id not in saved_ids:
        pending_chunks.append(chunk)
        pending_ids.append(chunk_id)

print("Already saved:", len(saved_ids))
print("Remaining chunks:", len(pending_chunks))


# STEP 4: Generate and save remaining embeddings

batch_size = 20

for start in range(0, len(pending_chunks), batch_size):

    batch = pending_chunks[start:start + batch_size]
    batch_ids = pending_ids[start:start + batch_size]

    print(
        f"Processing {start + len(batch)} "
        f"/ {len(pending_chunks)} remaining chunks"
    )

    contents = [
        types.Content(
            parts=[types.Part.from_text(text=chunk)]
        )
        for chunk in batch
    ]

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=contents
    )

    embeddings = [
        item.values for item in response.embeddings
    ]

    if len(embeddings) != len(batch):
        raise ValueError("Embedding count mismatch!")

    collection.upsert(
        ids=batch_ids,
        documents=batch,
        embeddings=embeddings
    )

    print("Batch saved successfully!")

    if start + batch_size < len(pending_chunks):
        print("Waiting 20 seconds...")
        time.sleep(20)


# STEP 5: Final result

print("\nIngestion completed!")
print("Total documents in ChromaDB:", collection.count())
