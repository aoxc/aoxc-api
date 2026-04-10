from contextlib import contextmanager
import time

from fastapi.testclient import TestClient

from app.config import settings
from app.crypto import RequestSignatureVerifier
from app.main import app

client = TestClient(app)


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


def _signed_headers(from_address: str, to_address: str, amount: float, asset: str, key: str) -> dict[str, str]:
    ts = str(int(time.time()))
    nonce = f"test-nonce-{time.time_ns()}"
    canonical = f"{from_address.lower()}|{to_address.lower()}|{amount:.8f}|{asset.upper()}|{ts}|{nonce}"
    signature = RequestSignatureVerifier(key).create_signature(canonical)
    return {
        "X-AOXC-Timestamp": ts,
        "X-AOXC-Nonce": nonce,
        "X-AOXC-Signature": signature,
    }


def test_auth_challenge_and_verify_issue_session_token() -> None:
    challenge_response = client.post("/api/v1/auth/challenge", json={"wallet_address": "0xA0aB1234"})
    assert challenge_response.status_code == 200
    challenge_data = challenge_response.json()
    assert challenge_data["wallet_address"] == "0xA0aB1234"
    assert challenge_data["nonce"]

    verify_response = client.post(
        "/api/v1/auth/verify",
        json={"wallet_address": "0xA0aB1234", "signature": "signed_payload"},
    )
    assert verify_response.status_code == 200
    verify_data = verify_response.json()
    assert verify_data["access_token"]
    assert verify_data["token_type"] == "Bearer"


def test_chain_policy_check_requires_session_token() -> None:
    response = client.post(
        "/api/v1/chain/tx/policy-check",
        json={
            "from_address": "0xFROM",
            "to_address": "0xTO",
            "amount": 3.5,
            "asset": "AOXC",
        },
    )
    assert response.status_code == 401


def test_chain_policy_check_accepts_valid_token() -> None:
    client.post("/api/v1/auth/challenge", json={"wallet_address": "0xA0aB7777"})
    verify_response = client.post(
        "/api/v1/auth/verify",
        json={"wallet_address": "0xA0aB7777", "signature": "ok"},
    )
    token = verify_response.json()["access_token"]

    response = client.post(
        "/api/v1/chain/tx/policy-check",
        json={
            "from_address": "0xA0aB7777",
            "to_address": "0xA0aB8888",
            "amount": 25.0,
            "asset": "AOXC",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is True
    assert data["policy_version"] == "aoxc-policy-v2"
    assert data["risk_level"] in {"low", "medium", "high"}


def test_wallet_address_validation_rejects_invalid_format() -> None:
    response = client.post("/api/v1/auth/challenge", json={"wallet_address": "alice"})
    assert response.status_code == 422


def test_chain_policy_check_rejects_missing_signature_when_enabled() -> None:
    client.post("/api/v1/auth/challenge", json={"wallet_address": "0xA0aB9000"})
    verify_response = client.post(
        "/api/v1/auth/verify",
        json={"wallet_address": "0xA0aB9000", "signature": "ok"},
    )
    token = verify_response.json()["access_token"]

    with temporary_security_settings(require_request_signature=True, request_signing_key="shared-secret"):
        response = client.post(
            "/api/v1/chain/tx/policy-check",
            json={
                "from_address": "0xA0aB9000",
                "to_address": "0xA0aB9001",
                "amount": 1.0,
                "asset": "AOXC",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 401


def test_chain_policy_check_accepts_valid_signature_when_enabled() -> None:
    from_address = "0xA0aB9002"
    to_address = "0xA0aB9003"
    amount = 2.0
    asset = "AOXC"

    client.post("/api/v1/auth/challenge", json={"wallet_address": from_address})
    verify_response = client.post(
        "/api/v1/auth/verify",
        json={"wallet_address": from_address, "signature": "ok"},
    )
    token = verify_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    headers.update(_signed_headers(from_address, to_address, amount, asset, key="shared-secret-2"))

    with temporary_security_settings(require_request_signature=True, request_signing_key="shared-secret-2"):
        response = client.post(
            "/api/v1/chain/tx/policy-check",
            json={
                "from_address": from_address,
                "to_address": to_address,
                "amount": amount,
                "asset": asset,
            },
            headers=headers,
        )

    assert response.status_code == 200


def test_chain_policy_check_rejects_replay_nonce_when_enabled() -> None:
    from_address = "0xA0aB9004"
    to_address = "0xA0aB9005"
    amount = 2.5
    asset = "AOXC"

    client.post("/api/v1/auth/challenge", json={"wallet_address": from_address})
    verify_response = client.post(
        "/api/v1/auth/verify",
        json={"wallet_address": from_address, "signature": "ok"},
    )
    token = verify_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    headers.update(_signed_headers(from_address, to_address, amount, asset, key="shared-secret-3"))

    with temporary_security_settings(require_request_signature=True, request_signing_key="shared-secret-3"):
        first = client.post(
            "/api/v1/chain/tx/policy-check",
            json={
                "from_address": from_address,
                "to_address": to_address,
                "amount": amount,
                "asset": asset,
            },
            headers=headers,
        )
        second = client.post(
            "/api/v1/chain/tx/policy-check",
            json={
                "from_address": from_address,
                "to_address": to_address,
                "amount": amount,
                "asset": asset,
            },
            headers=headers,
        )

    assert first.status_code == 200
    assert second.status_code == 401


def test_chain_policy_check_rejects_wallet_mismatch() -> None:
    client.post("/api/v1/auth/challenge", json={"wallet_address": "0xA0aB9010"})
    verify_response = client.post(
        "/api/v1/auth/verify",
        json={"wallet_address": "0xA0aB9010", "signature": "ok"},
    )
    token = verify_response.json()["access_token"]

    response = client.post(
        "/api/v1/chain/tx/policy-check",
        json={
            "from_address": "0xA0aBFFFF",
            "to_address": "0xA0aB9011",
            "amount": 1.0,
            "asset": "AOXC",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is False
    assert data["risk_level"] == "high"


def test_chain_rpc_requires_auth_token() -> None:
    response = client.post("/api/v1/chain/rpc", json={"method": "eth_chainId", "params": []})
    assert response.status_code == 401
