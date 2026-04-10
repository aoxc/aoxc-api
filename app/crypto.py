from __future__ import annotations

import hashlib
import hmac


class RequestSignatureVerifier:
    """
    Quantum-level tam guvenlik tek bir kutuphane ile garanti edilemez.
    Bu sinif pratikte guvenli bir temel saglar: HMAC-SHA256.

    Gelecekte OQS/Dilithium gibi post-quantum imzaya gecis icin API sabittir.
    """

    def __init__(self, secret: str) -> None:
        self.secret = secret.encode("utf-8")

    def create_signature(self, payload: str) -> str:
        digest = hmac.new(self.secret, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return digest

    def verify(self, payload: str, provided_signature: str) -> bool:
        expected = self.create_signature(payload)
        return hmac.compare_digest(expected, provided_signature)
