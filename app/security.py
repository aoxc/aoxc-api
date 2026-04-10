from __future__ import annotations

from collections import defaultdict, deque
from time import time

from fastapi import HTTPException, Request, status

from app.config import settings
from app.crypto import RequestSignatureVerifier

_REQUEST_WINDOW = 60
_request_buckets: dict[str, deque[float]] = defaultdict(deque)
_nonce_seen_at: dict[str, float] = {}
_signature_verifier = RequestSignatureVerifier(secret=settings.request_signing_secret)


def _cleanup_nonce_cache(now: float) -> None:
    expired = [nonce for nonce, seen_at in _nonce_seen_at.items() if now - seen_at > settings.nonce_cache_ttl_seconds]
    for nonce in expired:
        _nonce_seen_at.pop(nonce, None)


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


def enforce_signed_request(request: Request) -> None:
    if not settings.require_signed_requests:
        return

    ts_raw = request.headers.get("x-sign-ts", "")
    nonce = request.headers.get("x-sign-nonce", "")
    signature = request.headers.get("x-signature", "")

    if not ts_raw or not nonce or not signature:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature headers")

    try:
        ts = int(ts_raw)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid timestamp") from exc

    now = int(time())
    if abs(now - ts) > settings.request_max_age_seconds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Stale request timestamp")

    _cleanup_nonce_cache(now)
    if nonce in _nonce_seen_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Replay detected")

    payload = f"{request.method}|{request.url.path}|{ts}|{nonce}"
    if not _signature_verifier.verify(payload, signature):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid request signature")

    _nonce_seen_at[nonce] = now
