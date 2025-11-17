from llama_index import Document, VectorStoreIndex
from llama_index.vector_stores import WeaviateVectorStore
import weaviate
from pathlib import Path
import os

# Connect to Weaviate (works both in Docker and locally)
weaviate_url = os.getenv("WEAVIATE_URL", "http://localhost:8080")
client = weaviate.Client(weaviate_url)

# Load documents from mounted data folder
data_dir = Path("/app/data")
txt_files = list(data_dir.glob("*.txt"))

if not txt_files:
    print(f"Error: No .txt files found in {data_dir.absolute()}")
    exit(1)

documents = []
for txt_file in txt_files:
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            doc = Document(text=f.read(), metadata={"source": txt_file.stem})
            documents.append(doc)
        print(f"Loaded {txt_file.name}")
    except Exception as e:
        print(f"Error loading {txt_file}: {e}")

print(f"\nTotal documents: {len(documents)}")

# Build index (embeddings via TEI service)
vector_store = WeaviateVectorStore(weaviate_client=client)
index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("قانون کار در ایران چه می‌گوید؟")
print("\n--- Response ---")
print(response)