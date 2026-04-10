from __future__ import annotations

from collections import defaultdict, deque
import hmac
import time

from fastapi import HTTPException, status

from app.config import settings
from app.crypto import RequestSignatureVerifier

_REQUEST_WINDOW = 60
_request_buckets: dict[str, deque[float]] = defaultdict(deque)
_seen_nonces: dict[str, float] = {}


def enforce_rate_limit(request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    bucket = _request_buckets[client_ip]

    while bucket and now - bucket[0] > _REQUEST_WINDOW:
        bucket.popleft()

    if len(bucket) >= settings.requests_per_minute:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later.",
        )

    bucket.append(now)


def enforce_developer_api_key(request) -> None:
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


def enforce_tx_request_signature(
    from_address: str,
    to_address: str,
    amount: float,
    asset: str,
    timestamp_header: str | None,
    nonce_header: str | None,
    signature_header: str | None,
) -> None:
    if not settings.require_request_signature:
        return

    if not settings.request_signing_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Request signing key is not configured.",
        )

    if not timestamp_header or not nonce_header or not signature_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing request signature headers.",
        )

    try:
        request_ts = int(timestamp_header)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request timestamp format.",
        ) from exc

    now = int(time.time())
    if abs(now - request_ts) > settings.signature_max_skew_seconds:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Request timestamp outside allowed clock skew.",
        )

    _cleanup_seen_nonces(now)
    if nonce_header in _seen_nonces:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Replay detected for request nonce.",
        )

    canonical_payload = (
        f"{from_address.lower()}|{to_address.lower()}|{amount:.8f}|"
        f"{asset.upper()}|{timestamp_header}|{nonce_header}"
    )
    verifier = RequestSignatureVerifier(settings.request_signing_key)
    if not verifier.verify(canonical_payload, signature_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request signature.",
        )

    _seen_nonces[nonce_header] = now + settings.signature_nonce_ttl_seconds


def _cleanup_seen_nonces(now: int) -> None:
    expired = [nonce for nonce, expires in _seen_nonces.items() if now >= expires]
    for nonce in expired:
        _seen_nonces.pop(nonce, None)
