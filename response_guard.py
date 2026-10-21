import re


def check_response_guardrail(response: str) -> dict:
    unsupported_promises = [
        r"refund (will|shall) be (issued|processed) within 24 hours",
        r"refund (is|has been) approved",
        r"guaranteed refund",
        r"refund (will|shall) be completed immediately",
    ]

    for pattern in unsupported_promises:
        if re.search(pattern, response, re.IGNORECASE):
            return {
                "passed": False,
                "reason": "Potentially unsupported refund promise detected."
            }

    return {
        "passed": True,
        "reason": "No predefined unsupported refund promises detected."
    }
def check_order_grounding(response: str, order_id: str) -> dict:
    import re

    mentioned_ids = re.findall(r"\bNK\d{4}\b", response)

    if any(found_id != order_id for found_id in mentioned_ids):
        return {
            "passed": False,
            "reason": "Response contains an incorrect order ID."
        }

    if order_id not in mentioned_ids:
        return {
            "passed": False,
            "reason": "Response does not contain the verified order ID."
        }

    return {
        "passed": True,
        "reason": "Response contains only the verified order ID."
    }