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