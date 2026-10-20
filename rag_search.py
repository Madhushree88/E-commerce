
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DISTANCE_THRESHOLD = 0.6958
# Connect to the existing ChromaDB database
client = chromadb.PersistentClient(path="chroma_db")

# Load the same embedding model used for indexing
model = SentenceTransformer(MODEL_NAME, device="cpu")

# Sample customer question
question = "How long does a COD refund take?"
# Convert the question into an embedding
query_embedding = model.encode(
    question,
    normalize_embeddings=True
).tolist()

# Search both chunking collections
for collection_name in [
    "nykaa_fixed_chunks",
    "nykaa_sentence_chunks"
]:
    collection = client.get_collection(name=collection_name)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,
        include=["documents", "metadatas", "distances"]
    )

    best_distance = results["distances"][0][0]

    if best_distance > DISTANCE_THRESHOLD:
        print(f"\n--- {collection_name} ---")
        print("OUT OF SCOPE")
        print(
            "Sorry, I can only answer questions covered "
            "by the available Nykaa capstone support policies."
        )
        print("Closest distance:", round(best_distance, 4))
        continue

    print(f"\n--- {collection_name} ---")

    for index, document in enumerate(results["documents"][0]):
        source = results["metadatas"][0][index]["source"]
        distance = results["distances"][0][index]

        print(f"\nResult {index + 1}")
        print("Source:", source)
        print("Distance:", round(distance, 4))
        print("Text:", document)
