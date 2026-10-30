import re


def validate_final_response(response: str, expected_order_id: str) -> dict:
    issues = []

    # Check 1: Correct order reference
    mentioned_ids = re.findall(r"\bNK\d{4}\b", response, re.IGNORECASE)

    if not mentioned_ids:
        issues.append("Order ID is missing.")
    elif any(
        order_id.upper() != expected_order_id.upper()
        for order_id in mentioned_ids
    ):
        issues.append("Response contains an incorrect order ID.")

    # Check 2: Required fictional COD refund timeframe
    if not re.search(
        r"5\s*[-–to]+\s*7\s+business days",
        response,
        re.IGNORECASE,
    ):
        issues.append("Expected COD refund timeframe is missing.")

    # Check 3: Unsupported refund approval claims
    unsupported_claims = [
        r"your refund (has been|is) approved",
        r"refund (has been|is) approved for (your|this) order",
        r"your refund has been initiated",
        r"guaranteed refund",
    ]

    for pattern in unsupported_claims:
        if re.search(pattern, response, re.IGNORECASE):
            issues.append("Unsupported refund approval or guarantee detected.")
            break

    return {
        "valid": len(issues) == 0,
        "verdict": "APPROVED" if not issues else "REJECTED",
        "issues": issues,
    }