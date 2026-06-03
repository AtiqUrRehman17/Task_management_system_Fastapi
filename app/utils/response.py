from datetime import datetime,timezone
from typing import Any, Optional


def api_response(
    *,
    status: bool,
    message: str,
    data: Optional[Any] = None,
    error: Optional[str] = None,
):
    return {
        "status": status,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }