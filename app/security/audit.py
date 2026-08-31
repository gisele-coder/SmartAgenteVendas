import json
from datetime import UTC, datetime
from pathlib import Path

from app.config import settings


def write_audit(request_id: str, events: list[dict]) -> None:
    path = Path(settings.audit_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    recorded_at = datetime.now(UTC).isoformat()
    with path.open("a", encoding="utf-8") as file:
        for event in events:
            record = {"request_id": request_id, "recorded_at": recorded_at, **event}
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
