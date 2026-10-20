
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TEST_CASES = [
    ("How long does a COD refund take?", "cod_refunds.md"),
    ("Can I exchange footwear for a different size?", "size_exchange.md"),
    ("Can I cancel my order before shipment?", "cancellation.md"),
    ("What if my product arrives damaged?", "damaged_items.md"),
    ("How long does delivery take?", "delivery_sla.md"),
    ("Can I use loyalty points on an order?", "loyalty_points.md"),
]

COLLECTIONS = [
    "nykaa_fixed_chunks",
    "nykaa_sentence_chunks",
]

client = chromadb.PersistentClient(path="chroma_db")
model = SentenceTransformer(MODEL_NAME, device="cpu")

for collection_name in COLLECTIONS:
    collection = client.get_collection(name=collection_name)

    print(f"\n{'=' * 55}")
    print(f"COLLECTION: {collection_name}")
    print(f"{'=' * 55}")

    total_precision = 0
    total_recall = 0

    for question, expected_source in TEST_CASES:
        embedding = model.encode(
            question,
            normalize_embeddings=True
        ).tolist()

        results = collection.query(
            query_embeddings=[embedding],
            n_results=3,
            include=["metadatas"]
        )

        # Evaluate at document level, not chunk level.
        retrieved_sources = list(dict.fromkeys(
            item["source"]
            for item in results["metadatas"][0]
        ))

        relevant_retrieved = int(expected_source in retrieved_sources)

        precision = relevant_retrieved / len(retrieved_sources) if retrieved_sources else 0
        recall = relevant_retrieved / 1

        total_precision += precision
        total_recall += recall

        print(f"\nQuestion: {question}")
        print(f"Expected: {expected_source}")
        print(f"Retrieved documents: {retrieved_sources}")
        print(
            f"Precision = {relevant_retrieved}/{len(retrieved_sources)} "
            f"= {precision:.2f}"
        )
        print(f"Recall = {relevant_retrieved}/1 = {recall:.2f}")

    count = len(TEST_CASES)

    print(f"\nAVERAGE PRECISION: {total_precision / count:.2f}")
    print(f"AVERAGE RECALL: {total_recall / count:.2f}")