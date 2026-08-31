import json
import time

import httpx

from app.config import settings
from app.observability.logging_config import log_flow


def notify_flowise(
    request_id: str, event: str, customer_id: int | None, reason: str, risk_level: str
) -> None:
    if not settings.flowise_alerts_enabled:
        return

    payload = {
        "question": json.dumps(
            {
                "event": event,
                "request_id": request_id,
                "customer_id": customer_id,
                "reason": reason,
                "risk_level": risk_level,
            },
            ensure_ascii=False,
        )
    }
    headers = {}
    if settings.flowise_api_key:
        headers["Authorization"] = f"Bearer {settings.flowise_api_key}"

    t0 = time.perf_counter()
    url = f"{settings.flowise_url.rstrip('/')}/api/v1/prediction/{settings.flowise_chatflow_id}"
    try:
        response = httpx.post(
            url, json=payload, headers=headers, timeout=settings.flowise_timeout_s
        )
        log_flow(
            request_id,
            "flowise_notify",
            round((time.perf_counter() - t0) * 1000, 1),
            event=event,
            status_code=response.status_code,
        )
    except Exception as exc:  # noqa: BLE001
        log_flow(
            request_id,
            "flowise_notify_error",
            round((time.perf_counter() - t0) * 1000, 1),
            event=event,
            error=str(exc)[:80],
        )
