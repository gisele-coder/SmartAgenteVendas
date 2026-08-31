import threading

_lock = threading.Lock()
_metrics: dict = {}


def _reset_values() -> None:
    _metrics.update(
        {
            "runs_total": 0,
            "success_total": 0,
            "blocked_total": 0,
            "error_total": 0,
            "fallback_total": 0,
            "recommendations_total": 0,
            "total_ms_sum": 0.0,
            "total_ms_max": 0.0,
            "tool_ms_sum": 0.0,
            "tool_ms_max": 0.0,
        }
    )


_reset_values()


def record_run(
    status: str, fallback: bool, recommendations: int, total_ms: float, tool_ms: float
) -> None:
    with _lock:
        _metrics["runs_total"] += 1
        if status == "success":
            _metrics["success_total"] += 1
        elif status == "blocked":
            _metrics["blocked_total"] += 1
        else:
            _metrics["error_total"] += 1
        if fallback:
            _metrics["fallback_total"] += 1
        _metrics["recommendations_total"] += recommendations
        _metrics["total_ms_sum"] += total_ms
        _metrics["total_ms_max"] = max(_metrics["total_ms_max"], total_ms)
        _metrics["tool_ms_sum"] += tool_ms
        _metrics["tool_ms_max"] = max(_metrics["tool_ms_max"], tool_ms)


def snapshot() -> dict:
    with _lock:
        data = dict(_metrics)
    runs = data["runs_total"]
    data["total_ms_avg"] = round(data["total_ms_sum"] / runs, 1) if runs else None
    data["tool_ms_avg"] = round(data["tool_ms_sum"] / runs, 1) if runs else None
    data.pop("total_ms_sum")
    data.pop("tool_ms_sum")
    data["total_ms_max"] = round(data["total_ms_max"], 1)
    data["tool_ms_max"] = round(data["tool_ms_max"], 1)
    data["block_rate"] = round(data["blocked_total"] / runs, 2) if runs else None
    data["fallback_rate"] = round(data["fallback_total"] / runs, 2) if runs else None
    return data


def reset() -> None:
    with _lock:
        _reset_values()
