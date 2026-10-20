
from pathlib import Path
import re

import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

KB_DIR = Path("knowledge_base")


def load_documents():
    documents = []

    for file_path in sorted(KB_DIR.glob("*.md")):
        text = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "text": text,
        })

    return documents


def fixed_size_chunking(text, chunk_size=300, overlap=50):
    """Split text into fixed-size character chunks with overlap."""

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Chunk size must be positive and overlap smaller than chunk size.")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start += chunk_size - overlap

    return chunks

def sentence_based_chunking(text, sentences_per_chunk=2):
    """Split text into chunks containing complete sentences."""

    if sentences_per_chunk <= 0:
        raise ValueError("sentences_per_chunk must be positive.")

    # Replace line breaks with spaces
    cleaned_text = " ".join(text.split())

    # Split sentences at full stops, question marks, or exclamation marks
    sentences = re.split(r"(?<=[.!?])\s+", cleaned_text)

    # Remove empty sentences
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    chunks = []

    for i in range(0, len(sentences), sentences_per_chunk):
        group = sentences[i:i + sentences_per_chunk]
        chunk = " ".join(group)
        chunks.append(chunk)

    return chunks

def save_chunks_to_chromadb(client, collection_name, documents, model, chunk_function):
    """Generate embeddings and store chunks in ChromaDB."""

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )

    # Clear existing chunks so repeated runs do not leave old data.
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    chunk_texts = []
    chunk_ids = []
    metadata = []

    for doc in documents:
        chunks = chunk_function(doc["text"])

        for index, chunk in enumerate(chunks):
            chunk_texts.append(chunk)
            chunk_ids.append(f"{doc['filename']}_{index}")
            metadata.append({
                "source": doc["filename"],
                "chunk_index": index
            })

    embeddings = model.encode(
        chunk_texts,
        batch_size=8,
        show_progress_bar=False,
        normalize_embeddings=True
    )

    collection.add(
        ids=chunk_ids,
        documents=chunk_texts,
        embeddings=embeddings.tolist(),
        metadatas=metadata
    )

    print(f"{collection_name}: saved {collection.count()} chunks")

    return collection

if __name__ == "__main__":


    documents = load_documents()

    print(f"Loaded {len(documents)} policy documents.\n")

    print("\nLoading embedding model...")
    model = SentenceTransformer(MODEL_NAME, device="cpu")
    print("Embedding model loaded successfully!")

    test_embedding = model.encode("How long does a COD refund take?")
    print("Embedding dimensions:", len(test_embedding))

    total_fixed_chunks = 0
    total_sentence_chunks = 0

    for doc in documents:
        fixed_chunks = fixed_size_chunking(doc["text"])
        sentence_chunks = sentence_based_chunking(doc["text"])

        print(
            f"{doc['filename']}: "
            f"{len(fixed_chunks)} fixed chunks, "
            f"{len(sentence_chunks)} sentence chunks"
        )

        total_fixed_chunks += len(fixed_chunks)
        total_sentence_chunks += len(sentence_chunks)

    print(f"\nTotal fixed-size chunks: {total_fixed_chunks}")
    print(f"Total sentence-based chunks: {total_sentence_chunks}")

    print("\nCreating ChromaDB collections...")

    client = chromadb.PersistentClient(path="chroma_db")

    fixed_collection = save_chunks_to_chromadb(
        client,
        "nykaa_fixed_chunks",
        documents,
        model,
        fixed_size_chunking
    )

    sentence_collection = save_chunks_to_chromadb(
        client,
        "nykaa_sentence_chunks",
        documents,
        model,
        sentence_based_chunking
    )

    print("\nBoth ChromaDB collections created successfully!")
