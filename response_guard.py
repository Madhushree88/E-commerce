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
def check_cod_refund_grounding(response: str) -> dict:
    import re

    text = response.lower()

    if not re.search(r"\brefund\b", text):
        return {
            "passed": False,
            "reason": "Response does not discuss a refund."
        }

    # Detect individual refund timeframe claims
    timeframes = re.findall(
        r"\b(\d+)\s*business\s*days\b",
        text
    )

    # Reject unsupported single-number timeframes
    if any(number not in ("5", "7") for number in timeframes):
        return {
            "passed": False,
            "reason": "Response contains an unsupported refund timeframe."
        }

    # Check the expected policy timeframe
    correct_timeframe = re.search(
        r"\b5\s*(?:to|-|–)\s*7\s*business\s*days\b",
        text
    )

    if not correct_timeframe:
        return {
            "passed": False,
            "reason": "COD refund timeframe does not match the expected policy."
        }

    return {
        "passed": True,
        "reason": "COD refund timeframe matches the expected policy."
    }

    return {
        "passed": True,
        "reason": "COD refund timeframe matches the expected policy."
    }