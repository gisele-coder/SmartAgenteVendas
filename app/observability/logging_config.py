import json
import logging
import time
from datetime import UTC, datetime
from pathlib import Path

from app.config import settings

FLOW_LOGGER = "smartorder.flow"


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        if isinstance(record.msg, str):
            try:
                json.loads(record.msg)
                return record.msg
            except ValueError:
                payload = {"message": record.getMessage()}
        else:
            payload = dict(record.msg)
        payload.update(
            {
                "ts": datetime.now(UTC).isoformat(),
                "level": record.levelname,
                "logger": record.name,
            }
        )
        return json.dumps(payload, ensure_ascii=False)


def get_flow_logger() -> logging.Logger:
    return logging.getLogger(FLOW_LOGGER)


def setup_logging() -> None:
    logger = logging.getLogger(FLOW_LOGGER)
    if logger.handlers:
        return
    logger.setLevel(logging.INFO)
    formatter = JsonFormatter()
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    log_path = Path(settings.log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False


def log_flow(request_id: str, node: str, latency_ms: float, **extra) -> None:
    payload = {
        "request_id": request_id,
        "node": node,
        "latency_ms": latency_ms,
        **extra,
    }
    get_flow_logger().info(json.dumps(payload, ensure_ascii=False))


def now_ms() -> float:
    return time.perf_counter() * 1000
