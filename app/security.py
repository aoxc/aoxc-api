from __future__ import annotations

from collections import defaultdict, deque
import hmac
import time

from fastapi import HTTPException, status

from app.config import settings
from app.crypto import SUPPORTED_SIGNATURE_ALGORITHMS, SignatureVerifierSuite, build_verifier

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
    signature_alg_header: str | None = None,
    signature_pq_header: str | None = None,
    key_id_header: str | None = None,
    pq_key_id_header: str | None = None,
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
    nonce_scope_key = f"{from_address.lower()}|{nonce_header}"
    if nonce_scope_key in _seen_nonces:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Replay detected for request nonce.",
        )

    canonical_payload = (
        f"{from_address.lower()}|{to_address.lower()}|{amount:.8f}|"
        f"{asset.upper()}|{timestamp_header}|{nonce_header}"
    )
    requested_alg = (signature_alg_header or settings.request_signature_primary_alg).strip().lower()
    if settings.request_signature_require_key_id and not key_id_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing signature key id header.",
        )
    if key_id_header and key_id_header != settings.request_signing_key_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature key id.",
        )
    suite = _build_signature_verifier_suite(requested_alg)

    if not suite.primary_verifier.verify(canonical_payload, signature_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid request signature.",
        )

    if settings.request_signature_require_hybrid:
        if not signature_pq_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Hybrid mode enabled: missing PQ companion signature header.",
            )
        if not pq_key_id_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Hybrid mode enabled: missing PQ companion key id header.",
            )
        if pq_key_id_header != settings.request_signing_pq_key_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid PQ companion key id.",
            )
        if not suite.secondary_verifier or not suite.secondary_alg:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Hybrid signature verifier is not configured.",
            )
        if not suite.secondary_verifier.verify(canonical_payload, signature_pq_header):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid PQ companion signature.",
            )

    _seen_nonces[nonce_scope_key] = now + settings.signature_nonce_ttl_seconds


def _cleanup_seen_nonces(now: int) -> None:
    expired = [nonce for nonce, expires in _seen_nonces.items() if now >= expires]
    for nonce in expired:
        _seen_nonces.pop(nonce, None)


def _build_signature_verifier_suite(requested_alg: str) -> SignatureVerifierSuite:
    if requested_alg not in settings.request_signature_allowed_algs:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Signature algorithm '{requested_alg}' is not allowed.",
        )

    if requested_alg not in SUPPORTED_SIGNATURE_ALGORITHMS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Unsupported signature algorithm '{requested_alg}'.",
        )
    primary = build_verifier(requested_alg, settings.request_signing_key)

    secondary_verifier = None
    secondary_alg = None
    if settings.request_signature_require_hybrid:
        if not settings.request_signing_pq_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Hybrid mode enabled but REQUEST_SIGNING_PQ_KEY is not configured.",
            )
        secondary_alg = "mock-pqc-dilithium2"
        secondary_verifier = build_verifier(secondary_alg, settings.request_signing_pq_key)

    return SignatureVerifierSuite(
        primary_alg=requested_alg,
        primary_verifier=primary,
        secondary_alg=secondary_alg,
        secondary_verifier=secondary_verifier,
    )


def validate_security_configuration() -> None:
    if not settings.require_request_signature:
        return

    errors: list[str] = []
    if not settings.request_signing_key:
        errors.append("REQUEST_SIGNING_KEY must be set when REQUIRE_REQUEST_SIGNATURE=true.")
    if settings.request_signature_primary_alg not in settings.request_signature_allowed_algs:
        errors.append("REQUEST_SIGNATURE_PRIMARY_ALG must exist in REQUEST_SIGNATURE_ALLOWED_ALGS.")
    unsupported = [alg for alg in settings.request_signature_allowed_algs if alg not in SUPPORTED_SIGNATURE_ALGORITHMS]
    if unsupported:
        errors.append(f"Unsupported algorithms in REQUEST_SIGNATURE_ALLOWED_ALGS: {', '.join(unsupported)}.")
    if settings.request_signature_require_hybrid and not settings.request_signing_pq_key:
        errors.append("REQUEST_SIGNING_PQ_KEY must be set when REQUEST_SIGNATURE_REQUIRE_HYBRID=true.")
    if settings.request_signature_require_key_id and not settings.request_signing_key_id:
        errors.append("REQUEST_SIGNING_KEY_ID must be set when REQUEST_SIGNATURE_REQUIRE_KEY_ID=true.")

    if errors:
        raise ValueError("Invalid security configuration: " + " ".join(errors))
