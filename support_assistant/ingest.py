from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"


# --------------------------------------------------
# Load the embedding model
# --------------------------------------------------

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# --------------------------------------------------
# Create ChromaDB client
# --------------------------------------------------

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# --------------------------------------------------
# Create or get collection
# --------------------------------------------------

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space": "cosine"}
)


# --------------------------------------------------
# Read the 8 documents
# --------------------------------------------------

documents = []
document_ids = []
metadatas = []

for file_path in sorted(DOCS_DIR.glob("doc_*.txt")):

    text = file_path.read_text(
        encoding="utf-8"
    ).strip()

    if not text:
        continue

    # One document = one chunk
    documents.append(text)

    document_ids.append(
        file_path.stem
    )

    metadatas.append(
        {
            "source": file_path.name
        }
    )


# --------------------------------------------------
# Check document count
# --------------------------------------------------

print(f"Documents loaded: {len(documents)}")

if len(documents) != 8:
    raise ValueError(
        f"Expected 8 documents, but found {len(documents)}"
    )


# --------------------------------------------------
# Create embeddings
# --------------------------------------------------

print("Creating embeddings...")

embeddings = model.encode(
    documents,
    normalize_embeddings=True
).tolist()

print("Embeddings created.")


# --------------------------------------------------
# Store documents + embeddings in ChromaDB
# --------------------------------------------------

collection.upsert(
    ids=document_ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)


# --------------------------------------------------
# Verify ChromaDB
# --------------------------------------------------

print(
    f"Documents stored in ChromaDB: {collection.count()}"
)

print("Ingestion completed successfully.")