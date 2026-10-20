from crewai.tools import tool
from order_lookup import check_order_status
from escalation import calculate_escalation_score

@tool("Check Order Status")
def order_status_tool(record_id: str) -> str:
    """Look up a simulated Nykaa order using its record ID."""
    order = check_order_status(record_id)
    escalation = calculate_escalation_score(record_id)
    if not order["found"]:
        return f"Order {record_id} was not found."

    return (
        f"Order ID: {order['record_id']}\n"
        f"Category: {order['category']}\n"
        f"Status: {order['status']}\n"
        f"Order Value: INR {order['order_value_inr']}\n"
        f"Days Since Created: {order['days_since_created']}\n"
                f"Delayed Shipment: {order['delayed_shipment']}\n"
        f"Escalation Score: {escalation['escalation_score']}\n"
        f"Escalation Priority: {escalation['priority']}"
    )


if __name__ == "__main__":
    print("TEST 1: Existing order")
    print(order_status_tool.run(record_id="NK0001"))

    print("\nTEST 2: Non-existing order")
    print(order_status_tool.run(record_id="NK9999"))