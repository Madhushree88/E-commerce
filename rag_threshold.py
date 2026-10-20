
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Questions covered by our fictional policy documents
IN_SCOPE_QUESTIONS = [
    "How long does a COD refund take?",
    "Can I exchange footwear for a different size?",
    "Can I cancel my order before shipment?",
    "What happens if my product arrives damaged?",
    "How long does delivery take?",
]

# Questions unrelated to our policy documents
OUT_OF_SCOPE_QUESTIONS = [
    "Who won the FIFA World Cup in 2022?",
    "How do I cook vegetable biryani?",
    "What is the distance between Earth and Mars?",
]

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="nykaa_sentence_chunks"
)

model = SentenceTransformer(MODEL_NAME, device="cpu")


def test_question(question, expected_scope):
    embedding = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=1,
        include=["metadatas", "distances"]
    )

    distance = results["distances"][0][0]
    source = results["metadatas"][0][0]["source"]

    print(f"\nQuestion: {question}")
    print(f"Expected: {expected_scope}")
    print(f"Closest document: {source}")
    print(f"Cosine distance: {distance:.4f}")

    return distance


print("\n========== IN-SCOPE QUESTIONS ==========")

in_scope_distances = []

for question in IN_SCOPE_QUESTIONS:
    distance = test_question(question, "IN SCOPE")
    in_scope_distances.append(distance)


print("\n========== OUT-OF-SCOPE QUESTIONS ==========")

out_of_scope_distances = []

for question in OUT_OF_SCOPE_QUESTIONS:
    distance = test_question(question, "OUT OF SCOPE")
    out_of_scope_distances.append(distance)


print("\n========== CALIBRATION SUMMARY ==========")

print(
    "Highest in-scope distance:",
    round(max(in_scope_distances), 4)
)

print(
    "Lowest out-of-scope distance:",
    round(min(out_of_scope_distances), 4)
)

if max(in_scope_distances) < min(out_of_scope_distances):
    suggested_threshold = (
        max(in_scope_distances) +
        min(out_of_scope_distances)
    ) / 2

    print(
        "Candidate threshold:",
        round(suggested_threshold, 4)
    )
else:
    print(
        "Distance ranges overlap. "
        "A single threshold cannot perfectly separate these test questions."
    )
