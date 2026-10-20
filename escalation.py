
from order_lookup import check_order_status


def calculate_escalation_score(record_id):
    order = check_order_status(record_id)

    if not order["found"]:
        return {
            "record_id": record_id,
            "error": "Order not found."
        }

    delayed_score = 70 if order["delayed_shipment"] else 0

    # Normalize order age to a value between 0 and 1.
    normalized_age = min(
        max(order["days_since_created"], 0) / 30,
        1
    )

    age_score = normalized_age * 30

    total_score = round(delayed_score + age_score, 2)

    if total_score >= 70:
        priority = "High"
    elif total_score >= 40:
        priority = "Medium"
    else:
        priority = "Low"

    return {
        "record_id": record_id,
        "escalation_score": total_score,
        "priority": priority,
        "delayed_shipment": order["delayed_shipment"],
        "days_since_created": order["days_since_created"]
    }


if __name__ == "__main__":
    print("TEST 1: Existing order")
    print(calculate_escalation_score("NK0001"))

    print("\nTEST 2: Non-existing order")
    print(calculate_escalation_score("NK9999"))
