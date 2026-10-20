
import random
from collections import Counter

# Fixed seed makes the dataset reproducible.
SEED = 42
random.seed(SEED)

CATEGORIES = [
    "Apparel",
    "Electronics",
    "Home",
    "Footwear",
    "Beauty",
]

STATUSES = [
    "Placed",
    "Shipped",
    "Delivered",
    "Returned",
    "Refunded",
]

# Realistic illustrative order values in Indian rupees.
MIN_AMOUNT = 300
MAX_AMOUNT = 15000

ORDERS = []

# Guarantee at least 3 orders for every category.
for category in CATEGORIES:
    for _ in range(3):
        ORDERS.append({
            "record_id": f"NK{len(ORDERS) + 1:04d}",
            "category": category,
            "status": random.choice(STATUSES),
            "order_value_inr": random.randint(
                MIN_AMOUNT, MAX_AMOUNT
            ),
            "days_since_created": random.randint(0, 30),
            "delayed_shipment": False,
        })

# Add more orders to reach 50 records.
while len(ORDERS) < 50:
    ORDERS.append({
        "record_id": f"NK{len(ORDERS) + 1:04d}",
        "category": random.choice(CATEGORIES),
        "status": random.choice(STATUSES),
        "order_value_inr": random.randint(
            MIN_AMOUNT, MAX_AMOUNT
        ),
        "days_since_created": random.randint(0, 30),
        "delayed_shipment": False,
    })

# Ensure every required status occurs at least once.
for index, status in enumerate(STATUSES):
    ORDERS[index]["status"] = status

# Assign shipment delays randomly using the same seed.
for order in ORDERS:
    order["delayed_shipment"] = random.random() < 0.20

# Report dataset statistics.
print("Total orders:", len(ORDERS))
print("\nOrders per category:")
print(Counter(order["category"] for order in ORDERS))

print("\nOrders per status:")
print(Counter(order["status"] for order in ORDERS))

delayed_count = sum(
    order["delayed_shipment"] for order in ORDERS
)
delayed_percentage = delayed_count / len(ORDERS) * 100

print(f"\nDelayed orders: {delayed_count}/"
      f"{len(ORDERS)} ({delayed_percentage:.1f}%)")

print("\nFirst 3 orders:")
for order in ORDERS[:3]:
    print(order)

import json
from pathlib import Path

# Save the generated orders to a JSON file.
data_folder = Path(__file__).resolve().parent / "data"
data_folder.mkdir(exist_ok=True)

output_file = data_folder / "orders.json"

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(ORDERS, file, indent=4)

print("\nDataset saved to:", output_file)

# Validate dataset requirements
assert len(ORDERS) >= 40, "Not enough orders"

category_counts = Counter(
    order["category"] for order in ORDERS
)
status_counts = Counter(
    order["status"] for order in ORDERS
)

assert all(
    category_counts[category] >= 3
    for category in CATEGORIES
), "A category has fewer than 3 orders"

assert all(
    status_counts[status] >= 1
    for status in STATUSES
), "A required status is missing"

assert 10 <= delayed_percentage <= 30, \
    "Delayed shipment percentage is outside 10–30%"

assert all(
    0 <= order["days_since_created"] <= 30
    for order in ORDERS
), "Invalid order age"

assert len({
    order["record_id"] for order in ORDERS
}) == len(ORDERS), "Duplicate record IDs"

print("\nAll dataset validation checks PASSED!")
