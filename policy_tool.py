import subprocess
from pathlib import Path
from crewai.tools import tool

PROJECT_DIR = Path(__file__).resolve().parent


@tool("Search Nykaa Policies")
def policy_search_tool(question: str) -> str:
    """Search fictional Nykaa support policies for a customer question."""

    result = subprocess.run(
        [
            str(PROJECT_DIR / ".venv" / "bin" / "python"),
            str(PROJECT_DIR / "rag_bridge.py"),
            question,
        ],
        cwd=str(PROJECT_DIR),
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        return "Policy search failed. Please escalate to support."

    return result.stdout.strip()