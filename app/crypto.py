from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
from typing import Protocol


SUPPORTED_SIGNATURE_ALGORITHMS: tuple[str, ...] = ("hmac-sha256", "mock-pqc-dilithium2")


class SignatureVerifier(Protocol):
    def create_signature(self, payload: str) -> str:
        ...

    def verify(self, payload: str, provided_signature: str) -> bool:
        ...


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


class MockPQCSignatureVerifier:
    """
    Placeholder for PQC-style verification contract.
    This keeps the request signature API stable for future OQS integration.
    """

    def __init__(self, secret: str) -> None:
        self.secret = secret.encode("utf-8")

    def create_signature(self, payload: str) -> str:
        digest = hashlib.sha3_512(self.secret + b"|" + payload.encode("utf-8")).hexdigest()
        return digest

    def verify(self, payload: str, provided_signature: str) -> bool:
        expected = self.create_signature(payload)
        return hmac.compare_digest(expected, provided_signature)


@dataclass(frozen=True)
class SignatureVerifierSuite:
    primary_alg: str
    primary_verifier: RequestSignatureVerifier | MockPQCSignatureVerifier
    secondary_alg: str | None = None
    secondary_verifier: RequestSignatureVerifier | MockPQCSignatureVerifier | None = None
