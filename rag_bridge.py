import sys
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DISTANCE_THRESHOLD = 0.6958

if len(sys.argv) < 2:
    print("Please provide a customer question.")
    sys.exit(1)

question = " ".join(sys.argv[1:])

question = question.replace("Cash on Delivery", "COD")
question = question.replace("cash on delivery", "COD")
# Load existing ChromaDB database
client = chromadb.PersistentClient(path="chroma_db")

# Load embedding model
model = SentenceTransformer(MODEL_NAME, device="cpu")

# Convert question into an embedding
query_embedding = model.encode(
    question,
    normalize_embeddings=True
).tolist()

# Search the sentence-based collection
collection = client.get_collection(
    name="nykaa_sentence_chunks"
)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
    include=["documents", "metadatas", "distances"]
)

best_distance = results["distances"][0][0]

if best_distance > DISTANCE_THRESHOLD:
    print("OUT OF SCOPE")
    print("No relevant policy found.")
else:
    for index, document in enumerate(results["documents"][0]):
        source = results["metadatas"][0][index]["source"]
        distance = results["distances"][0][index]

        print(f"Source: {source}")
        print(f"Distance: {distance:.4f}")
        print(f"Policy: {document}")
        print("---")