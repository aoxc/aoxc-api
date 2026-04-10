from __future__ import annotations

from collections import defaultdict, deque
import hmac
from time import time

from fastapi import HTTPException, Request, status

from app.config import settings

_REQUEST_WINDOW = 60
_request_buckets: dict[str, deque[float]] = defaultdict(deque)


def enforce_rate_limit(request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    now = time()
    bucket = _request_buckets[client_ip]

    while bucket and now - bucket[0] > _REQUEST_WINDOW:
        bucket.popleft()

    if len(bucket) >= settings.requests_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )

    bucket.append(now)


def enforce_developer_api_key(request: Request) -> None:
    if not settings.require_api_key:
        return

    if not settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server API key configuration is missing.",
        )

    provided = request.headers.get("x-api-key", "")
    if not hmac.compare_digest(provided, settings.api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key for developer endpoints.",
        )
