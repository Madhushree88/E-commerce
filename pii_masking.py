import re


def mask_pii(text: str) -> str:
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[EMAIL_MASKED]",
        text
    )

    text = re.sub(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",
        "[PHONE_MASKED]",
        text
    )

    return text