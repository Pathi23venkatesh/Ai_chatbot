from pypdf import PdfReader

# Step 1: Read PDF
file_path = "documents/company_policy.pdf"
reader = PdfReader(file_path)

# Step 2: Extract text from all pages
full_text = ""

for page in reader.pages:
    text = page.extract_text() or ""
    full_text += text + "\n"

# Step 3: Set chunking parameters
chunk_size = 500
overlap = 100

# Step 4: Create chunks
chunks = []
start = 0

while start < len(full_text):
    end = start + chunk_size

    chunk = full_text[start:end]
    chunks.append(chunk)

    start = end - overlap

# Step 5: Display chunks
print("Total characters:", len(full_text))
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk)