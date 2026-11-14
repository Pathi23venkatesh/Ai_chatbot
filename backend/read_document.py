file_path = "documents/company_info.txt"

with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

print(text)
chunk_size = 500
overlap = 100

chunks = []

start = 0

while start < len(text):
    end = start + chunk_size

    chunk = text[start:end]

    chunks.append(chunk)

    start = end - overlap

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i + 1}:")
    print(chunk)