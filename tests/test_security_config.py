from contextlib import contextmanager
import time

import pytest
from fastapi import HTTPException

from app.config import settings
from app.crypto import RequestSignatureVerifier
from app.security import enforce_tx_request_signature, validate_security_configuration


@contextmanager
def temporary_security_settings(**kwargs):
    previous = {key: getattr(settings, key) for key in kwargs}
    try:
        for key, value in kwargs.items():
            object.__setattr__(settings, key, value)
        yield
    finally:
        for key, value in previous.items():
            object.__setattr__(settings, key, value)


def _signature_headers(
    from_address: str,
    to_address: str,
    amount: float,
    asset: str,
    secret: str,
    nonce: str,
    ts: str,
) -> tuple[str, str, str]:
    canonical = f"{from_address.lower()}|{to_address.lower()}|{amount:.8f}|{asset.upper()}|{ts}|{nonce}"
    signature = RequestSignatureVerifier(secret).create_signature(canonical)
    return ts, nonce, signature


def test_validate_security_configuration_rejects_unsupported_algorithm() -> None:
    with temporary_security_settings(
        require_request_signature=True,
        request_signing_key="secret",
        request_signature_primary_alg="hmac-sha256",
        request_signature_allowed_algs=("hmac-sha256", "future-ml-dsa"),
    ):
        with pytest.raises(ValueError):
            validate_security_configuration()


def test_enforce_signature_nonce_is_scoped_per_from_address() -> None:
    ts = str(int(time.time()))
    nonce = f"nonce-{time.time_ns()}"
    amount = 2.0
    asset = "AOXC"
    from_a = "0xA0aB1000"
    from_b = "0xA0aB1001"
    to_address = "0xA0aB2000"
    secret = "scope-secret"
    _, _, sig_a = _signature_headers(from_a, to_address, amount, asset, secret, nonce, ts)
    _, _, sig_b = _signature_headers(from_b, to_address, amount, asset, secret, nonce, ts)

    with temporary_security_settings(
        require_request_signature=True,
        request_signing_key=secret,
        signature_max_skew_seconds=300,
        signature_nonce_ttl_seconds=600,
    ):
        enforce_tx_request_signature(from_a, to_address, amount, asset, ts, nonce, sig_a)
        enforce_tx_request_signature(from_b, to_address, amount, asset, ts, nonce, sig_b)


def test_enforce_signature_requires_key_id_when_enabled() -> None:
    ts = str(int(time.time()))
    nonce = f"nonce-{time.time_ns()}"
    from_address = "0xA0aB1100"
    to_address = "0xA0aB2200"
    amount = 1.5
    asset = "AOXC"
    secret = "kid-secret"
    _, _, signature = _signature_headers(from_address, to_address, amount, asset, secret, nonce, ts)

    with temporary_security_settings(
        require_request_signature=True,
        request_signing_key=secret,
        request_signature_require_key_id=True,
    ):
        with pytest.raises(HTTPException) as exc:
            enforce_tx_request_signature(from_address, to_address, amount, asset, ts, nonce, signature)
        assert exc.value.status_code == 401
