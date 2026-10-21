import re


SUSPICIOUS_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"disregard (all )?(previous|prior) instructions",
    r"reveal (your )?(system|developer) prompt",
    r"override (your )?(system|safety) rules",
    r"bypass (your )?(safety|security) checks",
]


def detect_prompt_injection(text: str) -> bool:
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    return False