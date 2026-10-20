
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "orders.json"


def check_order_status(record_id):
    """Find an order by its record ID."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        orders = json.load(file)

    for order in orders:
        if order["record_id"] == record_id:
            return {
                "found": True,
                "record_id": order["record_id"],
                "category": order["category"],
                "status": order["status"],
                "order_value_inr": order["order_value_inr"],
                "days_since_created": order["days_since_created"],
                "delayed_shipment": order["delayed_shipment"]
            }

    return {
        "found": False,
        "record_id": record_id,
        "message": "Order not found."
    }


if __name__ == "__main__":
    print("TEST 1: Existing order")
    print(check_order_status("NK0001"))

    print("\nTEST 2: Non-existing order")
    print(check_order_status("NK9999"))
