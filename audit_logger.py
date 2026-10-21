import json
from datetime import datetime, timezone
from pathlib import Path

from pii_masking import mask_pii


LOG_FILE = Path("logs") / "agent_traces.jsonl"


def write_audit_log(agent_name: str, output: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent_name,
        "output": mask_pii(output),
    }

    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")